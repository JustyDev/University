import tkinter as tk
from math import hypot

# Настройки
WIDTH, HEIGHT = 900, 600
GRID_STEP = 20      # шаг сетки в пикселях canvas
POINT_R = 3         # радиус отображаемой вершины

def dist(a, b):
    return hypot(a[0] - b[0], a[1] - b[1])

# Геометрия для проверки пересечений
def orient(a, b, c):
    # ориентированная площадь*2 (псевдоскаляр): >0 — поворот влево (CCW)
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def on_segment(a, b, p):
    # p лежит на отрезке ab? (при условии коллинеарности)
    return min(a[0], b[0]) - 1e-9 <= p[0] <= max(a[0], b[0]) + 1e-9 and \
           min(a[1], b[1]) - 1e-9 <= p[1] <= max(a[1], b[1]) + 1e-9

def segments_intersect(a, b, c, d):
    # общий тест пересечения (включая касание/коллинеарность)
    o1 = orient(a, b, c)
    o2 = orient(a, b, d)
    o3 = orient(c, d, a)
    o4 = orient(c, d, b)

    if (o1 == 0 and on_segment(a, b, c)) or \
       (o2 == 0 and on_segment(a, b, d)) or \
       (o3 == 0 and on_segment(c, d, a)) or \
       (o4 == 0 and on_segment(c, d, b)):
        return True

    return (o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0)

def line_intersection_point(a, b, c, d):
    # возвращает точку пересечения прямых AB и CD (если не параллельны),
    # не проверяет, что она внутри отрезков — используйте вместе с segments_intersect
    x1, y1 = a; x2, y2 = b; x3, y3 = c; x4, y4 = d
    den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if abs(den) < 1e-12:
        return None
    px = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / den
    py = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / den
    return (px, py)

def shoelace_area_signed(points):
    # ориентированная площадь по формуле Гаусса (shoelace)
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

class App:
    def __init__(self, root):
        self.root = root
        root.title("Периметр и площадь многоугольника")

        # Холст
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Панель справа
        panel = tk.Frame(root, padx=8, pady=8)
        panel.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(panel, text="Управление:").pack(anchor="w")
        self.btn_compute = tk.Button(panel, text="Вычислить", command=self.compute)
        self.btn_compute.pack(fill="x", pady=(2, 6))

        self.btn_close = tk.Button(panel, text="Замкнуть", command=self.toggle_close)
        self.btn_close.pack(fill="x", pady=2)

        self.btn_undo = tk.Button(panel, text="Отменить вершину", command=self.undo_last)
        self.btn_undo.pack(fill="x", pady=2)

        self.btn_clear = tk.Button(panel, text="Очистить", command=self.clear)
        self.btn_clear.pack(fill="x", pady=(2, 10))

        self.grid_var = tk.BooleanVar(value=True)
        self.snap_var = tk.BooleanVar(value=False)
        tk.Checkbutton(panel, text="Сетка", variable=self.grid_var, command=self.redraw).pack(anchor="w")
        tk.Checkbutton(panel, text="Привязка к сетке", variable=self.snap_var).pack(anchor="w", pady=(0, 10))

        # Результаты
        tk.Label(panel, text="Результаты:").pack(anchor="w")
        self.lbl_n = tk.Label(panel, text="Вершин: 0")
        self.lbl_n.pack(anchor="w")
        self.lbl_closed = tk.Label(panel, text="Замкнут: нет")
        self.lbl_closed.pack(anchor="w")
        self.lbl_self = tk.Label(panel, text="Самопересечения: нет")
        self.lbl_self.pack(anchor="w", pady=(0, 6))
        self.lbl_perim = tk.Label(panel, text="Периметр: -")
        self.lbl_perim.pack(anchor="w")
        self.lbl_area = tk.Label(panel, text="Площадь |S|: -")
        self.lbl_area.pack(anchor="w")
        self.lbl_area_signed = tk.Label(panel, text="S (со знаком): -")
        self.lbl_area_signed.pack(anchor="w")
        self.lbl_orient = tk.Label(panel, text="Ориентация: -")
        self.lbl_orient.pack(anchor="w", pady=(0, 10))

        self.hint = tk.Label(panel, text="ЛКМ — добавить вершину\nПКМ — замкнуть/разомкнуть", fg="#555")
        self.hint.pack(anchor="w")

        # Данные многоугольника
        self.points = []        # список (x, y) в координатах canvas
        self.closed = False
        self.intersections = [] # список точек пересечений для отображения

        # События
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)

        self.redraw()

    # ==== Взаимодействие ====
    def on_left_click(self, event):
        x, y = event.x, event.y
        if self.snap_var.get():
            x = round(x / GRID_STEP) * GRID_STEP
            y = round(y / GRID_STEP) * GRID_STEP

        # если многоугольник уже замкнут — начнём новый
        if self.closed:
            self.points = []
            self.closed = False

        self.points.append((x, y))
        self.redraw()

    def on_right_click(self, event):
        self.toggle_close()

    def toggle_close(self):
        if len(self.points) >= 3:
            self.closed = not self.closed
            self.btn_close.config(text="Разомкнуть" if self.closed else "Замкнуть")
            self.redraw()

    def undo_last(self):
        if self.points:
            self.points.pop()
            if len(self.points) < 3:
                self.closed = False
                self.btn_close.config(text="Замкнуть")
            self.redraw()

    def clear(self):
        self.points.clear()
        self.closed = False
        self.btn_close.config(text="Замкнуть")
        self.redraw()

    # ==== Вычисления ====
    def compute(self):
        n = len(self.points)
        self.lbl_n.config(text=f"Вершин: {n}")
        self.lbl_closed.config(text=f"Замкнут: {'да' if self.closed else 'нет'}")

        if n < 3:
            self.lbl_perim.config(text="Периметр: недостаточно вершин")
            self.lbl_area.config(text="Площадь |S|: -")
            self.lbl_area_signed.config(text="S (со знаком): -")
            self.lbl_orient.config(text="Ориентация: -")
            return

        pts = self.points[:]
        # при вычислении считаем, что последняя соединяется с первой
        P = perimeter(pts)
        S_signed = shoelace_area_signed(pts)
        S_abs = abs(S_signed)

        self.lbl_perim.config(text=f"Периметр: {P:.3f} пикс.")
        self.lbl_area.config(text=f"Площадь |S|: {S_abs:.3f} кв. пикс.")
        self.lbl_area_signed.config(text=f"S (со знаком): {S_signed:.3f}")

        if S_signed > 0:
            self.lbl_orient.config(text="Ориентация: против часовой (CCW)")
        elif S_signed < 0:
            self.lbl_orient.config(text="Ориентация: по часовой (CW)")
        else:
            self.lbl_orient.config(text="Ориентация: нулевая площадь")

        # предупреждение о самопересечениях
        self.find_self_intersections()
        if self.intersections:
            self.lbl_self.config(text=f"Самопересечения: да ({len(self.intersections)})", fg="red")
        else:
            self.lbl_self.config(text="Самопересечения: нет", fg="black")

    def find_self_intersections(self):
        self.intersections.clear()
        n = len(self.points)
        if n < 4:
            return
        edges = [(i, (i+1) % n) for i in range(n)]
        for i, (a1, b1) in enumerate(edges):
            for j, (a2, b2) in enumerate(edges):
                if j <= i:
                    continue
                # пропускаем соседние рёбра с общей вершиной
                shared = {a1, b1}.intersection({a2, b2})
                if shared:
                    continue
                # пропустим также пару (первое, последнее) если они соседние
                if (a1 == 0 and b2 == 0) or (b1 == 0 and a2 == 0):
                    pass
                A, B = self.points[a1], self.points[b1]
                C, D = self.points[a2], self.points[b2]
                if segments_intersect(A, B, C, D):
                    p = line_intersection_point(A, B, C, D)
                    if p is not None:
                        self.intersections.append(p)

    # ==== Отрисовка ====
    def draw_grid(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        color = "#f0f0f0"
        for x in range(0, w+1, GRID_STEP):
            self.canvas.create_line(x, 0, x, h, fill=color)
        for y in range(0, h+1, GRID_STEP):
            self.canvas.create_line(0, y, w, y, fill=color)

    def redraw(self):
        self.canvas.delete("all")
        if self.grid_var.get():
            self.draw_grid()

        # Рёбра
        if len(self.points) >= 2:
            for i in range(len(self.points)-1):
                self.canvas.create_line(*self.points[i], *self.points[i+1], fill="black", width=2)
            if self.closed and len(self.points) >= 3:
                self.canvas.create_line(*self.points[-1], *self.points[0], fill="black", width=2)

        # Вершины
        for idx, (x, y) in enumerate(self.points):
            r = POINT_R
            color = "#0077ff" if idx == 0 else "#000000"
            self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=color, fill=color)

        # Пересечения, если уже считали
        if self.intersections:
            for (x, y) in self.intersections:
                self.draw_cross(x, y, size=6, color="red")

        # Обновим краткую сводку
        self.lbl_n.config(text=f"Вершин: {len(self.points)}")
        self.lbl_closed.config(text=f"Замкнут: {'да' if self.closed else 'нет'}")

    def draw_cross(self, x, y, size=6, color="red"):
        self.canvas.create_line(x-size, y-size, x+size, y+size, fill=color, width=2)
        self.canvas.create_line(x-size, y+size, x+size, y-size, fill=color, width=2)

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
