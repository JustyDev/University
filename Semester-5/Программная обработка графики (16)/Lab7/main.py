import tkinter as tk
from tkinter import messagebox
import math
from collections import deque

# Настройки "пиксельной" сетки и окна
PIXEL_SIZE = 4         # размер одного логического пикселя на экране
GRID_W, GRID_H = 220, 150   # размеры логической растра (в пикселях)
WINDOW_BG = "#f5f5f5"
BG_COLOR = "#FFFFFF"   # цвет фона/буфера

def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

class Raster:
    """
    Простейший растровый буфер + вывод в PhotoImage.
    Храним цвета как строки '#RRGGBB'.
    """
    def __init__(self, canvas, w, h, pixel_size):
        self.canvas = canvas
        self.w = w
        self.h = h
        self.ps = pixel_size
        self.img = tk.PhotoImage(width=w, height=h)
        self.canvas_img_id = self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.buf = [[BG_COLOR for _ in range(w)] for __ in range(h)]
        self.redraw_full()

    def clear(self, color=BG_COLOR):
        for y in range(self.h):
            row = self.buf[y]
            for x in range(self.w):
                row[x] = color
        self.redraw_full()

    def redraw_full(self):
        # Быстрое заполнение картинкой из строк
        # Соберём построчные данные
        # Пример: "{#FFFFFF #000000 ...} { ... }"
        lines = []
        for y in range(self.h):
            row = self.buf[y]
            line = "{" + " ".join(row) + "}"
            lines.append(line)
        self.img.put(" ".join(lines), to=(0, 0))

    def set_pixel(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            if self.buf[y][x] != color:
                self.buf[y][x] = color
                self.img.put(color, (x, y))

    def get_pixel(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.buf[y][x]
        return None

    def draw_grid(self, show):
        # Рисуем поверх изображения линиями canvas
        existing = getattr(self, "_grid_items", [])
        for it in existing:
            self.canvas.delete(it)
        self._grid_items = []
        if not show:
            return
        color = "#e6e6e6"
        wpx = self.w * self.ps
        hpx = self.h * self.ps
        # Вертикальные
        for gx in range(0, self.w + 1):
            x = gx * self.ps
            self._grid_items.append(self.canvas.create_line(x, 0, x, hpx, fill=color))
        # Горизонтальные
        for gy in range(0, self.h + 1):
            y = gy * self.ps
            self._grid_items.append(self.canvas.create_line(0, y, wpx, y, fill=color))

    def to_grid(self, cx, cy):
        return cx // self.ps, cy // self.ps

    def to_canvas_rect(self):
        return self.w * self.ps, self.h * self.ps

class App:
    def __init__(self, root):
        self.root = root
        root.title("Закраска областей (scanline, flood/boundary fill)")
        root.configure(bg=WINDOW_BG)

        # Левая часть — Canvas
        left = tk.Frame(root, bg=WINDOW_BG)
        left.pack(side=tk.LEFT, padx=8, pady=8)

        cw, ch = GRID_W * PIXEL_SIZE, GRID_H * PIXEL_SIZE
        self.canvas = tk.Canvas(left, width=cw, height=ch, bg="white", highlightthickness=1, highlightbackground="#aaa")
        self.canvas.pack()

        # Растр
        self.r = Raster(self.canvas, GRID_W, GRID_H, PIXEL_SIZE)

        # Правая панель
        right = tk.Frame(root, bg=WINDOW_BG)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=8, pady=8)

        # Цвета
        tk.Label(right, text="Цвет границы:", bg=WINDOW_BG).pack(anchor="w")
        self.boundary_color = tk.StringVar(value="#000000")
        tk.Entry(right, textvariable=self.boundary_color, width=10).pack(anchor="w", pady=(0,6))

        tk.Label(right, text="Цвет заливки:", bg=WINDOW_BG).pack(anchor="w")
        self.fill_color = tk.StringVar(value="#7d2bff")
        tk.Entry(right, textvariable=self.fill_color, width=10).pack(anchor="w", pady=(0,8))

        # Сетка и привязка
        self.grid_var = tk.BooleanVar(value=True)
        tk.Checkbutton(right, text="Сетка", variable=self.grid_var, command=self.update_grid, bg=WINDOW_BG).pack(anchor="w")
        self.snap_var = tk.BooleanVar(value=False)
        tk.Checkbutton(right, text="Привязка к узлам", variable=self.snap_var, bg=WINDOW_BG).pack(anchor="w", pady=(0,8))

        # Связанность
        tk.Label(right, text="Связанность:", bg=WINDOW_BG).pack(anchor="w")
        self.conn_var = tk.StringVar(value="4")
        tk.Radiobutton(right, text="4-связная", variable=self.conn_var, value="4", bg=WINDOW_BG).pack(anchor="w")
        tk.Radiobutton(right, text="8-связная", variable=self.conn_var, value="8", bg=WINDOW_BG).pack(anchor="w", pady=(0,8))

        # Кнопки управления
        row1 = tk.Frame(right, bg=WINDOW_BG); row1.pack(anchor="w", pady=(4,0))
        tk.Button(row1, text="Замкнуть/Разомкнуть", command=self.toggle_close).pack(side=tk.LEFT)

        row2 = tk.Frame(right, bg=WINDOW_BG); row2.pack(anchor="w", pady=(6,0))
        tk.Button(row2, text="Залить полигон (scanline)", command=self.fill_polygon_scanline).pack(side=tk.LEFT)

        row3 = tk.Frame(right, bg=WINDOW_BG); row3.pack(anchor="w", pady=(6,0))
        tk.Button(row3, text="Заливка от затравки", command=self.enable_seed_mode).pack(side=tk.LEFT)

        row4 = tk.Frame(right, bg=WINDOW_BG); row4.pack(anchor="w", pady=(6,0))
        tk.Button(row4, text="Boundary fill (от границы)", command=self.enable_boundary_mode).pack(side=tk.LEFT)

        row5 = tk.Frame(right, bg=WINDOW_BG); row5.pack(anchor="w", pady=(12,0))
        tk.Button(row5, text="Отменить вершину", command=self.undo_vertex).pack(side=tk.LEFT)

        row6 = tk.Frame(right, bg=WINDOW_BG); row6.pack(anchor="w", pady=(6,0))
        tk.Button(row6, text="Очистить всё", command=self.clear_all).pack(side=tk.LEFT)

        row7 = tk.Frame(right, bg=WINDOW_BG); row7.pack(anchor="w", pady=(12,0))
        tk.Button(row7, text="Пример звезда", command=self.example_star).pack(side=tk.LEFT)

        # Подсказка
        self.hint = tk.Label(right, text="ЛКМ — добавление вершины\nДля затравки: нажмите кнопку,\nзатем клик внутри области",
                             justify="left", bg=WINDOW_BG, fg="#555")
        self.hint.pack(anchor="w", pady=(12,0))

        # Данные многоугольника (в координатах растра — целые)
        self.vertices = []
        self.closed = False

        # Режимы клика
        self.mode = "draw"  # draw | flood | boundary

        # Привязка событий
        self.canvas.bind("<Button-1>", self.on_left_click)

        # Сетка
        self.update_grid()

    # ====================== Общие утилиты ======================
    def snap(self, x, y):
        if not self.snap_var.get():
            return x, y
        return round(x), round(y)

    def canvas_to_grid(self, cx, cy):
        gx, gy = self.r.to_grid(cx, cy)
        gx = clamp(gx, 0, self.r.w - 1)
        gy = clamp(gy, 0, self.r.h - 1)
        return gx, gy

    def update_grid(self):
        self.r.draw_grid(self.grid_var.get())

    def draw_bresenham(self, x0, y0, x1, y1, color):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.r.set_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def redraw_polygon_edges(self):
        # Перерисуем фоновый буфер (фон и всё, что уже было)
        # Здесь мы не чистим буфер — предполагается, что границы уже "нарисованы".
        # Но для наглядности можно перерисовать только рёбра:
        if not self.vertices:
            return
        col = self.boundary_color.get().strip() or "#000000"
        for i in range(len(self.vertices) - 1):
            x0, y0 = self.vertices[i]
            x1, y1 = self.vertices[i+1]
            self.draw_bresenham(x0, y0, x1, y1, col)
        if self.closed and len(self.vertices) >= 3:
            x0, y0 = self.vertices[-1]
            x1, y1 = self.vertices[0]
            self.draw_bresenham(x0, y0, x1, y1, col)

    def clear_all(self):
        self.vertices.clear()
        self.closed = False
        self.mode = "draw"
        self.r.clear(BG_COLOR)
        self.update_grid()

    def undo_vertex(self):
        if self.mode != "draw":
            messagebox.showinfo("Подсказка", "Отмена вершины доступна в режиме рисования.")
            return
        if self.vertices:
            self.vertices.pop()
            self.closed = False
            self.r.clear(BG_COLOR)
            self.redraw_polygon_edges()
            self.update_grid()

    def toggle_close(self):
        if len(self.vertices) < 3:
            messagebox.showinfo("Мало вершин", "Добавьте как минимум 3 вершины.")
            return
        self.closed = not self.closed
        self.redraw_polygon_edges()

    # ====================== Ввод кликом ======================
    def on_left_click(self, event):
        gx, gy = self.canvas_to_grid(event.x, event.y)
        gx, gy = self.snap(gx, gy)

        if self.mode == "draw":
            # при замкнутом контуре начало нового
            if self.closed:
                self.vertices = []
                self.closed = False
                self.r.clear(BG_COLOR)
                self.update_grid()

            self.vertices.append((gx, gy))
            n = len(self.vertices)
            col = self.boundary_color.get().strip() or "#000000"
            if n >= 2:
                x0, y0 = self.vertices[-2]
                x1, y1 = self.vertices[-1]
                self.draw_bresenham(x0, y0, x1, y1, col)

        elif self.mode == "flood":
            self.flood_fill(gx, gy, self.fill_color.get().strip() or "#7d2bff")
            self.mode = "draw"
        elif self.mode == "boundary":
            self.boundary_fill(gx, gy,
                               fill_color=self.fill_color.get().strip() or "#7d2bff",
                               boundary_color=self.boundary_color.get().strip() or "#000000")
            self.mode = "draw"

    def enable_seed_mode(self):
        self.mode = "flood"
        messagebox.showinfo("Затравка", "Кликните внутри области, которую нужно залить.")

    def enable_boundary_mode(self):
        self.mode = "boundary"
        messagebox.showinfo("Boundary fill", "Кликните внутри области, ограниченной цветом границы.")

    # ====================== Пример звезды ======================
    def example_star(self):
        self.clear_all()
        cx, cy = self.r.w // 2, self.r.h // 2
        R1, R2 = min(self.r.w, self.r.h) // 4, min(self.r.w, self.r.h) // 8
        pts = []
        for i in range(10):
            ang = math.radians(-90 + i * 36)  # от -90°, чтобы вершина была сверху
            R = R1 if i % 2 == 0 else R2
            x = int(round(cx + R * math.cos(ang)))
            y = int(round(cy + R * math.sin(ang)))
            pts.append((x, y))
        self.vertices = pts
        self.closed = True
        self.redraw_polygon_edges()

    # ====================== Scanline заполнение полигона ======================
    def fill_polygon_scanline(self):
        if not self.closed or len(self.vertices) < 3:
            messagebox.showinfo("Нет замкнутого контура", "Замкните многоугольник перед заливкой.")
            return

        verts = self.vertices[:]
        n = len(verts)
        y_min = min(p[1] for p in verts)
        y_max = max(p[1] for p in verts)
        fill_col = self.fill_color.get().strip() or "#7d2bff"
        boundary_col = self.boundary_color.get().strip() or "#000000"

        # По правилу чет-нечет: на каждой строке формируем список пересечений
        for y in range(max(0, y_min), min(self.r.h - 1, y_max) + 1):
            xs = []
            for i in range(n):
                x1, y1 = verts[i]
                x2, y2 = verts[(i + 1) % n]
                if y1 == y2:
                    continue  # горизонтальные рёбра не учитываем
                # полуоткрытый интервал: [minY, maxY)
                if y >= min(y1, y2) and y < max(y1, y2):
                    t = (y - y1) / (y2 - y1)
                    x = x1 + t * (x2 - x1)
                    xs.append(x)
            if not xs:
                continue
            xs.sort()
            # парами [x0, x1], [x2, x3], ...
            for k in range(0, len(xs), 2):
                if k + 1 >= len(xs):
                    break
                xL = xs[k]
                xR = xs[k + 1]
                # цулые пиксели в интервале
                xl = int(math.ceil(xL))
                xr = int(math.floor(xR))
                for x in range(xl, xr + 1):
                    # не перерисовываем границу
                    if self.r.get_pixel(x, y) != boundary_col:
                        self.r.set_pixel(x, y, fill_col)

    # ====================== Затравочные заливки ======================
    def neighbors(self, x, y):
        if self.conn_var.get() == "8":
            # 8-связная
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.r.w and 0 <= ny < self.r.h:
                        yield nx, ny
        else:
            # 4-связная
            for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.r.w and 0 <= ny < self.r.h:
                    yield nx, ny

    def flood_fill(self, sx, sy, new_color):
        """
        Классический flood fill: закрашиваем все пиксели, имеющие цвет исходной затравки.
        """
        target = self.r.get_pixel(sx, sy)
        if target is None:
            return
        if target == new_color:
            return

        dq = deque()
        dq.append((sx, sy))
        self.r.set_pixel(sx, sy, new_color)

        while dq:
            x, y = dq.popleft()
            for nx, ny in self.neighbors(x, y):
                if self.r.get_pixel(nx, ny) == target:
                    self.r.set_pixel(nx, ny, new_color)
                    dq.append((nx, ny))

    def boundary_fill(self, sx, sy, fill_color, boundary_color):
        """
        Boundary fill: растём от затравки, пока не встретим цвет границы.
        """
        if self.r.get_pixel(sx, sy) in (boundary_color, fill_color):
            return
        dq = deque()
        dq.append((sx, sy))
        self.r.set_pixel(sx, sy, fill_color)

        while dq:
            x, y = dq.popleft()
            for nx, ny in self.neighbors(x, y):
                c = self.r.get_pixel(nx, ny)
                if c is None:
                    continue
                if c != boundary_color and c != fill_color:
                    self.r.set_pixel(nx, ny, fill_color)
                    dq.append((nx, ny))

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
