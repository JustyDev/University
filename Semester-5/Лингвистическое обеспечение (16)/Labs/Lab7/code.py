import tkinter as tk
from tkinter import messagebox

# ---------- Лексер ----------
import re

NUM_RE = re.compile(r"""
    (?:
        \d+(?:\.\d*)? |    # 12   12.  12.34
        \.\d+              # .34
    )
    (?:[eE][+-]?\d+)?      # необязательная экспонента
""", re.X)

class CalcError(Exception): pass

def tokenize(s: str):
    tokens = []  # (type, value, pos)
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1; continue
        if c in '+-*/()':
            t = 'OP' if c in '+-*/' else ('LP' if c == '(' else 'RP')
            tokens.append((t, c, i)); i += 1; continue
        if c.isdigit() or c == '.':
            m = NUM_RE.match(s, i)
            if not m: raise CalcError(f"Неверная запись числа на позиции {i+1}")
            val = float(m.group(0))
            tokens.append(('NUM', val, i))
            i = m.end(); continue
        if c.isalpha() or c == '_':
            j = i+1
            while j < n and (s[j].isalnum() or s[j] == '_'): j += 1
            name = s[i:j]
            tokens.append(('ID', name, i))
            i = j; continue
        raise CalcError(f"Недопустимый символ '{c}' на позиции {i+1}")
    tokens.append(('EOF', '', n))
    return tokens

# ---------- Валидация простых ошибок до парсинга ----------
def validate_tokens(tok):
    depth = 0
    prev = None
    for k, t in enumerate(tok[:-1]):  # без EOF
        typ, val, pos = t
        # баланс скобок
        if typ == 'LP':
            depth += 1
            # запретим пустые скобки и * / сразу после '('
            nxt = tok[k+1]
            if nxt[0] == 'RP': raise CalcError("Пустые скобки '()' недопустимы")
            if nxt[0] == 'OP' and nxt[1] in '*/':
                raise CalcError("Недопустимый оператор сразу после '('")
        if typ == 'RP':
            depth -= 1
            if depth < 0: raise CalcError("Лишняя закрывающая скобка")
        # имя функции
        if typ == 'ID':
            if val != 'abs':
                raise CalcError(f"Неизвестная функция '{val}'")
            if tok[k+1][0] != 'LP':
                raise CalcError("После имени функции требуется '('")
        # два оператора подряд
        if typ == 'OP':
            nxt = tok[k+1]
            if nxt[0] == 'OP':
                # допустим унарные +/-, когда перед ними начало/оператор/(
                if nxt[1] in '+-':
                    if k == 0 or prev and prev[0] in ('OP','LP'):
                        pass
                    else:
                        raise CalcError("Два оператора подряд без операнда")
                else:
                    raise CalcError("Два оператора подряд без операнда")
        # отсутствие оператора между значениями/скобками
        if prev and prev[0] in ('NUM','RP') and typ in ('NUM','ID','LP'):
            raise CalcError("Отсутствует оператор между операндами/скобками")
        prev = t
    if depth > 0: raise CalcError("Не хватает закрывающей скобки")
    # начало/конец выражения
    first = tok[0]
    if first[0] == 'OP' and first[1] in '*/':
        raise CalcError("Выражение не может начинаться с '*' или '/'")
    last_non_eof = tok[-2]
    if last_non_eof[0] == 'OP':
        raise CalcError("Выражение не может заканчиваться оператором")

# ---------- Парсер (рекурсивный спуск) ----------
class Parser:
    def __init__(self, tokens):
        self.tok = tokens
        self.i = 0

    def cur(self): return self.tok[self.i]
    def eat(self): self.i += 1

    def parse(self):
        val = self.expr()
        if self.cur()[0] != 'EOF':
            t = self.cur()
            raise CalcError(f"Лишний фрагмент возле позиции {t[2]+1}")
        return val

    # expr = term (('+'|'-') term)*
    def expr(self):
        v = self.term()
        while self.cur()[0] == 'OP' and self.cur()[1] in '+-':
            op = self.cur()[1]; self.eat()
            r = self.term()
            v = v + r if op == '+' else v - r
        return v

    # term = factor (('*'|'/') factor)*
    def term(self):
        v = self.unary()
        while self.cur()[0] == 'OP' and self.cur()[1] in '*/':
            op = self.cur()[1]; self.eat()
            r = self.unary()
            if op == '*':
                v *= r
            else:
                if r == 0: raise CalcError("Деление на ноль")
                v /= r
        return v

    # unary = ('+'|'-') unary | primary
    def unary(self):
        if self.cur()[0] == 'OP' and self.cur()[1] in '+-':
            op = self.cur()[1]; self.eat()
            v = self.unary()
            return v if op == '+' else -v
        return self.primary()

    # primary = NUM | '(' expr ')' | 'abs' '(' expr ')'
    def primary(self):
        t = self.cur()
        if t[0] == 'NUM':
            self.eat(); return t[1]
        if t[0] == 'LP':
            self.eat()
            v = self.expr()
            if self.cur()[0] != 'RP':
                raise CalcError("Ожидалась закрывающая скобка ')'")
            self.eat()
            return v
        if t[0] == 'ID' and t[1] == 'abs':
            self.eat()
            if self.cur()[0] != 'LP':
                raise CalcError("После abs требуется '('")
            self.eat()
            v = self.expr()
            if self.cur()[0] != 'RP':
                raise CalcError("Ожидалась закрывающая скобка для abs")
            self.eat()
            return abs(v)
        raise CalcError(f"Неожиданный фрагмент возле позиции {t[2]+1}")

def evaluate(expr: str) -> float:
    tokens = tokenize(expr)
    validate_tokens(tokens)
    parser = Parser(tokens)
    return parser.parse()

# ---------- UI ----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ЛР №7: Строчный калькулятор (поддержка abs)")
        self.geometry("620x180")
        self.examples = [
            "abs(abs(0.2)+0.1)/2",
            "abs(abs(0.2)+0.1)/(4-2)",
            "abs(abs(0.2)+0.1)(4-2)",     # ошибка: нет оператора
            "abs(abs(0.2)+0.1)/*(4-2)",   # ошибка: два оператора подряд
            "abs(abs(0.2)0.1)*(4-2)",     # ошибка: нет оператора между ) и числом
            "abs(abs(0.2+0.1)*(4-2)",     # ошибка: не хватает ')'
            "abss(abs(0.2)+0.1)*(4-2)"    # ошибка: неизвестная функция
        ]
        self.ex_i = 0
        self.build()

    def build(self):
        frm = tk.Frame(self); frm.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(frm, text="Выражение:").grid(row=0, column=0, sticky="w")
        self.entry = tk.Entry(frm, width=60); self.entry.grid(row=0, column=1, columnspan=3, sticky="we", padx=5)
        tk.Button(frm, text="Вычислить", command=self.calc).grid(row=1, column=1, sticky="we", pady=6)
        tk.Button(frm, text="Очистить", command=self.clear).grid(row=1, column=2, sticky="we")
        tk.Button(frm, text="Пример", command=self.put_example).grid(row=1, column=3, sticky="we")
        self.res = tk.StringVar(value="Ответ: ")
        tk.Label(frm, textvariable=self.res, anchor="w").grid(row=2, column=0, columnspan=4, sticky="we", pady=(8,0))
        frm.grid_columnconfigure(1, weight=1)

    def calc(self):
        expr = self.entry.get().strip()
        if not expr:
            messagebox.showinfo("Калькулятор", "Введите выражение."); return
        try:
            val = evaluate(expr)
            self.res.set(f"Ответ: {val:.2f}  (без округления: {val})")
        except CalcError as e:
            self.res.set(f"Ошибка: {e}")
        except Exception as e:
            self.res.set(f"Ошибка вычисления: {e}")

    def clear(self):
        self.entry.delete(0, tk.END); self.res.set("Ответ: ")

    def put_example(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.examples[self.ex_i])
        self.ex_i = (self.ex_i + 1) % len(self.examples)

if __name__ == "__main__":
    App().mainloop()
