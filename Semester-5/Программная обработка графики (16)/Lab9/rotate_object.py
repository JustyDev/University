import tkinter as tk
from tkinter import colorchooser, messagebox
from math import hypot, sin, cos, radians

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

def polygon_centroid(points):
    """
    Центроид (центр масс) простого многоугольника.
    Если площадь близка к нулю — вернём среднее по вершинам.
    """
    A = shoelace_area_signed(points)
    if abs(A) < 1e-9:
        # вырожденно — среднее по вершинам
        sx = sum(x for x, _ in points) / len(points)
        sy = sum(y for _, y in points) / len(points)
        return sx, sy
    cx = 0.0
    cy = 0.0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i+1) % n]
        cross = x1*y2 - x2*y1
        cx += (x1 + x2) * cross
        cy += (y1 + y2) * cross
    cx /= (6.0 * A)
    cy /= (6.0 * A)
    return cx, cy

class App:
    def __init__(self, root):
        self.root = root
        root.title("Поворот фигуры")

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

        # Замыкание
        self.btn_close = tk.Button(panel, text="Замкнуть", command=self.toggle_close)
        self.btn_close.pack(fill="x", pady=(0, 6))

        # Цвет заливки
        self.fill_color = "#0b7a3c"
        self.border_color = "#000000"
        tk.Button(panel, text="Выбрать цвет", command=self.choose_fill_color).pack(fill="x", pady=(0, 10))

        # Перемещение
        move_box = tk.LabelFrame(panel, text="Перемещение фигуры:", padx=6, pady=6)
        move_box.pack(fill="x")

        tk.Button(move_box, text="верх", command=lambda: self.move_by(0, -self.get_step())).grid(row=0, column=1, pady=2)
        tk.Button(move_box, text="лево", command=lambda: self.move_by(-self.get_step(), 0)).grid(row=1, column=0, padx=2)
        tk.Button(move_box, text="право", command=lambda: self.move_by(self.get_step(), 0)).grid(row=1, column=2, padx=2)
        tk.Button(move_box, text="низ", command=lambda: self.move_by(0, self.get_step())).grid(row=2, column=1, pady=2)

        self.step_var = tk.StringVar(value="10")
        tk.Entry(move_box, textvariable=self.step_var, width=6, justify="center").grid(row=1, column=1, padx=4)

        # Поворот
        rot_box = tk.LabelFrame(panel, text="Поворот фигуры:", padx=6, pady=6)
        rot_box.pack(fill="x", pady=(8, 0))

        tk.Button(rot_box, text="по час.", command=lambda: self.rotate_by_deg(self.get_angle(), ccw=True)).grid(row=0, column=0, padx=2)
        self.angle_var = tk.StringVar(value="15")
        tk.Entry(rot_box, textvariable=self.angle_var, width=6, justify="center").grid(row=0, column=1)
        tk.Button(rot_box, text="против час.", command=lambda: self.rotate_by_deg(self.get_angle(), ccw=False)).grid(row=0, column=2, padx=2)

        # Подсказка
        self.status = tk.Label(panel, text="ЛКМ — добавить вершину;\nпри замкнутом: 2 клика для сдвига", fg="#555")
        self.status.pack(anchor="w", pady=(8, 0))

        # Данные
        self.points = []
        self.closed = False
        self.poly_item = None
        self.move_from = None

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

    def on_left_click(self, event):
        x, y = event.x, event.y
        if not self.closed:
            self.points.append((x, y))
            self.redraw()
        else:
            # перемещение двумя кликами
            if self.move_from is None:
                self.move_from = (x, y)
                self.status.config(text="Укажите конечную точку перемещения")
            else:
                dx = x - self.move_from[0]
                dy = y - self.move_from[1]
                self.move_from = None
                self.translate(dx, dy)
                self.status.config(text="ЛКМ — добавить вершину;\nпри замкнутом: 2 клика для сдвига")

    def on_right_click(self, event):
        self.toggle_close()

    def toggle_close(self):
        if len(self.points) < 3:
            messagebox.showinfo("Замкнуть", "Нужно как минимум 3 вершины.")
            return
        self.closed = not self.closed
        self.btn_close.config(text="Разомкнуть" if self.closed else "Замкнуть")
        # автозаливка отображается в redraw для замкнутого
        self.redraw()

    # ---------- Перемещение ----------
    def get_step(self):
        try:
            val = int(self.step_var.get())
            if val <= 0:
                raise ValueError
            return val
        except Exception:
            self.step_var.set("10")
            return 10

    def move_by(self, dx, dy):
        if not self.points:
            return
        self.translate(dx, dy)

    def translate(self, dx, dy):
        self.points = [(x + dx, y + dy) for (x, y) in self.points]
        self.redraw()

    # ---------- Поворот ----------
    def get_angle(self):
        try:
            v = float(self.angle_var.get())
            return v
        except Exception:
            self.angle_var.set("15")
            return 15.0

    def rotate_by_deg(self, deg, ccw=True):
        if not self.points:
            return
        theta = radians(deg if ccw else -deg)
        cx, cy = polygon_centroid(self.points)
        rotated = []
        c, s = cos(theta), sin(theta)
        for x, y in self.points:
            dx = x - cx
            dy = y - cy
            xr = cx + dx * c - dy * s
            yr = cy + dx * s + dy * c
            rotated.append((xr, yr))
        self.points = rotated
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
        if not self.closed:
            # ломаная и точки
            if len(self.points) >= 2:
                for i in range(len(self.points) - 1):
                    self.canvas.create_line(*self.points[i], *self.points[i+1], fill=self.border_color, width=3)
            for idx, (x, y) in enumerate(self.points):
                r = POINT_R
                color = "#0077ff" if idx == 0 else "#000000"
                self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=color, fill=color)
        else:
            flat = [coord for pt in self.points for coord in pt]
            self.poly_item = self.canvas.create_polygon(
                *flat, fill=self.fill_color, outline=self.border_color, width=4, joinstyle="round"
            )
        self.update_metrics()

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
