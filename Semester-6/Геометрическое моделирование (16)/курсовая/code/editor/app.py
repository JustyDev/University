import json
from pathlib import Path
from tkinter import (
    BOTH,
    BOTTOM,
    LEFT,
    TOP,
    X,
    Button,
    Canvas,
    Checkbutton,
    Frame,
    IntVar,
    Label,
    Menu,
    StringVar,
    filedialog,
    messagebox,
)

from .config import APP_TITLE, CANVAS_BG, SELECT_COLOR
from .dialogs import FillDialog
from .geometry import (
    arc_points_from_three,
    bbox_inside,
    bbox_intersects,
    distance,
    flatten,
    rect_from_points,
)
from .models import GraphicObject


class EditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.mode = StringVar(value="select")
        self.status = StringVar()
        self.snap_close = IntVar(value=1)
        self.objects = []
        self.selected_ids = set()
        self.temp_ids = []
        self.current_points = []
        self.drag_start = None
        self.file_path = None

        self.build_ui()
        self.bind_events()
        self.set_mode("select")

    def build_ui(self):
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self._build_file_menu()
        self._build_mode_menu()
        self._build_edit_menu()
        self._build_help_menu()
        self._build_toolbar()
        self._build_canvas()
        self._build_status_bar()

    def _build_file_menu(self):
        file_menu = Menu(self.menu, tearoff=False)
        file_menu.add_command(label="Новый", command=self.new_file)
        file_menu.add_command(label="Открыть...", command=self.open_file, accelerator="Cmd+O")
        file_menu.add_command(label="Сохранить", command=self.save_file, accelerator="Cmd+S")
        file_menu.add_command(label="Сохранить как...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        self.menu.add_cascade(label="Файл", menu=file_menu)

    def _build_mode_menu(self):
        mode_menu = Menu(self.menu, tearoff=False)
        for label, mode in [
            ("Выбор мышью", "select"),
            ("Рамка: полностью внутри", "select_inside"),
            ("Рамка: пересечение", "select_intersect"),
            ("Отрезок", "line"),
            ("Полилиния", "polyline"),
            ("Окружность", "circle"),
            ("Дуга по 3 точкам", "arc"),
            ("Удаление", "delete"),
        ]:
            mode_menu.add_command(label=label, command=lambda m=mode: self.set_mode(m))
        self.menu.add_cascade(label="Режим", menu=mode_menu)

    def _build_edit_menu(self):
        edit_menu = Menu(self.menu, tearoff=False)
        edit_menu.add_command(label="Удалить выбранное", command=self.delete_selected, accelerator="Backspace")
        edit_menu.add_command(label="Заливка выбранных контуров...", command=self.edit_fill)
        edit_menu.add_command(label="Снять выделение", command=self.clear_selection)
        self.menu.add_cascade(label="Правка", menu=edit_menu)

    def _build_help_menu(self):
        help_menu = Menu(self.menu, tearoff=False)
        help_menu.add_command(label="О программе", command=self.show_help)
        self.menu.add_cascade(label="Справка", menu=help_menu)

    def _build_toolbar(self):
        toolbar = Frame(self.root, padx=6, pady=6)
        toolbar.pack(side=TOP, fill=X)
        for text, mode in [
            ("Выбор", "select"),
            ("Внутри", "select_inside"),
            ("Пересечь", "select_intersect"),
            ("Отрезок", "line"),
            ("Полилиния", "polyline"),
            ("Окружность", "circle"),
            ("Дуга", "arc"),
            ("Удаление", "delete"),
        ]:
            Button(toolbar, text=text, command=lambda m=mode: self.set_mode(m)).pack(side=LEFT, padx=2)

        Button(toolbar, text="Заливка", command=self.edit_fill).pack(side=LEFT, padx=(12, 2))
        Button(toolbar, text="Удалить", command=self.delete_selected).pack(side=LEFT, padx=2)
        Checkbutton(toolbar, text="Замыкать полилинию", variable=self.snap_close).pack(side=LEFT, padx=12)

    def _build_canvas(self):
        self.canvas = Canvas(self.root, bg=CANVAS_BG, width=1100, height=680, highlightthickness=0)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)

    def _build_status_bar(self):
        footer = Frame(self.root)
        footer.pack(side=BOTTOM, fill=X)
        Label(footer, textvariable=self.status, anchor="w").pack(side=LEFT, fill=X, expand=True, padx=8, pady=5)

    def bind_events(self):
        self.canvas.bind("<Button-1>", self.on_left_down)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_up)
        self.canvas.bind("<Double-Button-1>", self.finish_polyline)
        self.canvas.bind("<Button-2>", self.cancel_current)
        self.canvas.bind("<Button-3>", self.cancel_current)
        self.root.bind("<Escape>", self.cancel_current)
        self.root.bind("<BackSpace>", lambda _event: self.delete_selected())
        self.root.bind("<Delete>", lambda _event: self.delete_selected())
        self.root.bind("<Command-s>", lambda _event: self.save_file())
        self.root.bind("<Command-o>", lambda _event: self.open_file())

    def set_mode(self, mode):
        self.mode.set(mode)
        self.cancel_current()
        messages = {
            "select": "Режим выбора: щёлкните объект. Shift добавляет к выделению.",
            "select_inside": "Режим рамки: выбраны объекты, полностью попавшие внутрь прямоугольника.",
            "select_intersect": "Режим рамки: выбраны объекты, которые пересекаются с прямоугольником.",
            "line": "Отрезок: нажмите и тяните мышью от начала к концу.",
            "circle": "Окружность: тяните мышью от центра к точке на окружности.",
            "arc": "Дуга: задайте три точки. Во время ввода видна тянущаяся линия.",
            "polyline": "Полилиния: щёлкайте точки. 1-й участок - отрезок, 2-й - дуга по 3 точкам; двойной щелчок завершает.",
            "delete": "Режим удаления: щёлкните объект, чтобы удалить его.",
        }
        self.status.set(messages.get(mode, ""))

    def clear_temp(self):
        for item in self.temp_ids:
            self.canvas.delete(item)
        self.temp_ids.clear()

    def cancel_current(self, _event=None):
        self.clear_temp()
        self.current_points.clear()
        self.drag_start = None

    def on_left_down(self, event):
        point = (event.x, event.y)
        mode = self.mode.get()
        if mode in ("line", "circle"):
            self.drag_start = point
        elif mode == "arc":
            self.current_points.append(point)
            if len(self.current_points) == 3:
                self.add_object(GraphicObject("arc", self.current_points.copy()))
                self.cancel_current()
            else:
                self.preview_points(point)
        elif mode == "polyline":
            self.add_polyline_point(point)
        elif mode in ("select_inside", "select_intersect"):
            self.drag_start = point
            self.clear_temp()
            rect = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline=SELECT_COLOR, dash=(4, 3))
            self.temp_ids.append(rect)
        elif mode == "select":
            self.select_at(point, add=bool(event.state & 0x0001))
        elif mode == "delete":
            obj = self.object_at(point)
            if obj:
                self.delete_objects({obj.obj_id})

    def on_drag(self, event):
        point = (event.x, event.y)
        mode = self.mode.get()
        if mode in ("line", "circle") and self.drag_start:
            self._preview_drag_shape(mode, point)
        elif mode in ("arc", "polyline"):
            self.preview_points(point)
        elif mode in ("select_inside", "select_intersect") and self.drag_start and self.temp_ids:
            self.canvas.coords(self.temp_ids[0], *rect_from_points(self.drag_start, point))

    def _preview_drag_shape(self, mode, point):
        self.clear_temp()
        if mode == "line":
            item = self.canvas.create_line(*flatten([self.drag_start, point]), fill=SELECT_COLOR, width=2, dash=(5, 3))
            self.temp_ids.append(item)
            return

        r = distance(self.drag_start, point)
        item = self.canvas.create_oval(
            self.drag_start[0] - r,
            self.drag_start[1] - r,
            self.drag_start[0] + r,
            self.drag_start[1] + r,
            outline=SELECT_COLOR,
            width=2,
            dash=(5, 3),
        )
        self.temp_ids.append(item)

    def on_left_up(self, event):
        point = (event.x, event.y)
        mode = self.mode.get()
        if mode == "line" and self.drag_start and distance(self.drag_start, point) > 2:
            self.add_object(GraphicObject("line", [self.drag_start, point]))
            self.cancel_current()
        elif mode == "circle" and self.drag_start and distance(self.drag_start, point) > 2:
            self.add_object(GraphicObject("circle", [self.drag_start, point]))
            self.cancel_current()
        elif mode in ("select_inside", "select_intersect") and self.drag_start:
            rect = rect_from_points(self.drag_start, point)
            self.select_by_rect(rect, partial=(mode == "select_intersect"))
            self.cancel_current()

    def add_polyline_point(self, point):
        if self.snap_close.get() and len(self.current_points) >= 3 and distance(self.current_points[0], point) < 12:
            self.current_points.append(self.current_points[0])
            self.finish_polyline()
            return
        self.current_points.append(point)
        self.preview_points(point)

    def finish_polyline(self, _event=None):
        if self.mode.get() != "polyline":
            return
        if len(self.current_points) >= 2:
            self.add_object(GraphicObject("polyline", self.current_points.copy()))
        self.cancel_current()

    def preview_points(self, point):
        self.clear_temp()
        if self.mode.get() == "arc" and self.current_points:
            self._preview_arc(point)
        elif self.mode.get() == "polyline" and self.current_points:
            self._preview_polyline(point)

    def _preview_arc(self, point):
        pts = self.current_points + [point]
        if len(pts) == 2:
            item = self.canvas.create_line(*flatten(pts), fill=SELECT_COLOR, width=2, dash=(5, 3))
        else:
            arc_pts = arc_points_from_three(*pts)
            item = self.canvas.create_line(*flatten(arc_pts), fill=SELECT_COLOR, width=2, dash=(5, 3), smooth=False)
        self.temp_ids.append(item)

    def _preview_polyline(self, point):
        obj = GraphicObject("polyline", self.current_points + [point], outline=SELECT_COLOR, width=2)
        pts = obj.polyline_render_points()
        item = self.canvas.create_line(
            *flatten(pts),
            fill=SELECT_COLOR,
            width=2,
            dash=(5, 3),
            capstyle="round",
            joinstyle="round",
        )
        self.temp_ids.append(item)

    def add_object(self, obj):
        self.objects.append(obj)
        obj.draw(self.canvas)
        self.clear_selection()
        self.select_object(obj.obj_id, add=True)

    def redraw_all(self):
        self.canvas.delete("all")
        for obj in self.objects:
            obj.draw(self.canvas)
        selected = set(self.selected_ids)
        self.selected_ids.clear()
        for obj_id in selected:
            self.select_object(obj_id, add=True)

    def object_at(self, point):
        items = self.canvas.find_overlapping(point[0] - 4, point[1] - 4, point[0] + 4, point[1] + 4)
        for item in reversed(items):
            for obj in self.objects:
                if item in obj.canvas_ids:
                    return obj
        return None

    def select_at(self, point, add=False):
        obj = self.object_at(point)
        if not add:
            self.clear_selection()
        if obj:
            if add and obj.obj_id in self.selected_ids:
                self.unselect_object(obj.obj_id)
            else:
                self.select_object(obj.obj_id, add=True)

    def select_by_rect(self, rect, partial):
        self.clear_selection()
        for obj in self.objects:
            bbox = self.object_bbox(obj)
            if not bbox:
                continue
            if (partial and bbox_intersects(bbox, rect)) or ((not partial) and bbox_inside(bbox, rect)):
                self.select_object(obj.obj_id, add=True)

    def object_bbox(self, obj):
        boxes = [self.canvas.bbox(item) for item in obj.canvas_ids]
        boxes = [b for b in boxes if b]
        if not boxes:
            return None
        return (
            min(b[0] for b in boxes),
            min(b[1] for b in boxes),
            max(b[2] for b in boxes),
            max(b[3] for b in boxes),
        )

    def select_object(self, obj_id, add=False):
        if not add:
            self.clear_selection()
        obj = self.by_id(obj_id)
        if not obj:
            return
        self.selected_ids.add(obj_id)
        for item in obj.canvas_ids:
            self.canvas.itemconfigure(item, width=obj.width + 2)
            if obj.kind in ("circle", "arc") or (obj.kind == "polyline" and obj.is_closed()):
                self.canvas.itemconfigure(item, outline=SELECT_COLOR)
            elif obj.kind in ("line", "polyline"):
                self.canvas.itemconfigure(item, fill=SELECT_COLOR)
        self.status.set(f"Выбрано объектов: {len(self.selected_ids)}")

    def unselect_object(self, obj_id):
        self.selected_ids.discard(obj_id)
        self.redraw_all()

    def clear_selection(self):
        if not self.selected_ids:
            return
        self.selected_ids.clear()
        self.redraw_all()
        self.status.set("Выделение снято.")

    def by_id(self, obj_id):
        return next((obj for obj in self.objects if obj.obj_id == obj_id), None)

    def delete_objects(self, ids):
        self.objects = [obj for obj in self.objects if obj.obj_id not in ids]
        self.selected_ids.difference_update(ids)
        self.redraw_all()
        self.status.set("Объекты удалены.")

    def delete_selected(self):
        if self.selected_ids:
            self.delete_objects(set(self.selected_ids))
        elif self.mode.get() != "delete":
            messagebox.showinfo(APP_TITLE, "Сначала выберите объекты для удаления.")

    def edit_fill(self):
        closed = [obj for obj in self.objects if obj.obj_id in self.selected_ids and obj.is_closed()]
        if not closed:
            messagebox.showinfo(APP_TITLE, "Выберите один или несколько замкнутых контуров: окружность или замкнутую полилинию.")
            return
        first = closed[0]
        dialog = FillDialog(self.root, first.fill or "#88c0d0", first.fill_type)
        self.root.wait_window(dialog)
        if not dialog.result:
            return
        fill_type, color = dialog.result
        for obj in closed:
            obj.fill_type = fill_type
            obj.fill = "" if fill_type == "none" else color
        self.redraw_all()
        self.status.set(f"Заливка изменена для контуров: {len(closed)}")

    def new_file(self):
        if not self.confirm_discard():
            return
        self.objects.clear()
        self.selected_ids.clear()
        self.file_path = None
        self.redraw_all()
        self.status.set("Создан новый документ.")

    def confirm_discard(self):
        return messagebox.askyesno(APP_TITLE, "Продолжить? Несохранённые изменения текущего рисунка могут быть потеряны.")

    def open_file(self):
        if not self.confirm_discard():
            return
        path = filedialog.askopenfilename(
            title="Открыть рисунок",
            filetypes=[("Файлы редактора", "*.json"), ("Все файлы", "*.*")],
        )
        if not path:
            return
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            self.objects = [GraphicObject.from_dict(item) for item in data.get("objects", [])]
            self.selected_ids.clear()
            self.file_path = path
            self.redraw_all()
            self.status.set(f"Файл открыт: {path}")
        except Exception as exc:
            messagebox.showerror(APP_TITLE, f"Не удалось открыть файл:\n{exc}")

    def save_file(self):
        if not self.file_path:
            return self.save_file_as()
        self.write_file(self.file_path)

    def save_file_as(self):
        path = filedialog.asksaveasfilename(
            title="Сохранить рисунок",
            defaultextension=".json",
            filetypes=[("Файлы редактора", "*.json"), ("Все файлы", "*.*")],
        )
        if not path:
            return
        self.file_path = path
        self.write_file(path)

    def write_file(self, path):
        data = {"version": 1, "objects": [obj.to_dict() for obj in self.objects]}
        try:
            Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            self.status.set(f"Файл сохранён: {path}")
        except Exception as exc:
            messagebox.showerror(APP_TITLE, f"Не удалось сохранить файл:\n{exc}")

    def show_help(self):
        messagebox.showinfo(
            APP_TITLE,
            "Лабораторная работа 1: графический редактор.\n\n"
            "Режимы выбираются через меню или кнопки. "
            "Отрезок и окружность строятся перетаскиванием мыши. "
            "Дуга задаётся тремя точками. "
            "Полилиния состоит из чередующихся отрезков и дуг по трём точкам; завершение - двойной щелчок. "
            "Замкнутые контуры можно заливать через Правка -> Заливка.",
        )

