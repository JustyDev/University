import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import os


class CppAnalyzer:
    def __init__(self):
        self.text = ""
        self.n = 0
        self.i = 0
        self.line = 1
        self.col = 1

    def set_text(self, text):
        # Важно: Python по умолчанию читает с переводом строк в '\n'
        self.text = text
        self.n = len(text)
        self.i = 0
        self.line = 1
        self.col = 1

    def _peek(self, k=0):
        j = self.i + k
        if 0 <= j < self.n:
            return self.text[j]
        return ""

    def _prev(self, k=1):
        j = self.i - k
        if 0 <= j < self.n:
            return self.text[j]
        return ""

    def _advance_one(self):
        c = self._peek(0)
        self.i += 1
        if c == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return c

    def _advance(self, count):
        for _ in range(count):
            self._advance_one()

    def _skip_line_comment(self):
        # После //
        while self.i < self.n:
            c = self._advance_one()
            if c == "\n":
                break

    def _skip_block_comment(self):
        # После /*
        while self.i < self.n:
            c = self._advance_one()
            if c == "*" and self._peek(0) == "/":
                self._advance(1)  # пропустить '/'
                break

    def _skip_normal_string(self):
        # Ожидается, что текущая позиция стоит сразу после начальной кавычки "
        escaped = False
        while self.i < self.n:
            c = self._advance_one()
            if escaped:
                escaped = False
                continue
            if c == "\\":
                escaped = True
                continue
            if c == '"':
                break

    def _skip_char_literal(self):
        # Ожидается, что текущая позиция стоит сразу после начальной кавычки '
        escaped = False
        while self.i < self.n:
            c = self._advance_one()
            if escaped:
                escaped = False
                continue
            if c == "\\":
                escaped = True
                continue
            if c == "'":
                break

    def _skip_raw_string_after_prefix(self):
        """
        На входе: позиция i указывает на символ " (после R и, возможно, префикса u/U/L/u8).
        Формат: R"delim( ... )delim"
        Мы сейчас на первой кавычке. Нужно прочитать delim до '(' и затем искать )delim"
        """
        # Уже стоим на '"'
        self._advance(1)  # пропустить открывающую '"'
        # Считать delimiter до '('
        delim_chars = []
        while self.i < self.n:
            c = self._advance_one()
            if c == "(":
                break
            if c == "\n":
                # Неверный raw-литерал, но корректно завершим
                # просто выходим
                return
            delim_chars.append(c)
        delim = ")" + "".join(delim_chars) + '"'
        # Теперь искать окончание: )delim"
        # Идём посимвольно, сравнивая с шаблоном
        match_len = len(delim)
        buffer = []
        while self.i < self.n:
            c = self._advance_one()
            buffer.append(c)
            if len(buffer) > match_len:
                buffer.pop(0)
            if len(buffer) == match_len and "".join(buffer) == delim:
                break

    def _maybe_skip_string_or_char(self):
        """
        Пытается распознать начало строкового/символьного/сырого литерала
        с префиксами u8, u, U, L, а также их комбинациями с R.

        Возвращает True, если что-то распознали и пропустили (сместили i),
        иначе False.
        """
        c0 = self._peek(0)
        c1 = self._peek(1)
        c2 = self._peek(2)
        c3 = self._peek(3)

        # RAW strings: R"  u8R"  uR"  UR"  LR"
        if c0 == "R" and c1 == '"':
            # R"
            self._advance(1)  # R
            self._skip_raw_string_after_prefix()
            return True
        if c0 == "u" and c1 == "8" and c2 == "R" and c3 == '"':
            self._advance(3)  # u8R
            self._skip_raw_string_after_prefix()
            return True
        if c0 == "u" and c1 == "R" and c2 == '"':
            self._advance(2)  # uR
            self._skip_raw_string_after_prefix()
            return True
        if c0 == "U" and c1 == "R" and c2 == '"':
            self._advance(2)  # UR
            self._skip_raw_string_after_prefix()
            return True
        if c0 == "L" and c1 == "R" and c2 == '"':
            self._advance(2)  # LR
            self._skip_raw_string_after_prefix()
            return True

        # Normal strings with prefixes: u8"  u"  U"  L"  and plain "
        if c0 == "u" and c1 == "8" and c2 == '"':
            self._advance(3)  # u8"
            self._skip_normal_string()
            return True
        if c0 == "u" and c1 == '"':
            self._advance(2)  # u"
            self._skip_normal_string()
            return True
        if c0 == "U" and c1 == '"':
            self._advance(2)  # U"
            self._skip_normal_string()
            return True
        if c0 == "L" and c1 == '"':
            self._advance(2)  # L"
            self._skip_normal_string()
            return True
        if c0 == '"':
            self._advance(1)  # "
            self._skip_normal_string()
            return True

        # Char literals: u'  U'  L'  and plain '
        # Но важно не спутать апостроф-разделитель цифр 1'000
        if c0 == "u" and c1 == "'":
            self._advance(2)
            self._skip_char_literal()
            return True
        if c0 == "U" and c1 == "'":
            self._advance(2)
            self._skip_char_literal()
            return True
        if c0 == "L" and c1 == "'":
            self._advance(2)
            self._skip_char_literal()
            return True
        if c0 == "'":
            # Эвристика: если слева цифра и справа цифра/буква, считаем это разделителем цифр, а не символьным литералом
            prevc = self._prev(1)
            nextc = c1
            if prevc.isdigit() and (nextc.isdigit() or nextc.isalpha()):
                # это, вероятнее всего, разделитель цифр в числе
                return False
            self._advance(1)
            self._skip_char_literal()
            return True

        return False

    def analyze(self, text):
        """
        Возвращает словарь с результатами:
        {
          'break': {'count': int, 'lines': set, 'occ': [(line, col, length)]},
          '<<':    {'count': int, 'lines': set, 'occ': [(line, col, length)]},
          '>>':    {'count': int, 'lines': set, 'occ': [(line, col, length)]},
        }
        """
        self.set_text(text)
        res = {
            'break': {'count': 0, 'lines': set(), 'occ': []},
            '<<': {'count': 0, 'lines': set(), 'occ': []},
            '>>': {'count': 0, 'lines': set(), 'occ': []},
        }

        while self.i < self.n:
            c = self._peek(0)
            # Комментарии
            if c == "/":
                if self._peek(1) == "/":
                    self._advance(2)
                    self._skip_line_comment()
                    continue
                elif self._peek(1) == "*":
                    self._advance(2)
                    self._skip_block_comment()
                    continue

            # Строки/символьные литералы (включая Raw)
            if self._maybe_skip_string_or_char():
                continue

            # Идентификаторы
            if c.isalpha() or c == "_":
                start_line, start_col = self.line, self.col
                start_i = self.i
                while self.i < self.n and (self._peek(0).isalnum() or self._peek(0) == "_"):
                    self._advance_one()
                token = self.text[start_i:self.i]
                if token == "break":
                    res['break']['count'] += 1
                    res['break']['lines'].add(start_line)
                    res['break']['occ'].append((start_line, start_col, len("break")))
                continue

            # Операторы << и >> (исключаем <<= и >>=)
            if c == "<" and self._peek(1) == "<":
                if self._peek(2) == "=":
                    self._advance(3)
                else:
                    start_line, start_col = self.line, self.col
                    self._advance(2)
                    res['<<']['count'] += 1
                    res['<<']['lines'].add(start_line)
                    res['<<']['occ'].append((start_line, start_col, 2))
                continue

            if c == ">" and self._peek(1) == ">":
                if self._peek(2) == "=":
                    self._advance(3)
                else:
                    start_line, start_col = self.line, self.col
                    self._advance(2)
                    res['>>']['count'] += 1
                    res['>>']['lines'].add(start_line)
                    res['>>']['occ'].append((start_line, start_col, 2))
                continue

            # Прочие символы и пробелы
            self._advance_one()

        return res


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ЛР №1: Поиск break, << и >> в C++ коде (tkinter)")
        self.geometry("1100x700")

        self._create_widgets()
        self.file_path = None
        self.analyzer = CppAnalyzer()

    def _create_widgets(self):
        # Меню
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Открыть...", command=self.open_file)
        file_menu.add_command(label="Анализировать", command=self.analyze)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)
        self.config(menu=menubar)

        # Панели
        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, padx=8, pady=4)

        btn_open = tk.Button(top_frame, text="Открыть файл", command=self.open_file)
        btn_open.pack(side=tk.LEFT)

        btn_analyze = tk.Button(top_frame, text="Анализировать", command=self.analyze)
        btn_analyze.pack(side=tk.LEFT, padx=6)

        btn_clear = tk.Button(top_frame, text="Очистить результаты/подсветку", command=self.clear_results_and_highlights)
        btn_clear.pack(side=tk.LEFT, padx=6)

        # Основная область: слева код, справа результаты
        main_frame = tk.PanedWindow(self, sashrelief=tk.RAISED, sashwidth=6)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame)
        right_frame = tk.Frame(main_frame, width=340)

        # Текст с кодом
        self.code_text = ScrolledText(left_frame, wrap=tk.NONE, undo=True)
        self.code_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # Результаты
        lbl_res = tk.Label(right_frame, text="Результаты анализа")
        lbl_res.pack(anchor="w", padx=6, pady=(6, 0))

        self.result_text = ScrolledText(right_frame, wrap=tk.WORD, height=10, state=tk.NORMAL)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # Добавляем в панед
        main_frame.add(left_frame, stretch="always")
        main_frame.add(right_frame)

        # Настройка тегов для подсветки
        self.code_text.tag_configure("tag_break", background="#fff3a5", foreground="#000000")   # мягкий жёлтый
        self.code_text.tag_configure("tag_ltlt", background="#c9f1ff", foreground="#000000")     # голубой
        self.code_text.tag_configure("tag_gtgt", background="#f5c9ff", foreground="#000000")     # розово-лиловый

        # Статусбар
        self.status = tk.StringVar(value="Готово")
        status_bar = tk.Label(self, textvariable=self.status, anchor="w", relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def open_file(self):
        path = filedialog.askopenfilename(
            title="Открыть C/C++ файл",
            filetypes=[
                ("C/C++ files", "*.cpp *.cc *.cxx *.hpp *.hh *.h *.hxx"),
                ("All files", "*.*"),
            ]
        )
        if not path:
            return
        # Попробуем несколько кодировок
        encodings_try = ["utf-8-sig", "utf-8", "cp1251", "latin-1"]
        content = None
        for enc in encodings_try:
            try:
                with open(path, "r", encoding=enc, errors="strict") as f:
                    content = f.read()
                break
            except Exception:
                continue
        if content is None:
            # В крайнем случае, читаем с заменой символов
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

        # Показать в текстовом поле
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", content)
        self.file_path = path
        self.status.set(f"Открыт файл: {os.path.basename(path)}")

        # Очистим результаты/подсветку
        self.clear_results_and_highlights()

    def clear_results_and_highlights(self):
        # Снять подсветку
        for tag in ["tag_break", "tag_ltlt", "tag_gtgt"]:
            self.code_text.tag_remove(tag, "1.0", tk.END)
        # Очистить результаты
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.status.set("Готово")

    def analyze(self):
        code = self.code_text.get("1.0", tk.END)
        if not code.strip():
            messagebox.showinfo("Анализ", "Текст пуст. Сначала откройте файл или вставьте код.")
            return

        self.status.set("Анализ...")
        self.update_idletasks()

        result = self.analyzer.analyze(code)

        # Показать результаты
        self._display_results(result)

        # Подсветка совпадений
        self._highlight(result)

        total = result['break']['count'] + result['<<']['count'] + result['>>']['count']
        self.status.set(f"Анализ завершен. Найдено: break={result['break']['count']}, <<={result['<<']['count']}, >>={result['>>']['count']} (итого {total}).")

    def _display_results(self, result):
        def fmt_lines(lines_set):
            if not lines_set:
                return "-"
            return ", ".join(str(x) for x in sorted(lines_set))

        text = []
        text.append("Искомые элементы:")
        text.append(f" - break: количество = {result['break']['count']}, строки: {fmt_lines(result['break']['lines'])}")
        text.append(f" - <<   : количество = {result['<<']['count']}, строки: {fmt_lines(result['<<']['lines'])}")
        text.append(f" - >>   : количество = {result['>>']['count']}, строки: {fmt_lines(result['>>']['lines'])}")
        total = result['break']['count'] + result['<<']['count'] + result['>>']['count']
        text.append(f"\nИтого найдено: {total}")

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", "\n".join(text))
        self.result_text.config(state=tk.DISABLED)

    def _highlight(self, result):
        # Удалить старые теги
        for tag in ["tag_break", "tag_ltlt", "tag_gtgt"]:
            self.code_text.tag_remove(tag, "1.0", tk.END)

        for (ln, col, length) in result['break']['occ']:
            start = f"{ln}.{max(0, col - 1)}"
            end = f"{ln}.{max(0, col - 1 + length)}"
            self.code_text.tag_add("tag_break", start, end)

        for (ln, col, length) in result['<<']['occ']:
            start = f"{ln}.{max(0, col - 1)}"
            end = f"{ln}.{max(0, col - 1 + length)}"
            self.code_text.tag_add("tag_ltlt", start, end)

        for (ln, col, length) in result['>>']['occ']:
            start = f"{ln}.{max(0, col - 1)}"
            end = f"{ln}.{max(0, col - 1 + length)}"
            self.code_text.tag_add("tag_gtgt", start, end)


if __name__ == "__main__":
    app = App()
    app.mainloop()
