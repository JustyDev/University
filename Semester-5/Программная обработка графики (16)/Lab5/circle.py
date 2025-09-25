import tkinter as tk
import math
from time import perf_counter

WIDTH, HEIGHT = 900, 600
PIXEL_SIZE = 4  # размер "пикселя" на экране

def to_grid(x, y):
    return x // PIXEL_SIZE, y // PIXEL_SIZE

def to_canvas(gx, gy):
    return gx * PIXEL_SIZE, gy * PIXEL_SIZE

class App:
    def __init__(self, root):
        self.root = root
        root.title("Окружности/дуги — вариант 16 (штрихпунктир 3-3-1-3)")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        ctrl = tk.Frame(root)
        ctrl.pack(side=tk.BOTTOM, fill=tk.X, pady=4)

        # Режимы
        self.mode = tk.StringVar(value="circle")
        tk.Radiobutton(ctrl, text="Окружность", variable=self.mode, value="circle").pack(side=tk.LEFT, padx=4)
        tk.Radiobutton(ctrl, text="Дуга", variable=self.mode, value="arc").pack(side=tk.LEFT)
        tk.Radiobutton(ctrl, text="Концентрические", variable=self.mode, value="concentric").pack(side=tk.LEFT)

        # Цвет
        tk.Label(ctrl, text="Цвет:").pack(side=tk.LEFT, padx=(10, 2))
        self.color_var = tk.StringVar(value="#000000")
        tk.Entry(ctrl, textvariable=self.color_var, width=8).pack(side=tk.LEFT)

        # Радиус / шаг / количество
        tk.Label(ctrl, text="R:").pack(side=tk.LEFT, padx=(10, 2))
        self.r_var = tk.StringVar(value="")
        tk.Entry(ctrl, textvariable=self.r_var, width=6).pack(side=tk.LEFT)

        tk.Label(ctrl, text="Шаг dR:").pack(side=tk.LEFT, padx=(8, 2))
        self.step_var = tk.StringVar(value="20")
        tk.Entry(ctrl, textvariable=self.step_var, width=6).pack(side=tk.LEFT)

        tk.Label(ctrl, text="N:").pack(side=tk.LEFT, padx=(8, 2))
        self.n_var = tk.StringVar(value="5")
        tk.Entry(ctrl, textvariable=self.n_var, width=6).pack(side=tk.LEFT)

        # Углы для дуги (в градусах, 0 — вправо, против часовой)
        tk.Label(ctrl, text="угол нач:").pack(side=tk.LEFT, padx=(12, 2))
        self.a0_var = tk.StringVar(value="0")
        tk.Entry(ctrl, textvariable=self.a0_var, width=6).pack(side=tk.LEFT)

        tk.Label(ctrl, text="угол кон:").pack(side=tk.LEFT, padx=(6, 2))
        self.a1_var = tk.StringVar(value="180")
        tk.Entry(ctrl, textvariable=self.a1_var, width=6).pack(side=tk.LEFT)

        # Кнопки
        tk.Button(ctrl, text="Нарисовать (по полям)", command=self.draw_from_fields).pack(side=tk.LEFT, padx=10)
        tk.Button(ctrl, text="Очистить", command=self.clear).pack(side=tk.LEFT)
        self.grid_var = tk.BooleanVar(value=False)
        tk.Checkbutton(ctrl, text="Сетка", variable=self.grid_var, command=self.toggle_grid).pack(side=tk.LEFT, padx=8)

        self.status = tk.Label(ctrl, text="ЛКМ: центр; второй ЛКМ: радиус", anchor="w")
        self.status.pack(side=tk.LEFT, padx=12)

        self.center = None
        self.grid_items = []

        self.canvas.bind("<Button-1>", self.on_click)

        # Шаблон варианта 16
        self.pattern = [3, 3, 1, 3]           # длины сегментов в пикселях
        self.pattern_modes = [True, False, True, False]  # рисуем/пропуск

    # ======== рисование базовое ========
    def draw_pixel(self, gx, gy, color="#000000"):
        x0, y0 = to_canvas(gx, gy)
        x1, y1 = x0 + PIXEL_SIZE - 1, y0 + PIXEL_SIZE - 1
        self.canvas.create_rectangle(x0, y0, x1, y1, outline=color, fill=color)

    # ======== служебные для дуги ========
    @staticmethod
    def normalize_angle_deg(a):
        return a % 360.0

    def make_angle_filter(self, cx, cy, a0_deg, a1_deg):
        a0 = self.normalize_angle_deg(a0_deg)
        a1 = self.normalize_angle_deg(a1_deg)

        def in_range(ang):
            # полный круг, если углы совпадают
            if abs(((a1 - a0) % 360.0)) < 1e-9:
                return True
            if a0 <= a1:
                return a0 <= ang <= a1
            else:
                return ang >= a0 or ang <= a1

        def filt(px, py):
            ang = math.degrees(math.atan2(-(py - cy), (px - cx)))
            ang = self.normalize_angle_deg(ang)
            return in_range(ang)

        return filt

    # ======== построение окружности упорядоченным обходом ========
    @staticmethod
    def octant_points_r0(r):
        """
        Алгоритм средней точки для базового октанта (0..45°), старт в (r, 0).
        Возвращает список (x,y) для x >= y >= 0 в порядке возрастания угла.
        """
        x, y = int(round(r)), 0
        d = 1 - x
        pts = []
        while y <= x:
            pts.append((x, y))
            y += 1
            if d < 0:
                d += 2 * y + 1
            else:
                x -= 1
                d += 2 * (y - x) + 1
        return pts  # (x, y) для базового октанта

    def circle_path_points(self, cx, cy, r):
        """
        Полный упорядоченный путь по окружности CCW, начиная с угла 0° (вправо).
        Использует базовый октант и симметрии с реверсом по нечётным октантам.
        """
        base = self.octant_points_r0(r)
        # Отображения в октанты (0..7), плюс нужно ли реверсировать base
        maps = [
            (lambda x, y: (cx + x, cy - y), False),  # 0:   0..45
            (lambda x, y: (cx + y, cy - x), True),   # 1:  45..90
            (lambda x, y: (cx - y, cy - x), False),  # 2:  90..135
            (lambda x, y: (cx - x, cy - y), True),   # 3: 135..180
            (lambda x, y: (cx - x, cy + y), False),  # 4: 180..225
            (lambda x, y: (cx - y, cy + x), True),   # 5: 225..270
            (lambda x, y: (cx + y, cy + x), False),  # 6: 270..315
            (lambda x, y: (cx + x, cy + y), True),   # 7: 315..360
        ]

        path = []
        first = True
        for transform, need_rev in maps:
            seq = reversed(base) if need_rev else base
            for i, (x, y) in enumerate(seq):
                # избегаем дубликатов на стыках октантов
                if not first and i == 0:
                    continue
                path.append(transform(x, y))
            first = False
        return path

    def draw_circle_variant16(self, cx, cy, r, color, angle_filter=None):
        """
        Рисует окружность/дугу штрихпунктиром 3-3-1-3 (вариант 16).
        Если задан angle_filter(px, py) -> bool, рисуем только точки дуги.
        """
        if r <= 0:
            return 0
        path = self.circle_path_points(cx, cy, r)

        seg_idx = 0
        remaining = self.pattern[seg_idx]
        draw_on = self.pattern_modes[seg_idx]

        pixels = 0
        for (px, py) in path:
            if (angle_filter is None) or angle_filter(px, py):
                if draw_on:
                    self.draw_pixel(px, py, color)
                    pixels += 1
                remaining -= 1
                if remaining == 0:
                    seg_idx = (seg_idx + 1) % len(self.pattern)
                    remaining = self.pattern[seg_idx]
                    draw_on = self.pattern_modes[seg_idx]
        return pixels

    # ======== UI обработка ========
    def on_click(self, event):
        gx, gy = to_grid(event.x, event.y)
        if self.center is None:
            self.center = (gx, gy)
            self.draw_pixel(gx, gy, "#ff0000")
            self.status.config(text=f"Центр: ({gx},{gy}). Второй ЛКМ: радиус.")
        else:
            cx, cy = self.center
            dx, dy = gx - cx, gy - cy
            R = int(round(math.hypot(dx, dy)))
            color = self.color_var.get().strip() or "#000000"

            t0 = perf_counter()
            pixels = 0

            if self.mode.get() == "circle":
                pixels = self.draw_circle_variant16(cx, cy, R, color)
            elif self.mode.get() == "arc":
                a0 = float(self.a0_var.get() or 0)
                a1 = float(self.a1_var.get() or 0)
                filt = self.make_angle_filter(cx, cy, a0, a1)
                pixels = self.draw_circle_variant16(cx, cy, R, color, angle_filter=filt)
            else:  # concentric
                n = int(self.n_var.get() or 1)
                step = int(self.step_var.get() or 1)
                for i in range(n):
                    r_i = R + i * step
                    pixels += self.draw_circle_variant16(cx, cy, r_i, color)

            dt = (perf_counter() - t0) * 1000.0
            print(f"Готово: mode={self.mode.get()}, центр=({cx},{cy}), R={R}, пикселей={pixels}, {dt:.2f} мс")

            self.center = None
            self.status.config(text="ЛКМ: центр; второй ЛКМ: радиус")

    def draw_from_fields(self):
        color = self.color_var.get().strip() or "#000000"
        if self.center is None:
            cx = (self.canvas.winfo_width() // PIXEL_SIZE) // 2
            cy = (self.canvas.winfo_height() // PIXEL_SIZE) // 2
        else:
            cx, cy = self.center

        mode = self.mode.get()
        t0 = perf_counter()
        pixels = 0

        if mode == "circle":
            R = int(self.r_var.get() or 80)
            pixels = self.draw_circle_variant16(cx, cy, R, color)
        elif mode == "arc":
            R = int(self.r_var.get() or 80)
            a0 = float(self.a0_var.get() or 0)
            a1 = float(self.a1_var.get() or 180)
            filt = self.make_angle_filter(cx, cy, a0, a1)
            pixels = self.draw_circle_variant16(cx, cy, R, color, angle_filter=filt)
        else:  # concentric
            R = int(self.r_var.get() or 40)
            n = int(self.n_var.get() or 5)
            step = int(self.step_var.get() or 20)
            for i in range(n):
                r_i = R + i * step
                pixels += self.draw_circle_variant16(cx, cy, r_i, color)

        dt = (perf_counter() - t0) * 1000.0
        print(f"Готово: mode={mode}, центр=({cx},{cy}), пикселей={pixels}, {dt:.2f} мс")
        self.center = None
        self.status.config(text="ЛКМ: центр; второй ЛКМ: радиус")

    def clear(self):
        self.canvas.delete("all")
        self.center = None
        if self.grid_var.get():
            self.draw_grid()

    def toggle_grid(self):
        if self.grid_var.get():
            self.draw_grid()
        else:
            for item in self.grid_items:
                self.canvas.delete(item)
            self.grid_items.clear()

    def draw_grid(self):
        for item in self.grid_items:
            self.canvas.delete(item)
        self.grid_items.clear()

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        cols = w // PIXEL_SIZE
        rows = h // PIXEL_SIZE
        color = "#e8e8e8"
        for c in range(cols + 1):
            x = c * PIXEL_SIZE
            self.grid_items.append(self.canvas.create_line(x, 0, x, h, fill=color))
        for r in range(rows + 1):
            y = r * PIXEL_SIZE
            self.grid_items.append(self.canvas.create_line(0, y, w, y, fill=color))

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
