import tkinter as tk

# Настройка размеров окна и "пикселя" (масштаб отображения)
WIDTH, HEIGHT = 800, 500
PIXEL_SIZE = 8  # размер рисуемого "пикселя" на холсте (для наглядности)

def bresenham_line(x0, y0, x1, y1, plot):
    """
    Целочисленный алгоритм Брезенхема во всех октантах.
    Вызывает plot(x, y) на каждом пикселе линии.
    """
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        plot(x0, y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

class App:
    def __init__(self, root):
        self.root = root
        root.title("Штрихпунктирная линия (вариант 16)")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        panel = tk.Frame(root)
        panel.pack(side=tk.BOTTOM, fill=tk.X)

        self.color_var = tk.StringVar(value="#000000")
        tk.Label(panel, text="Цвет:").pack(side=tk.LEFT, padx=(8, 4))
        self.color_entry = tk.Entry(panel, textvariable=self.color_var, width=10)
        self.color_entry.pack(side=tk.LEFT, padx=(0, 8))

        tk.Button(panel, text="Очистить", command=self.clear).pack(side=tk.LEFT, padx=8)
        tk.Label(panel, text="ЛКМ: выберите 2 точки для отрезка").pack(side=tk.LEFT, padx=16)

        self.start_point = None  # первая точка в "сеточных" координатах

        # Привязка события клика мышью
        self.canvas.bind("<Button-1>", self.on_click)

    def clear(self):
        self.canvas.delete("all")
        self.start_point = None

    def on_click(self, event):
        # Перевод экранных координат в "сетку" пикселей
        gx = event.x // PIXEL_SIZE
        gy = event.y // PIXEL_SIZE

        if self.start_point is None:
            self.start_point = (gx, gy)
            # пометим первую точку
            self.draw_pixel(gx, gy, "#ff0000")
        else:
            x0, y0 = self.start_point
            x1, y1 = gx, gy
            color = self.color_var.get().strip() or "#000000"
            self.draw_line_dashdot(x0, y0, x1, y1, color)
            self.start_point = None

    def draw_pixel(self, gx, gy, color="#000000"):
        """
        Рисует один "пиксель" в сеточных координатах (gx, gy)
        как прямоугольник PIXEL_SIZE x PIXEL_SIZE на холсте.
        """
        x0 = gx * PIXEL_SIZE
        y0 = gy * PIXEL_SIZE
        x1 = x0 + PIXEL_SIZE - 1
        y1 = y0 + PIXEL_SIZE - 1
        self.canvas.create_rectangle(x0, y0, x1, y1, outline=color, fill=color)

    def draw_line_dashdot(self, x0, y0, x1, y1, color="#000000"):
        """
        Рисует линию штрихпунктиром:
        3 пикселя - пропуск 3 - 1 пиксель - пропуск 3 - повтор.
        """
        # Длины сегментов (в пикселях линии)
        pattern = [3, 3, 1, 3]
        # Режимы для каждого сегмента: рисовать/пропускать
        modes = [True, False, True, False]

        seg_idx = 0
        remaining = pattern[seg_idx]
        draw_on = modes[seg_idx]

        def patterned_plot(px, py):
            nonlocal seg_idx, remaining, draw_on
            if draw_on:
                self.draw_pixel(px, py, color)
            remaining -= 1
            if remaining == 0:
                seg_idx = (seg_idx + 1) % len(pattern)
                remaining = pattern[seg_idx]
                draw_on = modes[seg_idx]

        bresenham_line(x0, y0, x1, y1, patterned_plot)

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
