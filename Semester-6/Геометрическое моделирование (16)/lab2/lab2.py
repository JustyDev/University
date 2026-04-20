import tkinter as tk
from tkinter import ttk
from typing import Optional, List
import math

# ── Константы ─────────────────────────────────────────────────────────────
CANVAS_W = 520
CANVAS_H = 460
POINT_R  = 7    # радиус кружка точки
HIT_R    = 12   # радиус обнаружения клика/наведения
GRID_STEP = 40  # шаг сетки

COLOR_LINE     = "#2c7be5"
COLOR_POINT    = "#e63946"
COLOR_HOVER    = "#ff9f43"
COLOR_DRAG     = "#2dc653"
COLOR_SELECTED = "#a855f7"
COLOR_FILL     = "#afd3fa"
COLOR_BG       = "#f0f4f8"
COLOR_GRID     = "#dde3ec"
COLOR_DARK     = "#1d2d44"


class PolyEditor:
    """Интерактивный редактор полигональной фигуры с таблицей координат."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Лаб. 2 — Полигональная фигура  |  Вариант 16")
        root.resizable(False, False)
        root.configure(bg=COLOR_DARK)

        self.points: List[List[float]] = []   # [[x, y], ...]
        self._drag_idx:     Optional[int] = None
        self._hover_idx:    Optional[int] = None
        self._selected_idx: Optional[int] = None

        self._build_ui()
        self._redraw()

    # ── Построение интерфейса ─────────────────────────────────────────────

    def _build_ui(self) -> None:
        # Заголовок
        tk.Label(self.root,
                 text="Лабораторная работа №2  |  Полигональная фигура",
                 font=("Arial", 13, "bold"),
                 bg=COLOR_DARK, fg="white", pady=6).pack(fill=tk.X)

        body = tk.Frame(self.root, bg=COLOR_DARK)
        body.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        # ── Холст ──────────────────────────────────────────────────────────
        canvas_frame = tk.LabelFrame(body, text=" Графическая область ",
                                      font=("Arial", 10, "bold"),
                                      bg=COLOR_DARK, fg="#adb5bd", labelanchor="n")
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.canvas = tk.Canvas(canvas_frame,
                                 width=CANVAS_W, height=CANVAS_H,
                                 bg=COLOR_BG, cursor="crosshair",
                                 highlightthickness=1,
                                 highlightbackground="#4a90d9")
        self.canvas.pack(padx=4, pady=4)

        self.canvas.bind("<Button-1>",        self._on_press)
        self.canvas.bind("<B1-Motion>",       self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<Button-2>",        self._on_delete)  # macOS trackpad
        self.canvas.bind("<Button-3>",        self._on_delete)  # ПКМ
        self.canvas.bind("<Motion>",          self._on_hover)

        self.status_var = tk.StringVar(
            value="ЛКМ — добавить точку  |  Перетащить — переместить  |  ПКМ — удалить")
        tk.Label(canvas_frame, textvariable=self.status_var,
                 font=("Arial", 9), bg=COLOR_DARK, fg="#adb5bd",
                 pady=2).pack()

        # ── Правая панель ──────────────────────────────────────────────────
        right = tk.Frame(body, bg=COLOR_DARK, padx=6)
        right.pack(side=tk.LEFT, fill=tk.Y)

        # Таблица
        tbl_frame = tk.LabelFrame(right, text=" Координаты точек ",
                                   font=("Arial", 10, "bold"),
                                   bg=COLOR_DARK, fg="#adb5bd")
        tbl_frame.pack(fill=tk.BOTH, expand=True)

        self._setup_table_style()

        cols = ("№", "X", "Y", "Длина")
        self.tree = ttk.Treeview(tbl_frame, columns=cols, show="headings",
                                  height=16, style="Custom.Treeview")
        widths = {"№": 38, "X": 65, "Y": 65, "Длина": 70}
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths[col], anchor=tk.CENTER)

        sb = ttk.Scrollbar(tbl_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(4, 0), pady=4)
        sb.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 4), pady=4)

        self.tree.bind("<<TreeviewSelect>>", self._on_table_select)

        # Опции
        opts = tk.Frame(right, bg=COLOR_DARK, pady=4)
        opts.pack(fill=tk.X)

        self.closed_var = tk.BooleanVar(value=False)
        self.fill_var   = tk.BooleanVar(value=False)
        self.grid_var   = tk.BooleanVar(value=True)

        for text, var in (("Замкнуть фигуру", self.closed_var),
                          ("Заливка фигуры",  self.fill_var),
                          ("Показать сетку",  self.grid_var)):
            tk.Checkbutton(opts, text=text, variable=var,
                           command=self._refresh,
                           bg=COLOR_DARK, fg="white",
                           selectcolor="#3a86ff",
                           activebackground=COLOR_DARK,
                           activeforeground="white",
                           font=("Arial", 10)).pack(anchor=tk.W)

        tk.Button(right, text="  Очистить всё  ",
                  command=self._clear,
                  bg="#e63946", fg="white",
                  font=("Arial", 10, "bold"),
                  relief=tk.FLAT, cursor="hand2",
                  pady=4).pack(fill=tk.X, pady=6)

        self.summary_var = tk.StringVar(value="Точек: 0")
        tk.Label(right, textvariable=self.summary_var,
                 font=("Arial", 10), bg=COLOR_DARK, fg="#adb5bd").pack()

    @staticmethod
    def _setup_table_style() -> None:
        style = ttk.Style()
        style.configure("Custom.Treeview",
                        font=("Courier", 11), rowheight=22,
                        background="white", fieldbackground="white")
        style.configure("Custom.Treeview.Heading",
                        font=("Arial", 10, "bold"))
        style.map("Custom.Treeview",
                  background=[("selected", "#3a86ff")],
                  foreground=[("selected", "white")])

    # ── Вспомогательные ───────────────────────────────────────────────────

    def _find_near(self, x: float, y: float) -> Optional[int]:
        for i, (px, py) in enumerate(self.points):
            if math.hypot(x - px, y - py) <= HIT_R:
                return i
        return None

    def _clamp(self, x: float, y: float):
        return (max(POINT_R, min(x, CANVAS_W - POINT_R)),
                max(POINT_R, min(y, CANVAS_H - POINT_R)))

    # ── Обработчики мыши ─────────────────────────────────────────────────

    def _on_press(self, event: tk.Event) -> None:
        idx = self._find_near(event.x, event.y)
        if idx is not None:
            self._drag_idx = idx
            self._selected_idx = idx
            self._redraw()
        else:
            x, y = self._clamp(event.x, event.y)
            self.points.append([x, y])
            self._drag_idx = len(self.points) - 1
            self._selected_idx = self._drag_idx
            self._refresh()

    def _on_drag(self, event: tk.Event) -> None:
        if self._drag_idx is not None:
            self.points[self._drag_idx] = list(self._clamp(event.x, event.y))
            self._refresh()

    def _on_release(self, event: tk.Event) -> None:
        self._drag_idx = None

    def _on_delete(self, event: tk.Event) -> None:
        idx = self._find_near(event.x, event.y)
        if idx is None:
            return
        del self.points[idx]
        if self._selected_idx == idx:
            self._selected_idx = None
        elif self._selected_idx is not None and self._selected_idx > idx:
            self._selected_idx -= 1
        self._refresh()

    def _on_hover(self, event: tk.Event) -> None:
        old = self._hover_idx
        self._hover_idx = self._find_near(event.x, event.y)
        if old != self._hover_idx:
            cursor = "fleur" if self._hover_idx is not None else "crosshair"
            self.canvas.config(cursor=cursor)
            if self._hover_idx is not None:
                hx, hy = self.points[self._hover_idx]
                self.status_var.set(
                    f"Точка {self._hover_idx + 1}:  X = {hx:.0f},  Y = {hy:.0f}")
            else:
                self.status_var.set(
                    "ЛКМ — добавить точку  |  Перетащить — переместить  |  ПКМ — удалить")
            self._redraw()

    def _on_table_select(self, event: tk.Event) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        if vals:
            idx = int(vals[0]) - 1
            if 0 <= idx < len(self.points):
                self._selected_idx = idx
                self._redraw()

    # ── Отрисовка ─────────────────────────────────────────────────────────

    def _refresh(self) -> None:
        self._redraw()
        self._update_table()

    def _redraw(self) -> None:
        self.canvas.delete("all")

        # Сетка
        if self.grid_var.get():
            for gx in range(0, CANVAS_W + 1, GRID_STEP):
                self.canvas.create_line(gx, 0, gx, CANVAS_H,
                                         fill=COLOR_GRID, width=1)
            for gy in range(0, CANVAS_H + 1, GRID_STEP):
                self.canvas.create_line(0, gy, CANVAS_W, gy,
                                         fill=COLOR_GRID, width=1)

        pts = self.points
        n   = len(pts)

        if n == 0:
            self.canvas.create_text(
                CANVAS_W // 2, CANVAS_H // 2,
                text="Нажмите левой кнопкой мыши\nдля добавления точек",
                font=("Arial", 13), fill="#b0bec5", justify=tk.CENTER)
            return

        closed = self.closed_var.get() and n >= 3

        # Заливка (только когда замкнута)
        if closed and self.fill_var.get():
            flat = [coord for p in pts for coord in p]
            self.canvas.create_polygon(flat, fill=COLOR_FILL, outline="")

        # Линии
        if n >= 2:
            for i in range(n - 1):
                x1, y1 = pts[i]
                x2, y2 = pts[i + 1]
                self.canvas.create_line(x1, y1, x2, y2,
                                         fill=COLOR_LINE, width=2,
                                         capstyle=tk.ROUND)
        if closed:
            x1, y1 = pts[-1]
            x2, y2 = pts[0]
            self.canvas.create_line(x1, y1, x2, y2,
                                     fill=COLOR_LINE, width=2, dash=(6, 3))

        # Точки
        for i, (x, y) in enumerate(pts):
            r = POINT_R
            if i == self._drag_idx:
                color = COLOR_DRAG
            elif i == self._selected_idx:
                color = COLOR_SELECTED
            elif i == self._hover_idx:
                color = COLOR_HOVER
            else:
                color = COLOR_POINT

            self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                     fill=color, outline="white", width=2)

            # Номер точки (смещаем, чтобы не вылезал за края)
            lx = x + r + 7 if x < CANVAS_W - 22 else x - r - 7
            anchor = tk.W if x < CANVAS_W - 22 else tk.E
            self.canvas.create_text(lx, y - r,
                                     text=str(i + 1),
                                     font=("Arial", 9, "bold"),
                                     fill=COLOR_DARK, anchor=anchor)

    # ── Таблица ───────────────────────────────────────────────────────────

    def _update_table(self) -> None:
        sel_idx = self._selected_idx
        for item in self.tree.get_children():
            self.tree.delete(item)

        pts = self.points
        n   = len(pts)
        closed = self.closed_var.get() and n >= 3
        iids: List[str] = []

        for i, (x, y) in enumerate(pts):
            if i < n - 1 or closed:
                nx, ny = pts[(i + 1) % n]
                length = f"{math.hypot(nx - x, ny - y):.1f}"
            else:
                length = "—"
            iid = self.tree.insert("", tk.END,
                                    values=(i + 1,
                                            f"{x:.0f}",
                                            f"{y:.0f}",
                                            length))
            iids.append(iid)

        if sel_idx is not None and 0 <= sel_idx < len(iids):
            self.tree.selection_set(iids[sel_idx])
            self.tree.see(iids[sel_idx])

        total = sum(
            math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
            for i in range(n - 1)
        )
        if closed and n >= 2:
            total += math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1])

        self.summary_var.set(
            f"Точек: {n}   |   Длина: {total:.1f} px")

    # ── Очистка ───────────────────────────────────────────────────────────

    def _clear(self) -> None:
        self.points = []
        self._drag_idx = self._hover_idx = self._selected_idx = None
        self._refresh()


def main() -> None:
    root = tk.Tk()
    PolyEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
