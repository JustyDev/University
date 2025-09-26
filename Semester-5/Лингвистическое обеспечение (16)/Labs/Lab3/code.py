import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import re, os

MACROS_TO_CHECK = {
    "MAIN":       r"#\s*define\s+MAIN\b",
    "DO":         r"#\s*define\s+DO\b",
    "WHILE":      r"#\s*define\s+WHILE\s*\(",
    "OPEN_OUT":   r"#\s*define\s+OPEN_OUT\s*\(",
    "OPEN_IN":    r"#\s*define\s+OPEN_IN\s*\(",
    "WRITE_REAL": r"#\s*define\s+WRITE_REAL\s*\(",
    "READ_REAL":  r"#\s*define\s+READ_REAL\s*\(",
    "CLOSE":      r"#\s*define\s+CLOSE\s*\(",
}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ЛР №3: Макросы с параметрами — минимальный просмотр/проверка")
        self.geometry("900x600")
        self._build_ui()
        self.file_path = None

    def _build_ui(self):
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=8, pady=6)

        tk.Button(top, text="Открыть C++ файл", command=self.open_file).pack(side=tk.LEFT)
        tk.Button(top, text="Проверить макросы", command=self.check_macros).pack(side=tk.LEFT, padx=6)
        tk.Button(top, text="Очистить", command=self.clear_all).pack(side=tk.LEFT, padx=6)

        pan = tk.PanedWindow(self, sashrelief=tk.RAISED, sashwidth=6)
        pan.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(pan)
        right = tk.Frame(pan, width=320)

        self.code = ScrolledText(left, wrap=tk.NONE, undo=True)
        self.code.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        tk.Label(right, text="Результат проверки").pack(anchor="w", padx=6, pady=(8,0))
        self.result = ScrolledText(right, wrap=tk.WORD, height=10, state=tk.DISABLED)
        self.result.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        pan.add(left, stretch="always")
        pan.add(right)

        self.status = tk.StringVar(value="Готово")
        tk.Label(self, textvariable=self.status, anchor="w", relief=tk.SUNKEN).pack(fill=tk.X, side=tk.BOTTOM)

    def open_file(self):
        path = filedialog.askopenfilename(
            title="Открыть C/C++ файл",
            filetypes=[("C/C++ files", "*.cpp *.cc *.cxx *.hpp *.hh *.h *.hxx"), ("All files", "*.*")]
        )
        if not path:
            return
        content = None
        for enc in ("utf-8-sig", "utf-8", "cp1251", "latin-1"):
            try:
                with open(path, "r", encoding=enc) as f:
                    content = f.read()
                break
            except Exception:
                continue
        if content is None:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

        self.code.delete("1.0", tk.END)
        self.code.insert("1.0", content)
        self.file_path = path
        self.status.set(f"Открыт файл: {os.path.basename(path)}")
        self._set_result("")

    def check_macros(self):
        text = self.code.get("1.0", tk.END)
        if not text.strip():
            messagebox.showinfo("Проверка", "Текст пуст. Откройте файл или вставьте код.")
            return

        lines = ["Проверка наличия макросов:"]
        for name, pattern in MACROS_TO_CHECK.items():
            found = re.search(pattern, text)
            lines.append(f" - {name}: {'найден' if found else 'не найден'}")

        self._set_result("\n".join(lines))
        self.status.set("Проверка завершена.")

    def clear_all(self):
        self.code.delete("1.0", tk.END)
        self._set_result("")
        self.status.set("Готово")

    def _set_result(self, s: str):
        self.result.config(state=tk.NORMAL)
        self.result.delete("1.0", tk.END)
        self.result.insert("1.0", s)
        self.result.config(state=tk.DISABLED)

if __name__ == "__main__":
    App().mainloop()
