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

class App:
    def __init__(self, root):
        self.root = root
        root.title("Перемещение фигуры")

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

        self.fill_color = "#b3124b"
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

        # Подсказка по перемещению мышью
        self.status = tk.Label(panel, text="ЛКМ — добавить вершину;\nпри замкнутом: 2 клика для сдвига", fg="#555")
        self.status.pack(anchor="w", pady=(8, 0))

        # Данные
        self.points = []
        self.closed = False
        self.poly_item = None  # id create_polygon
        self.move_from = None  # для перемещения двумя кликами

        # События
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)  # альтернативное замыкание

        self.redraw()

    # ---------- UI действия ----------
    def choose_fill_color(self):
        color = colorchooser.askcolor(self.fill_color, title="Цвет заливки")[1]
        if color:
            self.fill_color = color
            if self.closed:
                self.redraw()  # обновить заливку

    def on_left_click(self, event):
        x, y = event.x, event.y

        if not self.closed:
            # ввод вершин
            self.points.append((x, y))
            self.redraw()
        else:
            # перемещение двумя кликами
            if self.move_from is None:
                self.move_from = (x, y)
                self.status.config(text="Выберите конечную точку перемещения")
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
        # автозаливка после замыкания
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
        # незамкнутый: рёбра + точки
        if not self.closed:
            if len(self.points) >= 2:
                for i in range(len(self.points) - 1):
                    self.canvas.create_line(*self.points[i], *self.points[i+1], fill=self.border_color, width=3)
            for idx, (x, y) in enumerate(self.points):
                r = POINT_R
                color = "#0077ff" if idx == 0 else "#000000"
                self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=color, fill=color)
        else:
            # замкнутый: залитый многоугольник
            flat = [coord for pt in self.points for coord in pt]
            # create_polygon сам соединит последнюю и первую точки
            self.poly_item = self.canvas.create_polygon(
                *flat, fill=self.fill_color, outline=self.border_color, width=4, joinstyle="round"
            )

        self.update_metrics()

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
