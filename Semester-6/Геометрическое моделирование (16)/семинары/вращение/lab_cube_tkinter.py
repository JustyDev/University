import math
import tkinter as tk
from tkinter import messagebox, ttk


class FigureApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Лабораторная работа: Куб")
        self.root.geometry("1180x760")
        self.root.minsize(1040, 680)

        self.canvas_width = 700
        self.canvas_height = 680
        self.base_scale = 120.0
        self.current_points: list[list[float]] = []
        self.current_edges: list[tuple[int, int]] = []

        self.point_entries: list[tuple[tk.Entry, tk.Entry, tk.Entry]] = []
        self.edge_entries: list[tuple[tk.Entry, tk.Entry]] = []

        self.axis_var = tk.StringVar(value="ox")
        self.angle_var = tk.StringVar(value="15")
        self.scale_var = tk.StringVar(value="1.2")

        self._build_ui()
        self._fill_default_cube()
        self.render_figure()

    def _build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill="both", expand=True)
        main.columnconfigure(0, weight=0)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        controls = ttk.Frame(main)
        controls.grid(row=0, column=0, sticky="nsw", padx=(0, 12))

        canvas_frame = ttk.LabelFrame(main, text="Графическое поле", padding=8)
        canvas_frame.grid(row=0, column=1, sticky="nsew")
        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            canvas_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            background="white",
            highlightthickness=1,
            highlightbackground="#b0b0b0",
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        point_frame = ttk.LabelFrame(controls, text="Координаты точек", padding=8)
        point_frame.pack(fill="x")

        ttk.Label(point_frame, text="X").grid(row=0, column=0, padx=4, pady=(0, 4))
        ttk.Label(point_frame, text="Y").grid(row=0, column=1, padx=4, pady=(0, 4))
        ttk.Label(point_frame, text="Z").grid(row=0, column=2, padx=4, pady=(0, 4))

        for index in range(8):
            ttk.Label(point_frame, text=f"{index + 1}.").grid(row=index + 1, column=0, sticky="w")
            x_entry = ttk.Entry(point_frame, width=8)
            y_entry = ttk.Entry(point_frame, width=8)
            z_entry = ttk.Entry(point_frame, width=8)
            x_entry.grid(row=index + 1, column=0, padx=(24, 4), pady=2)
            y_entry.grid(row=index + 1, column=1, padx=4, pady=2)
            z_entry.grid(row=index + 1, column=2, padx=4, pady=2)
            self.point_entries.append((x_entry, y_entry, z_entry))

        edge_frame = ttk.LabelFrame(controls, text="Соединения точек", padding=8)
        edge_frame.pack(fill="x", pady=(12, 0))

        ttk.Label(edge_frame, text="Точка 1").grid(row=0, column=0, padx=4, pady=(0, 4))
        ttk.Label(edge_frame, text="Точка 2").grid(row=0, column=1, padx=4, pady=(0, 4))

        for index in range(12):
            ttk.Label(edge_frame, text=f"{index + 1}.").grid(row=index + 1, column=0, sticky="w")
            first_entry = ttk.Entry(edge_frame, width=8)
            second_entry = ttk.Entry(edge_frame, width=8)
            first_entry.grid(row=index + 1, column=0, padx=(24, 4), pady=2)
            second_entry.grid(row=index + 1, column=1, padx=4, pady=2)
            self.edge_entries.append((first_entry, second_entry))

        action_frame = ttk.LabelFrame(controls, text="Управление", padding=8)
        action_frame.pack(fill="x", pady=(12, 0))

        ttk.Button(action_frame, text="Старт", command=self.start).pack(fill="x", pady=2)

        scale_row = ttk.Frame(action_frame)
        scale_row.pack(fill="x", pady=(8, 2))
        ttk.Label(scale_row, text="Коэффициент").pack(anchor="w")
        ttk.Entry(scale_row, textvariable=self.scale_var, width=12).pack(fill="x", pady=(2, 0))
        ttk.Button(action_frame, text="Масштабировать", command=self.scale_figure).pack(fill="x", pady=2)

        rotate_row = ttk.Frame(action_frame)
        rotate_row.pack(fill="x", pady=(8, 2))
        ttk.Label(rotate_row, text="Ось вращения").pack(anchor="w")
        axis_box = ttk.Combobox(
            rotate_row,
            textvariable=self.axis_var,
            values=("ox", "oy", "oz"),
            state="readonly",
            width=10,
        )
        axis_box.pack(fill="x", pady=(2, 6))
        ttk.Label(rotate_row, text="Угол в градусах").pack(anchor="w")
        ttk.Entry(rotate_row, textvariable=self.angle_var, width=12).pack(fill="x", pady=(2, 0))
        ttk.Button(action_frame, text="Повернуть", command=self.rotate_figure).pack(fill="x", pady=2)

        ttk.Button(action_frame, text="Сбросить", command=self.reset_defaults).pack(fill="x", pady=(8, 2))

        hint = (
            "Индексация точек начинается с 1.\n"
        )
        ttk.Label(controls, text=hint, justify="left").pack(anchor="w", pady=(12, 0))

    def _fill_default_cube(self) -> None:
        default_points = [
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
        ]
        default_edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 1),
            (5, 6),
            (6, 7),
            (7, 8),
            (8, 5),
            (1, 5),
            (2, 6),
            (3, 7),
            (4, 8),
        ]

        for entries, values in zip(self.point_entries, default_points):
            for entry, value in zip(entries, values):
                entry.delete(0, tk.END)
                entry.insert(0, str(value))

        for entries, values in zip(self.edge_entries, default_edges):
            for entry, value in zip(entries, values):
                entry.delete(0, tk.END)
                entry.insert(0, str(value))

    def reset_defaults(self) -> None:
        self._fill_default_cube()
        self.start()

    def _read_points(self) -> list[list[float]]:
        points: list[list[float]] = []
        for index, (x_entry, y_entry, z_entry) in enumerate(self.point_entries, start=1):
            x_text = x_entry.get().strip()
            y_text = y_entry.get().strip()
            z_text = z_entry.get().strip()
            if not x_text and not y_text and not z_text:
                continue
            try:
                point = [float(x_text), float(y_text), float(z_text)]
            except ValueError as exc:
                raise ValueError(f"Некорректные координаты у точки {index}.") from exc
            points.append(point)
        if not points:
            raise ValueError("Введите хотя бы одну точку.")
        return points

    def _read_edges(self, point_count: int) -> list[tuple[int, int]]:
        edges: list[tuple[int, int]] = []
        for index, (first_entry, second_entry) in enumerate(self.edge_entries, start=1):
            first_text = first_entry.get().strip()
            second_text = second_entry.get().strip()
            if not first_text and not second_text:
                continue
            try:
                first = int(first_text)
                second = int(second_text)
            except ValueError as exc:
                raise ValueError(f"Некорректная пара соединения в строке {index}.") from exc
            if first < 1 or second < 1 or first > point_count or second > point_count:
                raise ValueError(
                    f"В строке {index} указана точка вне диапазона 1..{point_count}."
                )
            edges.append((first - 1, second - 1))
        if not edges:
            raise ValueError("Введите хотя бы одно соединение между точками.")
        return edges

    def start(self) -> None:
        try:
            self.current_points = self._read_points()
            self.current_edges = self._read_edges(len(self.current_points))
            self.render_figure()
        except ValueError as error:
            messagebox.showerror("Ошибка ввода", str(error))

    def scale_figure(self) -> None:
        if not self.current_points:
            self.start()
            if not self.current_points:
                return
        try:
            factor = float(self.scale_var.get().strip())
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Введите числовой коэффициент масштаба.")
            return
        self.current_points = [[coord * factor for coord in point] for point in self.current_points]
        self.render_figure()

    def rotate_figure(self) -> None:
        if not self.current_points:
            self.start()
            if not self.current_points:
                return
        try:
            angle_deg = float(self.angle_var.get().strip())
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Введите числовой угол поворота.")
            return

        axis = self.axis_var.get()
        angle = math.radians(angle_deg)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        rotated_points: list[list[float]] = []

        for x, y, z in self.current_points:
            if axis == "ox":
                rotated = [x, y * cos_a - z * sin_a, y * sin_a + z * cos_a]
            elif axis == "oy":
                rotated = [x * cos_a + z * sin_a, y, -x * sin_a + z * cos_a]
            else:
                rotated = [x * cos_a - y * sin_a, x * sin_a + y * cos_a, z]
            rotated_points.append(rotated)

        self.current_points = rotated_points
        self.render_figure()

    def _project_point(self, point):
        x, y, z = point
        projection_x = x - 0.45 * z
        projection_y = y - 0.25 * z
        screen_x = self.canvas_width / 2 + projection_x * self.base_scale
        screen_y = self.canvas_height / 2 - projection_y * self.base_scale
        return screen_x, screen_y

    def render_figure(self) -> None:
        self.canvas.delete("all")
        self._draw_axes()

        if not self.current_points:
            return

        projected = [self._project_point(point) for point in self.current_points]

        for first, second in self.current_edges:
            x1, y1 = projected[first]
            x2, y2 = projected[second]
            self.canvas.create_line(x1, y1, x2, y2, fill="#1f3c88", width=2)

        for index, (x, y) in enumerate(projected, start=1):
            self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="#d62828", outline="")
            self.canvas.create_text(x + 14, y - 10, text=str(index), fill="#222222", font=("Arial", 11))

    def _draw_axes(self) -> None:
        cx = self.canvas_width / 2
        cy = self.canvas_height / 2
        length = 220

        self.canvas.create_line(cx, cy, cx + length, cy, arrow=tk.LAST, fill="#666666")
        self.canvas.create_text(cx + length + 20, cy, text="X", fill="#666666")

        self.canvas.create_line(cx, cy, cx, cy - length, arrow=tk.LAST, fill="#666666")
        self.canvas.create_text(cx, cy - length - 14, text="Y", fill="#666666")

        self.canvas.create_line(cx, cy, cx - 110, cy + 75, arrow=tk.LAST, fill="#666666")
        self.canvas.create_text(cx - 126, cy + 88, text="Z", fill="#666666")


def main() -> None:
    root = tk.Tk()
    ttk.Style().theme_use("clam")
    FigureApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
