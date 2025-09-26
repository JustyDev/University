import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import re, os

# Число:   1) d+.d+ (возможен e[+-]?d+), не допускаем "... .d" после (чтобы не ловить 2.2.5)
#          2) d+e[+-]?d+
#          3) d+  (не перед/после точки, чтобы не ловить "0." и "..5")
NUM_RE = re.compile(r"""
(?<![A-Za-z_\.])(
    \d+\.\d+(?:[eE][+-]?\d+)?(?!\.\d)(?![A-Za-z_0-9]) |  # 22.5, 2.25e1
    \d+(?:[eE][+-]?\d+)(?![A-Za-z_0-9]) |                # 8e-2
    \d+(?!\.)(?![A-Za-z_0-9])                            # 67
)
""", re.X)

def find_numbers_in_line(s: str):
    return [m.group(0) for m in NUM_RE.finditer(s)]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ЛР №6: Поиск вещественных/числовых значений в строках")
        self.geometry("900x600")
        self._ui()

    def _ui(self):
        top = tk.Frame(self); top.pack(fill=tk.X, padx=8, pady=6)
        tk.Button(top, text="Открыть файл", command=self.open_file).pack(side=tk.LEFT)
        tk.Button(top, text="Анализировать", command=self.analyze).pack(side=tk.LEFT, padx=6)
        tk.Button(top, text="Очистить", command=self.clear_all).pack(side=tk.LEFT, padx=6)
        tk.Button(top, text="Вставить примеры", command=self.insert_examples).pack(side=tk.LEFT, padx=6)

        pan = tk.PanedWindow(self, sashrelief=tk.RAISED, sashwidth=6); pan.pack(fill=tk.BOTH, expand=True)
        left = tk.Frame(pan); right = tk.Frame(pan, width=380)
        tk.Label(left, text="Исходный текст / код").pack(anchor="w", padx=6, pady=(6,0))
        self.src = ScrolledText(left, wrap=tk.NONE, undo=True); self.src.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        tk.Label(right, text="Результат анализа").pack(anchor="w", padx=6, pady=(6,0))
        self.dst = ScrolledText(right, wrap=tk.WORD, state=tk.DISABLED); self.dst.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        pan.add(left, stretch="always"); pan.add(right)

    def open_file(self):
        path = filedialog.askopenfilename(
            title="Открыть файл",
            filetypes=[("C/C++/Text files", "*.cpp *.cc *.cxx *.hpp *.hh *.h *.txt *.md *.log"), ("All files", "*.*")]
        )
        if not path: return
        for enc in ("utf-8-sig","utf-8","cp1251","latin-1"):
            try:
                with open(path, "r", encoding=enc) as f: data = f.read(); break
            except Exception: data = None
        if data is None:
            with open(path, "r", encoding="utf-8", errors="replace") as f: data = f.read()
        self.src.delete("1.0", tk.END); self.src.insert("1.0", data)

    def analyze(self):
        text = self.src.get("1.0", tk.END)
        if not text.strip():
            messagebox.showinfo("Анализ", "Текст пуст."); return
        lines_out = []
        for i, line in enumerate(text.splitlines(), 1):
            nums = find_numbers_in_line(line)
            if nums:
                lines_out.append(f"{i}: {', '.join(nums)}")
        self.dst.config(state=tk.NORMAL)
        self.dst.delete("1.0", tk.END)
        self.dst.insert("1.0", "\n".join(lines_out) if lines_out else "Чисел не найдено")
        self.dst.config(state=tk.DISABLED)

    def clear_all(self):
        self.src.delete("1.0", tk.END)
        self.dst.config(state=tk.NORMAL); self.dst.delete("1.0", tk.END); self.dst.config(state=tk.DISABLED)

    def insert_examples(self):
        ex = "\n".join([
            'Abc+0.03-iuy',
            '0.h2-87ky/u',
            '-(8e-2*6t)+y+1.1',
            'iu-0.12+t5r/67=we2q',
            '2.2.5',
            '2..5',
            '2.25ee1'
        ])
        self.src.delete("1.0", tk.END)
        self.src.insert("1.0", ex)

if __name__ == "__main__":
    App().mainloop()
