from tkinter import LEFT, RIGHT, X, Button, Frame, Label, Radiobutton, StringVar, Toplevel, colorchooser


class FillDialog(Toplevel):
    def __init__(self, master, current_fill="#88c0d0", current_type="solid"):
        super().__init__(master)
        self.title("Заливка контура")
        self.resizable(False, False)
        self.result = None
        self.color = current_fill or "#88c0d0"
        self.fill_type = StringVar(value=current_type if current_type != "none" else "solid")

        Label(self, text="Тип заливки").pack(anchor="w", padx=16, pady=(14, 4))
        for value, title in [
            ("none", "Без заливки"),
            ("solid", "Сплошная"),
            ("light", "Редкая штриховка"),
            ("medium", "Средняя штриховка"),
            ("dense", "Плотная штриховка"),
        ]:
            Radiobutton(self, text=title, variable=self.fill_type, value=value).pack(anchor="w", padx=16)

        color_frame = Frame(self)
        color_frame.pack(fill=X, padx=16, pady=10)
        self.sample = Label(color_frame, text="      ", bg=self.color, relief="sunken")
        self.sample.pack(side=LEFT)
        Button(color_frame, text="Выбрать цвет", command=self.choose_color).pack(side=LEFT, padx=8)

        btns = Frame(self)
        btns.pack(fill=X, padx=16, pady=(0, 14))
        Button(btns, text="OK", command=self.ok).pack(side=RIGHT, padx=(6, 0))
        Button(btns, text="Отмена", command=self.destroy).pack(side=RIGHT)

        self.grab_set()
        self.transient(master)

    def choose_color(self):
        value = colorchooser.askcolor(color=self.color, parent=self)
        if value and value[1]:
            self.color = value[1]
            self.sample.configure(bg=self.color)

    def ok(self):
        self.result = (self.fill_type.get(), self.color)
        self.destroy()

