import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import os, re

HEX_INT_RE = re.compile(
    r"""^
        0[xX]
        [0-9A-Fa-f](?:'?[0-9A-Fa-f])*        # цифры с возможными разделителями '
        (?:                                   # необязательный суффикс
            [uU](?:[lL]{1,2})? |              # U, UL, ULL
            (?:[lL]{1,2})[uU]?                # L, LL, LU, LLU
        )?
        $""",
    re.X
)

def strip_wrapping_parens(s: str) -> str:
    # Убираем внешние скобки, если они охватывают всю строку
    s = s.strip()
    while s.startswith("(") and s.endswith(")"):
        depth = 0
        ok = True
        for i, ch in enumerate(s):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0 and i != len(s) - 1:
                    ok = False
                    break
        if ok and depth == 0:
            s = s[1:-1].strip()
        else:
            break
    return s

def join_backslash_lines(text: str) -> str:
    # Склеиваем строки с обратным слешем в конце (многострочные макроопределения)
    out = []
    buf = ""
    for line in text.splitlines():
        if buf:
            buf += line
        else:
            buf = line
        if buf.rstrip().endswith("\\"):
            buf = buf.rstrip()[:-1]  # убираем слеш и продолжаем на следующей строке
            continue
        out.append(buf)
        buf = ""
    if buf:
        out.append(buf)
    return "\n".join(out)

def remove_block_comments(text: str) -> str:
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)

def find_myconst_values(code: str):
    # Упрощённо: уберём блочные комментарии, склеим продолжения строк, обработаем построчно
    code = remove_block_comments(code)
    code = join_backslash_lines(code)
    results = []
    for raw_line in code.splitlines():
        line = raw_line
        # убираем // комментарий
        pos = line.find("//")
        if pos != -1:
            line = line[:pos]
        m = re.match(r"^\s*#\s*define\s+MYCONST\s+(.+?)\s*$", line)
        if not m:
            continue
        rhs = m.group(1).strip()
        rhs_no_paren = strip_wrapping_parens(rhs)
        is_hex = HEX_INT_RE.match(rhs_no_paren) is not None
        results.append((raw_line, rhs, rhs_no_paren, is_hex))
    return results

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ЛР №2: Проверка #define MYCONST на шестнадцатеричную целую константу")
        self.geometry("900x600")
        self._build_ui()
        self.file_path = None

    def _build_ui(self):
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=8, pady=6)

        tk.Button(top, text="Открыть файл", command=self.open_file).pack(side=tk.LEFT)
        tk.Button(top, text="Анализировать", command=self.analyze).pack(side=tk.LEFT, padx=6)
        tk.Button(top, text="Очистить", command=self.clear_all).pack(side=tk.LEFT, padx=6)

        pan = tk.PanedWindow(self, sashrelief=tk.RAISED, sashwidth=6)
        pan.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(pan)
        right = tk.Frame(pan, width=320)

        self.code_text = ScrolledText(left, wrap=tk.NONE, undo=True)
        self.code_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        tk.Label(right, text="Результат").pack(anchor="w", padx=6, pady=(6,0))
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

        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", content)
        self.file_path = path
        self.status.set(f"Открыт файл: {os.path.basename(path)}")
        self._set_result("")

    def analyze(self):
        code = self.code_text.get("1.0", tk.END)
        if not code.strip():
            messagebox.showinfo("Анализ", "Текст пуст. Откройте файл или вставьте код.")
            return
        items = find_myconst_values(code)
        if not items:
            self._set_result("Не найдено строк вида: #define MYCONST <значение>")
            self.status.set("Готово")
            return

        lines = []
        for raw_line, rhs, rhs_no_paren, is_hex in items:
            verdict = "ДА, это целая шестнадцатеричная константа" if is_hex else "НЕТ"
            lines.append(f"Строка: {raw_line.strip()}")
            lines.append(f"Правая часть: {rhs}")
            if rhs != rhs_no_paren:
                lines.append(f"Без внешних скобок: {rhs_no_paren}")
            lines.append(f"Результат: {verdict}")
            lines.append("")

        self._set_result("\n".join(lines))
        self.status.set("Анализ завершён.")

    def clear_all(self):
        self.code_text.delete("1.0", tk.END)
        self._set_result("")
        self.status.set("Готово")

    def _set_result(self, text: str):
        self.result.config(state=tk.NORMAL)
        self.result.delete("1.0", tk.END)
        self.result.insert("1.0", text)
        self.result.config(state=tk.DISABLED)

if __name__ == "__main__":
    App().mainloop()
