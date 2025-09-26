import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import os
import re

TYPE_WORDS = {
    "void","bool","char","short","int","long","float","double",
    "signed","unsigned","size_t","wchar_t","char16_t","char32_t","auto",
    "const","volatile","struct","class","typename"
}
DECL_SKIP_KW = {"const","volatile","constexpr","static","inline","register","thread_local","mutable"}

def remove_block_comments(text: str) -> str:
    return re.sub(r"/\*.*?\*/", lambda m: " " * (m.end()-m.start()), text, flags=re.S)

def remove_line_comments(text: str) -> str:
    def repl(m):
        s = m.group(0)
        return " " * len(s)
    return re.sub(r"//[^\n]*", repl, text)

def join_backslash_lines(text: str) -> str:
    out = []
    buf = ""
    for line in text.splitlines(True):  # keepends
        if buf:
            buf += line
        else:
            buf = line
        # if line ends with backslash before newline
        # handle Windows \r\n too
        stripped = buf.rstrip("\r\n")
        if stripped.endswith("\\"):
            # remove the trailing backslash and continue
            buf = stripped[:-1]
            continue
        out.append(buf)
        buf = ""
    if buf:
        out.append(buf)
    return "".join(out)

def sanitize_for_decls(code: str) -> str:
    # склеиваем многострочные макросы, вычищаем комментарии и строки, оставляя пробелы/длины чтобы индексы не плыли
    code = join_backslash_lines(code)
    code = remove_block_comments(code)
    code = remove_line_comments(code)
    # удаляем строковые и символьные литералы, заменяя их пробелами той же длины
    def wipe_strings(s: str) -> str:
        i, n = 0, len(s)
        out = list(s)
        def wipe(a,b):
            for k in range(a,b):
                out[k] = " "
        while i < n:
            c = s[i]
            # raw strings: R"..." and u8R"..." etc.
            if c in "uUL" and i+1 < n:
                if s[i:i+3] == "u8R" and i+3<n and s[i+3] == '"':
                    # move to R"
                    i += 2  # now at 'R'
                elif s[i:i+2] in ("uR","UR","LR") and i+2<n and s[i+2] == '"':
                    i += 1
            if s[i:i+2] == 'R"':
                a = i
                i += 2
                # read delimiter up to '('
                while i < n and s[i] != "(":
                    i += 1
                if i >= n:
                    break
                i += 1  # skip '('
                # find )delim"
                # need to find the matching ) then delimiter then "
                # build delimiter from preceding chars
                # go back to get delim
                j = a+2
                delim = []
                while j < n and s[j] != "(":
                    delim.append(s[j]); j += 1
                endseq = ")" + "".join(delim) + '"'
                # scan until endseq
                k = i
                while k < n and s[k:k+len(endseq)] != endseq:
                    k += 1
                if k < n:
                    k += len(endseq)
                    wipe(a,k)
                    i = k
                    continue
                else:
                    # unterminated
                    wipe(a,n); i = n; break
            if c in ('"', "'"):
                a = i
                q = c
                i += 1
                esc = False
                while i < n:
                    ch = s[i]
                    i += 1
                    if esc:
                        esc = False
                        continue
                    if ch == "\\":
                        esc = True
                        continue
                    if ch == q:
                        break
                wipe(a, i)
                continue
            i += 1
        return "".join(out)
    code = wipe_strings(code)
    return code

def split_declarators(s: str):
    parts = []
    cur = []
    depth_par = depth_br = depth_brace = 0
    for ch in s:
        if ch == ',' and depth_par == 0 and depth_br == 0 and depth_brace == 0:
            part = "".join(cur).strip()
            if part:
                parts.append(part)
            cur = []
            continue
        if ch == '(':
            depth_par += 1
        elif ch == ')':
            depth_par = max(0, depth_par-1)
        elif ch == '[':
            depth_br += 1
        elif ch == ']':
            depth_br = max(0, depth_br-1)
        elif ch == '{':
            depth_brace += 1
        elif ch == '}':
            depth_brace = max(0, depth_brace-1)
        cur.append(ch)
    part = "".join(cur).strip()
    if part:
        parts.append(part)
    return parts

def extract_name_from_declarator(decl: str):
    # ищем первый идентификатор, пропуская служебные слова
    for m in re.finditer(r"[A-Za-z_]\w*", decl):
        name = m.group(0)
        if name in DECL_SKIP_KW:
            continue
        # кандидат найден
        end = m.end()
        # проверим: это не функция?
        j = end
        while j < len(decl) and decl[j].isspace():
            j += 1
        if j < len(decl) and decl[j] == '(':
            # найти парную ')'
            k = j + 1
            depth = 1
            while k < len(decl) and depth:
                if decl[k] == '(':
                    depth += 1
                elif decl[k] == ')':
                    depth -= 1
                k += 1
            inside = decl[j+1:k-1] if k-1 >= j+1 else ""
            if inside.strip() == "":
                return None  # пустые () — точно функция
            # если внутри есть слова-типы — считаем это прототипом функции
            if re.search(r"\b(" + "|".join(TYPE_WORDS) + r")\b", inside):
                return None
            # иначе это, вероятно, прямая инициализация переменной
            return name
        return name
    return None

def collect_variables_to_rename(code: str):
    sanitized = sanitize_for_decls(code)
    mapping = {}
    # исключим typedef-блоки: простая эвристика — если слева от int/long есть слово typedef в той же строке, пропускаем
    for base, prefix, pattern in [
        ("int",  "i", r"(?<!\w)int(?!\s+long)\s+([^;]*);"),
        ("long", "l", r"(?<!\w)long(?!\s+long)\s+([^;]*);"),
    ]:
        for m in re.finditer(pattern, sanitized):
            start_line_idx = sanitized.rfind("\n", 0, m.start()) + 1
            line = sanitized[start_line_idx: sanitized.find("\n", m.start()) if sanitized.find("\n", m.start())!=-1 else len(sanitized)]
            if re.search(r"\btypedef\b", line):
                continue
            declarators = split_declarators(m.group(1))
            for decl in declarators:
                name = extract_name_from_declarator(decl)
                if not name:
                    continue
                if name == "main":
                    continue
                # не переименовываем уже "венгерские" имена? По примеру — всё равно добавляем префикс
                new_name = prefix + name
                if name not in mapping:
                    mapping[name] = new_name
    return mapping

# ---------- Замена идентификаторов вне комментариев и строк ----------

def replace_identifiers(code: str, mapping: dict) -> str:
    if not mapping:
        return code
    i, n = 0, len(code)
    out = []
    def peek(k=0):
        j = i + k
        return code[j] if j < n else ""
    while i < n:
        c = code[i]
        # line comment
        if c == "/" and peek(1) == "/":
            j = i + 2
            while j < n and code[j] != "\n":
                j += 1
            out.append(code[i:j]); i = j
            continue
        # block comment
        if c == "/" and peek(1) == "*":
            j = i + 2
            while j < n-1 and not (code[j] == "*" and code[j+1] == "/"):
                j += 1
            j = min(n, j+2)
            out.append(code[i:j]); i = j
            continue
        # raw strings
        if c in "uUL" and i+1 < n:
            if code[i:i+3] == "u8R" and i+3<n and code[i+3] == '"':
                # handle as R""
                # emit as-is
                out.append(code[i:i+3]); i += 3; c = code[i]
            elif code[i:i+2] in ("uR","UR","LR") and i+2<n and code[i+2] == '"':
                out.append(code[i:i+2]); i += 2; c = code[i]
        if code[i:i+2] == 'R"':
            # read delimiter up to '('
            a = i
            i += 2
            while i < n and code[i] != "(":
                i += 1
            if i >= n:
                out.append(code[a:]); i = n; break
            i += 1
            # build endseq
            j = a+2
            delim = []
            while j < n and code[j] != "(":
                delim.append(code[j]); j += 1
            endseq = ")" + "".join(delim) + '"'
            # scan to end
            k = i
            while k < n and code[k:k+len(endseq)] != endseq:
                k += 1
            if k < n:
                k += len(endseq)
                out.append(code[a:k]); i = k
                continue
            else:
                out.append(code[a:]); i = n; break
        # normal strings and chars
        if c in ('"', "'"):
            q = c
            j = i + 1
            esc = False
            while j < n:
                ch = code[j]; j += 1
                if esc:
                    esc = False
                    continue
                if ch == "\\":
                    esc = True
                    continue
                if ch == q:
                    break
            out.append(code[i:j]); i = j
            continue
        # identifier
        if (c.isalpha() or c == "_"):
            j = i + 1
            while j < n and (code[j].isalnum() or code[j] == "_"):
                j += 1
            ident = code[i:j]
            if ident in mapping:
                out.append(mapping[ident])
            else:
                out.append(ident)
            i = j
            continue
        # other
        out.append(c); i += 1
    return "".join(out)

# --------------- UI ----------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ЛР №5: Перевод идентификаторов (int, long) в «венгерскую запись»")
        self.geometry("1100x700")
        self._build_ui()
        self.file_path = None
        self.last_mapping = {}

    def _build_ui(self):
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=8, pady=6)

        tk.Button(top, text="Открыть C++ файл", command=self.open_file).pack(side=tk.LEFT)
        tk.Button(top, text="Преобразовать", command=self.transform).pack(side=tk.LEFT, padx=6)
        tk.Button(top, text="Сохранить результат как...", command=self.save_result).pack(side=tk.LEFT, padx=6)
        tk.Button(top, text="Очистить", command=self.clear_all).pack(side=tk.LEFT, padx=6)
        tk.Button(top, text="Вставить пример", command=self.insert_example).pack(side=tk.LEFT, padx=6)

        pan = tk.PanedWindow(self, sashrelief=tk.RAISED, sashwidth=6)
        pan.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(pan)
        right = tk.Frame(pan, width=420)

        tk.Label(left, text="Исходный код").pack(anchor="w", padx=6, pady=(6,0))
        self.src = ScrolledText(left, wrap=tk.NONE, undo=True)
        self.src.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        tk.Label(right, text="Результат / Переименования").pack(anchor="w", padx=6, pady=(6,0))
        self.dst = ScrolledText(right, wrap=tk.NONE, state=tk.DISABLED)
        self.dst.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

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
        self.src.delete("1.0", tk.END)
        self.src.insert("1.0", content)
        self.file_path = path
        self.status.set(f"Открыт файл: {os.path.basename(path)}")
        self._set_dst("")

    def transform(self):
        code = self.src.get("1.0", tk.END)
        if not code.strip():
            messagebox.showinfo("Преобразование", "Текст пуст. Откройте файл или вставьте код.")
            return
        mapping = collect_variables_to_rename(code)
        self.last_mapping = mapping
        new_code = replace_identifiers(code, mapping)
        # Показ результата + список переименований
        lines = []
        lines.append("Переименования (тип int -> префикс 'i', тип long -> префикс 'l'):")
        if mapping:
            for k in sorted(mapping):
                lines.append(f"  {k} -> {mapping[k]}")
        else:
            lines.append("  (ничего не найдено)")
        lines.append("\n===== Результат =====\n")
        lines.append(new_code)
        self._set_dst("\n".join(lines))
        self.status.set(f"Готово. Переименовано идентификаторов: {len(mapping)}")

    def save_result(self):
        text = self.dst.get("1.0", tk.END)
        if not text.strip():
            messagebox.showinfo("Сохранение", "Результат пуст.")
            return
        path = filedialog.asksaveasfilename(
            title="Сохранить результат",
            defaultextension=".cpp",
            filetypes=[("C/C++ files", "*.cpp *.cc *.cxx *.hpp *.hh *.h *.hxx"), ("All files", "*.*")]
        )
        if not path:
            return
        # Если в правом поле есть служебная часть, можно сохранить только код.
        # Для простоты сохраним всё, как показано.
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        self.status.set(f"Сохранено: {os.path.basename(path)}")

    def clear_all(self):
        self.src.delete("1.0", tk.END)
        self._set_dst("")
        self.status.set("Готово")
        self.last_mapping = {}

    def insert_example(self):
        example = """\
#include <iostream>
#include <vector>
using namespace std;

int i, mas[100], j;   // массив и два int
long L, *p, &ref = L; // несколько long

int main() {
    int a = 1, *b = &a, c(5);
    long len = 10, arr[3] = {1,2,3};
    for (int k = 0; k < 3; ++k) {
        a += k;
    }
    // unsigned не мешает (будет отнесён к int/long)
    unsigned int ui = 7;
    unsigned long ul = 42;

    cout << mas[j] << a << c << len << ref << ui << ul << endl;

    // Функции и прототипы не должны переименовываться:
    // int f(int x); // прототип
    return 0;
}
"""
        self.src.delete("1.0", tk.END)
        self.src.insert("1.0", example)
        self._set_dst("")
        self.status.set("Пример вставлен")

    def _set_dst(self, s: str):
        self.dst.config(state=tk.NORMAL)
        self.dst.delete("1.0", tk.END)
        self.dst.insert("1.0", s)
        self.dst.config(state=tk.DISABLED)

if __name__ == "__main__":
    App().mainloop()
