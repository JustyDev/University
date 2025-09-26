import tkinter as tk
from tkinter import colorchooser, messagebox
from math import hypot

# Настройки
WIDTH, HEIGHT = 900, 600
GRID_STEP = 20      # шаг сетки в пикселях canvas
POINT_R = 3         # радиус отображаемой вершины

def dist(a, b):
    return hypot(a[0] - b[0], a[1] - b[1])

# Геометрия для проверки пересечений (как в 6-й лабе)
def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def on_segment(a, b, p):
    return min(a[0], b[0]) - 1e-9 <= p[0] <= max(a[0], b[0]) + 1e-9 and \
           min(a[1], b[1]) - 1e-9 <= p[1] <= max(a[1], b[1]) + 1e-9

def segments_intersect(a, b, c, d):
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
    x1, y1 = a; x2, y2 = b; x3, y3 = c; x4, y4 = d
    den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if abs(den) < 1e-12:
        return None
    px = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / den
    py = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / den
    return (px, py)

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

def point_in_polygon(pt, poly):
    # классический ray-casting (чётно-нечётное правило)
    x, y = pt
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % n]
        # проверяем пересечение горизонтального луча вправо с ребром
        if ((y1 > y) != (y2 > y)):
            x_int = (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1
            if x_int > x:
                inside = not inside
    return inside

class App:
    def __init__(self, root):
        self.root = root
        root.title("Периметр/площадь + закраска (на основе 6-й лабы)")

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

        # Новое: цвета и заполнение
        color_frame = tk.LabelFrame(panel, text="Цвета", padx=6, pady=6)
        color_frame.pack(fill="x", pady=(4, 6))
        self.border_color = "#000000"
        self.fill_color = "#8a2be2"
        self.bg_color = "#ffffff"

        tk.Button(color_frame, text="Цвет контура", command=self.choose_border_color).pack(fill="x", pady=2)
        self.border_preview = tk.Canvas(color_frame, width=40, height=16, bg=self.border_color, highlightthickness=1, highlightbackground="#aaa")
        self.border_preview.pack(pady=(0, 4))

        tk.Button(color_frame, text="Цвет заливки", command=self.choose_fill_color).pack(fill="x", pady=2)
        self.fill_preview = tk.Canvas(color_frame, width=40, height=16, bg=self.fill_color, highlightthickness=1, highlightbackground="#aaa")
        self.fill_preview.pack(pady=(0, 4))

        # Режимы закраски
        fill_frame = tk.LabelFrame(panel, text="Заполнение", padx=6, pady=6)
        fill_frame.pack(fill="x", pady=(2, 8))

        self.fill_mode = tk.StringVar(value="seed")  # seed | boundary
        tk.Radiobutton(fill_frame, text="По затравке", variable=self.fill_mode, value="seed").pack(anchor="w")
        tk.Radiobutton(fill_frame, text="По границе", variable=self.fill_mode, value="boundary").pack(anchor="w")

        self.conn_var = tk.IntVar(value=4)  # 4 или 8
        conn_row = tk.Frame(fill_frame)
        conn_row.pack(anchor="w", pady=(4, 2))
        tk.Label(conn_row, text="Связность:").pack(side=tk.LEFT)
        tk.Radiobutton(conn_row, text="4", variable=self.conn_var, value=4).pack(side=tk.LEFT)
        tk.Radiobutton(conn_row, text="8", variable=self.conn_var, value=8).pack(side=tk.LEFT)

        self.btn_fill = tk.Button(fill_frame, text="Заполнить", command=self.fill_action)
        self.btn_fill.pack(fill="x", pady=(4, 2))

        self.lbl_seed = tk.Label(fill_frame, text="Затравка: не задана")
        self.lbl_seed.pack(anchor="w")

        # Настройки сетки
        self.grid_var = tk.BooleanVar(value=True)
        self.snap_var = tk.BooleanVar(value=False)
        tk.Checkbutton(panel, text="Сетка", variable=self.grid_var, command=lambda: self.redraw(False)).pack(anchor="w")
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

        self.hint = tk.Label(panel, text="ЛКМ — добавить вершину\nShift+ЛКМ — затравка\nПКМ — замкнуть/разомкнуть", fg="#555")
        self.hint.pack(anchor="w")

        # Данные многоугольника
        self.points = []
        self.closed = False
        self.intersections = []

        # Затравка
        self.seed = None  # (x, y) в координатах канвы

        # Растровый слой для закраски/границ
        self.img = None
        self.img_item = None

        # События
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Shift-Button-1>", self.on_shift_left_click)  # задать затравку
        self.canvas.bind("<Button-3>", self.on_right_click)

        self.redraw(True)

    # ===== Цвета =====
    def choose_border_color(self):
        color = colorchooser.askcolor(self.border_color, title="Выберите цвет контура")[1]
        if color:
            self.border_color = color
            self.border_preview.configure(bg=color)
            self.redraw(True)  # перерисуем границы в растровый слой

    def choose_fill_color(self):
        color = colorchooser.askcolor(self.fill_color, title="Выберите цвет заливки")[1]
        if color:
            self.fill_color = color
            self.fill_preview.configure(bg=color)

    # ===== Взаимодействие =====
    def on_left_click(self, event):
        # добавляем вершину
        x, y = event.x, event.y
        if self.snap_var.get():
            x = round(x / GRID_STEP) * GRID_STEP
            y = round(y / GRID_STEP) * GRID_STEP

        if self.closed:  # начинаем новый многоугольник
            self.points = []
            self.closed = False

        self.points.append((x, y))
        self.redraw(True)

    def on_shift_left_click(self, event):
        x, y = event.x, event.y
        self.seed = (int(x), int(y))
        self.lbl_seed.config(text=f"Затравка: ({self.seed[0]}, {self.seed[1]})")
        self.redraw(False)

    def on_right_click(self, event):
        self.toggle_close()

    def toggle_close(self):
        if len(self.points) >= 3:
            self.closed = not self.closed
            self.btn_close.config(text="Разомкнуть" if self.closed else "Замкнуть")
            self.redraw(True)

    def undo_last(self):
        if self.points:
            self.points.pop()
            if len(self.points) < 3:
                self.closed = False
                self.btn_close.config(text="Замкнуть")
            self.redraw(True)

    def clear(self):
        self.points.clear()
        self.closed = False
        self.btn_close.config(text="Замкнуть")
        self.seed = None
        self.lbl_seed.config(text="Затравка: не задана")
        self.redraw(True)

    # ===== Вычисления (как в 6-й) =====
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
                if {a1, b1}.intersection({a2, b2}):
                    continue
                A, B = self.points[a1], self.points[b1]
                C, D = self.points[a2], self.points[b2]
                if segments_intersect(A, B, C, D):
                    p = line_intersection_point(A, B, C, D)
                    if p is not None:
                        self.intersections.append(p)

    # ===== Растровый слой =====
    def ensure_image(self):
        if self.img is None:
            self.img = tk.PhotoImage(width=WIDTH, height=HEIGHT)
        # очистка изображения цветом фона
        self.img.put(self.bg_color, to=(0, 0, WIDTH, HEIGHT))

    def put_px(self, x, y, color):
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            self.img.put(color, to=(x, y, x+1, y+1))

    def get_px(self, x, y):
        if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
            return None
        val = self.img.get(x, y)
        if isinstance(val, tuple):
            return val  # (r,g,b)
        if isinstance(val, str) and val.startswith("#") and len(val) == 7:
            r = int(val[1:3], 16); g = int(val[3:5], 16); b = int(val[5:7], 16)
            return (r, g, b)
        return val

    def draw_line_on_image(self, x0, y0, x1, y1, color):
        # целочисленный Брезенхем
        x0 = int(round(x0)); y0 = int(round(y0))
        x1 = int(round(x1)); y1 = int(round(y1))
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.put_px(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    # ===== Перерисовка =====
    def draw_grid(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        color = "#f0f0f0"
        for x in range(0, w+1, GRID_STEP):
            self.canvas.create_line(x, 0, x, h, fill=color)
        for y in range(0, h+1, GRID_STEP):
            self.canvas.create_line(0, y, w, y, fill=color)

    def redraw(self, geometry_changed: bool):
        # Сохраняем/пересоздаём растровый слой
        if self.img is None or geometry_changed:
            self.ensure_image()
            # заново прорисуем границу многоугольника в растровом изображении
            if len(self.points) >= 2:
                for i in range(len(self.points)-1):
                    x1, y1 = self.points[i]
                    x2, y2 = self.points[i+1]
                    self.draw_line_on_image(x1, y1, x2, y2, self.border_color)
                if self.closed and len(self.points) >= 3:
                    x1, y1 = self.points[-1]
                    x2, y2 = self.points[0]
                    self.draw_line_on_image(x1, y1, x2, y2, self.border_color)

        # Полная перерисовка слоёв Canvas
        self.canvas.delete("all")
        # сначала растровый слой
        self.img_item = self.canvas.create_image(0, 0, anchor="nw", image=self.img)

        # сетка (по желанию)
        if self.grid_var.get():
            self.draw_grid()

        # векторные рёбра (как в 6-й)
        if len(self.points) >= 2:
            for i in range(len(self.points)-1):
                self.canvas.create_line(*self.points[i], *self.points[i+1], fill=self.border_color, width=2)
            if self.closed and len(self.points) >= 3:
                self.canvas.create_line(*self.points[-1], *self.points[0], fill=self.border_color, width=2)

        # вершины
        for idx, (x, y) in enumerate(self.points):
            r = POINT_R
            color = "#0077ff" if idx == 0 else "#000000"
            self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=color, fill=color)

        # точки самопересечений (если считали)
        if self.intersections:
            for (x, y) in self.intersections:
                self.draw_cross(x, y, size=6, color="red")

        # затравка
        if self.seed is not None:
            self.draw_cross(self.seed[0], self.seed[1], size=5, color="#cc00cc")

        # краткая сводка
        self.lbl_n.config(text=f"Вершин: {len(self.points)}")
        self.lbl_closed.config(text=f"Замкнут: {'да' if self.closed else 'нет'}")

    def draw_cross(self, x, y, size=6, color="red"):
        self.canvas.create_line(x-size, y-size, x+size, y+size, fill=color, width=2)
        self.canvas.create_line(x-size, y+size, x+size, y-size, fill=color, width=2)

    # ===== Заполнение =====
    def fill_action(self):
        if len(self.points) < 3 or not self.closed:
            messagebox.showwarning("Заполнение", "Многоугольник должен быть замкнут и иметь >= 3 вершин.")
            return

        # если затравка не задана — попробуем взять центр масс вершин
        if self.seed is None:
            cx = int(round(sum(x for x, _ in self.points) / len(self.points)))
            cy = int(round(sum(y for _, y in self.points) / len(self.points)))
            # скорректируем, если вдруг вне многоугольника
            if not point_in_polygon((cx, cy), self.points):
                # пройдём небольшой поиск вокруг центра
                found = False
                for r in range(0, 50):
                    for dx in (-r, 0, r):
                        for dy in (-r, 0, r):
                            x = cx + dx; y = cy + dy
                            if 0 <= x < WIDTH and 0 <= y < HEIGHT and point_in_polygon((x, y), self.points):
                                self.seed = (x, y)
                                found = True
                                break
                        if found:
                            break
                    if found:
                        break
                if not found:
                    messagebox.showinfo("Заполнение", "Не удалось подобрать точку внутри. Укажите затравку Shift+ЛКМ.")
                    return
            else:
                self.seed = (cx, cy)
            self.lbl_seed.config(text=f"Затравка: ({self.seed[0]}, {self.seed[1]})")

        # обязательно: перерисуем контуры в растровом слое (вдруг менялся цвет/геометрия)
        self.redraw(True)

        if self.fill_mode.get() == "seed":
            self.flood_fill_seed(self.seed[0], self.seed[1], self.conn_var.get())
        else:
            self.flood_fill_boundary(self.seed[0], self.seed[1], self.conn_var.get())

        # отобразим результат (не сбрасывая растровый слой)
        self.redraw(False)

    def flood_fill_seed(self, sx, sy, connectivity=4):
        # Заполнение по затравке: заливаем область цвета начального пикселя
        target = self.get_px(sx, sy)
        if target is None:
            return
        fill_rgb = self._rgb(self.fill_color)
        border_rgb = self._rgb(self.border_color)
        if target == fill_rgb or target == border_rgb:
            return

        stack = [(sx, sy)]
        while stack:
            x, y = stack.pop()
            # найдём пределы слева и справа для текущей строки
            x_left = x
            while x_left >= 0:
                c = self.get_px(x_left, y)
                if c != target:
                    break
                x_left -= 1
            x_left += 1

            x_right = x
            while x_right < WIDTH:
                c = self.get_px(x_right, y)
                if c != target:
                    break
                x_right += 1
            x_right -= 1

            # закрасим горизонтальный отрезок
            for xi in range(x_left, x_right + 1):
                self.put_px(xi, y, self.fill_color)

            # проверим верхнюю и нижнюю строки — добавим новые затравки сегментами
            for ny in (y - 1, y + 1):
                if ny < 0 or ny >= HEIGHT:
                    continue
                xi = x_left
                while xi <= x_right:
                    c = self.get_px(xi, ny)
                    if c == target:
                        # новый сегмент
                        sx2 = xi
                        while xi <= x_right and self.get_px(xi, ny) == target:
                            xi += 1
                        stack.append((sx2, ny))
                    xi += 1

    def flood_fill_boundary(self, sx, sy, connectivity=4):
        # Заполнение по границе: заполняем, пока не встретим цвет границы
        fill_rgb = self._rgb(self.fill_color)
        border_rgb = self._rgb(self.border_color)

        def fillable(x, y):
            c = self.get_px(x, y)
            return c is not None and c != border_rgb and c != fill_rgb

        if not fillable(sx, sy):
            return

        stack = [(sx, sy)]
        while stack:
            x, y = stack.pop()

            # расширяем влево
            x_left = x
            while x_left >= 0 and fillable(x_left, y):
                x_left -= 1
            x_left += 1

            # расширяем вправо
            x_right = x
            while x_right < WIDTH and fillable(x_right, y):
                x_right += 1
            x_right -= 1

            # закрашиваем найденный горизонтальный отрезок
            for xi in range(x_left, x_right + 1):
                self.put_px(xi, y, self.fill_color)

            # проверяем соседние строки
            for ny in (y - 1, y + 1):
                if ny < 0 or ny >= HEIGHT:
                    continue
                # для 8-связности расширим диапазон на 1 в обе стороны
                start = max(0, x_left - (1 if connectivity == 8 else 0))
                end = min(WIDTH - 1, x_right + (1 if connectivity == 8 else 0))
                xi = start
                while xi <= end:
                    if fillable(xi, ny):
                        sx2 = xi
                        while xi <= end and fillable(xi, ny):
                            xi += 1
                        stack.append((sx2, ny))
                    xi += 1

    def _rgb(self, color):
        # в (r,g,b) 0..255
        r16, g16, b16 = self.root.winfo_rgb(color)
        return r16 // 256, g16 // 256, b16 // 256

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
