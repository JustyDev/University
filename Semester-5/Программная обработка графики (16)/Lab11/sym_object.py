import tkinter as tk
from tkinter import colorchooser, messagebox
from math import hypot

# Настройки
WIDTH, HEIGHT = 900, 600
POINT_R = 3

def dist(a, b):
    return hypot(a[0] - b[0], a[1] - b[1])

def shoelace_area_signed(points):
    n = len(points)
    s = 0.0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i+1) % n]
        s += x1*y2 - x2*y1
    return 0.5 * s

def perimeter(points):
    n = len(points)
    p = 0.0
    for i in range(n):
        p += dist(points[i], points[(i+1) % n])
    return p

def reflect_point_about_point(P, C):
    x, y = P; cx, cy = C
    return (2*cx - x, 2*cy - y)

def reflect_point_about_line(P, A, B):
    ax, ay = A; bx, by = B; px, py = P
    ux, uy = (bx - ax), (by - ay)
    len2 = ux*ux + uy*uy
    if len2 == 0:
        return P
    apx, apy = (px - ax), (py - ay)
    t = (apx*ux + apy*uy) / len2
    parx, pary = (t*ux, t*uy)
    rx = 2*parx - apx
    ry = 2*pary - apy
    return (ax + rx, ay + ry)

class App:
    def __init__(self, root):
        self.root = root
        root.title("Симметричные отражения фигуры")

        # Холст
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Панель справа
        panel = tk.Frame(root, padx=8, pady=8)
        panel.pack(side=tk.RIGHT, fill=tk.Y)

        # Результаты
        self.lbl_perim = tk.Label(panel, text="Периметр = -")
        self.lbl_perim.pack(fill="x", pady=(0, 2))
        self.lbl_area = tk.Label(panel, text="Площадь = -")
        self.lbl_area.pack(fill="x", pady=(0, 6))

        # Кнопки
        self.btn_close = tk.Button(panel, text="Замкнуть", command=self.toggle_close)
        self.btn_close.pack(fill="x", pady=(0, 6))

        self.fill_color = "#1e8acc"
        self.border_color = "#000000"
        tk.Button(panel, text="Выбрать цвет", command=self.choose_fill_color).pack(fill="x", pady=(0, 8))

        sym_box = tk.LabelFrame(panel, text="Симметрия:", padx=6, pady=6)
        sym_box.pack(fill="x")
        tk.Button(sym_box, text="Относительно точки", command=self.start_sym_point).pack(fill="x", pady=2)
        tk.Button(sym_box, text="Относительно линии", command=self.start_sym_line).pack(fill="x", pady=2)

        tk.Button(panel, text="Очистить", command=self.clear_all).pack(fill="x", pady=(10, 0))

        # Подсказка
        self.status = tk.Label(panel, text="ЛКМ — добавить вершину; ПКМ — замкнуть/разомкнуть", fg="#555")
        self.status.pack(anchor="w", pady=(8, 0))

        # Данные
        self.points = []
        self.closed = False

        # Для отображения “следа” и линии
        self.prev_points = None       # предыдущая фигура (для полупрозрачного вывода)
        self.last_line = None         # (A, B) — последняя линия отражения
        self.last_sym_point = None    # точка симметрии (для маркера)

        # Режимы ввода
        self.mode = None              # None | 'sym_point' | 'sym_line_first' | 'sym_line_second'
        self.sym_point = None
        self.line_first = None

        # События
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)

        self.redraw()

    # ---------- UI ----------
    def choose_fill_color(self):
        color = colorchooser.askcolor(self.fill_color, title="Цвет заливки")[1]
        if color:
            self.fill_color = color
            if self.closed:
                self.redraw()

    def clear_all(self):
        self.points = []
        self.closed = False
        self.prev_points = None
        self.last_line = None
        self.last_sym_point = None
        self.mode = None
        self.line_first = None
        self.sym_point = None
        self.btn_close.config(text="Замкнуть")
        self.status.config(text="ЛКМ — добавить вершину; ПКМ — замкнуть/разомкнуть")
        self.redraw()

    def start_sym_point(self):
        if not (self.closed and len(self.points) >= 3):
            messagebox.showinfo("Симметрия", "Замкните многоугольник (не менее 3 вершин).")
            return
        self.mode = 'sym_point'
        self.sym_point = None
        self.line_first = None
        self.status.config(text="Кликните точку — симметрия относительно точки")

    def start_sym_line(self):
        if not (self.closed and len(self.points) >= 3):
            messagebox.showinfo("Симметрия", "Замкните многоугольник (не менее 3 вершин).")
            return
        self.mode = 'sym_line_first'
        self.line_first = None
        self.sym_point = None
        self.status.config(text="Кликните 1-ю точку линии")

    def on_left_click(self, event):
        x, y = event.x, event.y

        # Ввод для симметрии
        if self.mode == 'sym_point':
            self.sym_point = (x, y)
            self.prev_points = self.points[:]          # сохранить прошлое положение
            self.last_sym_point = self.sym_point
            self.last_line = None
            self.reflect_about_point(self.sym_point)
            self.mode = None
            self.status.config(text="Отражение выполнено. ПКМ — разомкнуть; кнопки — новая симметрия")
            return

        if self.mode == 'sym_line_first':
            self.line_first = (x, y)
            self.mode = 'sym_line_second'
            self.status.config(text="Кликните 2-ю точку линии")
            self.redraw()
            return

        if self.mode == 'sym_line_second':
            if self.line_first is None:
                self.mode = None
                return
            A = self.line_first
            B = (x, y)
            if A == B:
                messagebox.showwarning("Симметрия", "Две точки линии совпадают. Укажите разные точки.")
                return
            self.prev_points = self.points[:]
            self.last_line = (A, B)
            self.last_sym_point = None
            self.reflect_about_line(A, B)
            self.mode = None
            self.line_first = None
            self.status.config(text="Отражение выполнено. ПКМ — разомкнуть; кнопки — новая симметрия")
            return

        # Обычный набор вершин
        if not self.closed:
            self.points.append((x, y))
            self.redraw()

    def on_right_click(self, event):
        self.toggle_close()

    def toggle_close(self):
        if len(self.points) < 3 and not self.closed:
            messagebox.showinfo("Замкнуть", "Нужно как минимум 3 вершины.")
            return
        self.closed = not self.closed
        self.btn_close.config(text="Разомкнуть" if self.closed else "Замкнуть")
        # сброс режимов и вспомогательных маркеров
        self.mode = None
        self.line_first = None
        self.sym_point = None
        self.status.config(text="ЛКМ — добавить вершину; ПКМ — замкнуть/разомкнуть")
        self.redraw()

    # ---------- Симметрии ----------
    def reflect_about_point(self, C):
        if not (self.closed and len(self.points) >= 3):
            return
        self.points = [reflect_point_about_point(P, C) for P in self.points]
        self.redraw()

    def reflect_about_line(self, A, B):
        if not (self.closed and len(self.points) >= 3):
            return
        self.points = [reflect_point_about_line(P, A, B) for P in self.points]
        self.redraw()

    # ---------- Расчёты ----------
    def update_metrics(self):
        if self.closed and len(self.points) >= 3:
            P = perimeter(self.points)
            S = abs(shoelace_area_signed(self.points))
            self.lbl_perim.config(text=f"Периметр = {int(round(P))}")
            self.lbl_area.config(text=f"Площадь = {int(round(S))}")
        else:
            self.lbl_perim.config(text="Периметр = -")
            self.lbl_area.config(text="Площадь = -")

    # ---------- Отрисовка ----------
    def redraw(self):
        self.canvas.delete("all")

        # 1) Полупрозрачный “след” прошлой фигуры (если есть)
        if self.prev_points and len(self.prev_points) >= 3:
            flat_prev = [coord for pt in self.prev_points for coord in pt]
            # имитация прозрачности через stipple
            self.canvas.create_polygon(
                *flat_prev, fill=self.fill_color, stipple="gray50",
                outline="#666666", width=2, dash=(5, 4), joinstyle="round"
            )

        # 2) Текущая фигура
        if not self.closed:
            if len(self.points) >= 2:
                for i in range(len(self.points) - 1):
                    self.canvas.create_line(*self.points[i], *self.points[i+1],
                                            fill=self.border_color, width=3)
            for idx, (x, y) in enumerate(self.points):
                r = POINT_R
                color = "#0077ff" if idx == 0 else "#000000"
                self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=color, fill=color)
        else:
            flat = [coord for pt in self.points for coord in pt]
            self.canvas.create_polygon(
                *flat, fill=self.fill_color, outline=self.border_color,
                width=4, joinstyle="round"
            )

        # 3) Последняя линия отражения (если есть) — поверх
        if self.last_line:
            (ax, ay), (bx, by) = self.last_line
            self.canvas.create_line(ax, ay, bx, by, fill="#cc00cc", width=3, dash=(8, 4))
            # маленькие маркеры точек линии
            for (x, y) in (self.last_line[0], self.last_line[1]):
                r = 3
                self.canvas.create_oval(x-r, y-r, x+r, y+r, outline="#cc00cc", fill="#cc00cc")

        # 4) Маркер последней точки симметрии (если была симметрия от точки)
        if self.last_sym_point:
            x, y = self.last_sym_point
            self._cross(x, y, size=6, color="#cc00cc")

        self.update_metrics()

    def _cross(self, x, y, size=6, color="red"):
        self.canvas.create_line(x-size, y-size, x+size, y+size, fill=color, width=2)
        self.canvas.create_line(x-size, y+size, x+size, y-size, fill=color, width=2)

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
