import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import os
import re

# Русские и латинские гласные (й/Й считается согласной)
VOWELS = set("аеёиоуыэюяАЕЁИОУЫЭЮЯaeiouyAEIOUY")

WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё]+")

def abbreviate_word(word: str) -> str:
    # Найти первую гласную
    n = len(word)
    iv = -1
    for i, ch in enumerate(word):
        if ch in VOWELS:
            iv = i
            break
    if iv == -1:
        return word  # нет гласных — не сокращаем

    j = iv + 1
    # подряд идущие гласные
    while j < n and word[j] in VOWELS:
        j += 1
    # затем первая группа согласных после последовательности гласных
    while j < n and word[j].isalpha() and word[j] not in VOWELS:
        j += 1

    cut = word[:j]
    return cut + "." if j < n else cut  # добавляем точку, только если что-то отрезали

def transform_text(text: str) -> str:
    # Заменяем только «слова» (последовательности букв), остальное — как есть
    return WORD_RE.sub(lambda m: abbreviate_word(m.group(0)), text)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ЛР №4: Сокращение слов в тексте")
        self.geometry("1000x650")
        self._build_ui()
        self.file_path = None

    def _build_ui(self):
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=8, pady=6)

        tk.Button(top, text="Открыть файл", command=self.open_file).pack(side=tk.LEFT)
        tk.Button(top, text="Обработать", command=self.process).pack(side=tk.LEFT, padx=6)
        tk.Button(top, text="Очистить", command=self.clear_all).pack(side=tk.LEFT, padx=6)
        tk.Button(top, text="Вставить пример", command=self.insert_example).pack(side=tk.LEFT, padx=6)

        pan = tk.PanedWindow(self, sashrelief=tk.RAISED, sashwidth=6)
        pan.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(pan)
        right = tk.Frame(pan, width=450)

        tk.Label(left, text="Исходный текст").pack(anchor="w", padx=6, pady=(6,0))
        self.src = ScrolledText(left, wrap=tk.WORD, undo=True)
        self.src.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        tk.Label(right, text="Результат").pack(anchor="w", padx=6, pady=(6,0))
        self.dst = ScrolledText(right, wrap=tk.WORD, state=tk.DISABLED)
        self.dst.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        pan.add(left, stretch="always")
        pan.add(right)

        self.status = tk.StringVar(value="Готово")
        tk.Label(self, textvariable=self.status, anchor="w", relief=tk.SUNKEN).pack(fill=tk.X, side=tk.BOTTOM)

    def open_file(self):
        path = filedialog.askopenfilename(
            title="Открыть текстовый файл",
            filetypes=[("Text files", "*.txt *.md *.log *.csv *.cpp *.h"), ("All files", "*.*")]
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

        self.src.delete("1.0", tk.END)
        self.src.insert("1.0", content)
        self.file_path = path
        self.status.set(f"Открыт файл: {os.path.basename(path)}")
        self._set_result("")

    def process(self):
        text = self.src.get("1.0", tk.END)
        if not text.strip():
            messagebox.showinfo("Обработка", "Текст пуст. Откройте файл или введите текст.")
            return
        result = transform_text(text)
        self._set_result(result)
        self.status.set("Готово: обработано.")

    def clear_all(self):
        self.src.delete("1.0", tk.END)
        self._set_result("")
        self.status.set("Готово")

    def insert_example(self):
        example = "Проверка вывода текста производится согласно установленного правила"
        self.src.delete("1.0", tk.END)
        self.src.insert("1.0", example)
        self._set_result("")

    def _set_result(self, s: str):
        self.dst.config(state=tk.NORMAL)
        self.dst.delete("1.0", tk.END)
        self.dst.insert("1.0", s)
        self.dst.config(state=tk.DISABLED)

if __name__ == "__main__":
    App().mainloop()
