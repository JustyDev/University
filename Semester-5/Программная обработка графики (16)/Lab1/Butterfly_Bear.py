import tkinter as tk
import math

W, H = 900, 540
BG = "#e9f3ff"


class GroupObject:
    def __init__(self, cv, tag):
        self.cv = cv
        self.tag = tag
        self.x = 0
        self.y = 0

    def set_pos(self, x, y):
        dx, dy = x - self.x, y - self.y
        if dx or dy:
            self.cv.move(self.tag, dx, dy)
            self.x, self.y = x, y

    def move_by(self, dx, dy):
        self.cv.move(self.tag, dx, dy)
        self.x += dx
        self.y += dy


class Butterfly(GroupObject):
    def __init__(self, cv, x, y, s=1.0, tag="butterfly"):
        super().__init__(cv, tag)
        self.s = s
        self._build()
        self.set_pos(x, y)
        self.t = 0.0

    def _build(self):
        s = self.s
        t = self.tag

        # Тело
        bw, bh = 120*s, 36*s
        self.cv.create_oval(-bw/2, -bh/2, bw/2, bh/2,
                            fill="#5f4b3a", outline="#3d3129", width=2, tags=t)

        # Ножки
        self.cv.create_line(-20*s, bh/2, -32*s, bh/2+18*s, width=4, fill="#3d3129", tags=t)
        self.cv.create_line( 20*s, bh/2,  32*s, bh/2+18*s, width=4, fill="#3d3129", tags=t)

        # Голова
        hr = 16*s
        hx, hy = bw/2 + hr*0.8, -bh*0.10
        self.cv.create_oval(hx-hr, hy-hr, hx+hr, hy+hr,
                            fill="#6b5645", outline="#3d3129", width=2, tags=t)
        self.cv.create_line(hx, hy*3, hx+28*s, hy-34*s, width=3, fill="#3d3129", tags=t)
        self.cv.create_line(hx, hy*3, hx+12*s, hy-32*s, width=3, fill="#3d3129", tags=t)

        # Крылья
        wingL = [
            -6 * s, -bh / 2,  # нижняя внутренняя точка у тела
            -6 * s, -bh * 2.1,  # верхняя внутренняя точка (вертикальная кромка)
            -76 * s, -bh * 2.4,  # внешний верх
            -30 * s, -bh / 2  # внешний низ у тела
        ]
        self.cv.create_polygon(*wingL, fill="#ffcc66", outline="#8a5a00", width=3, tags=t)

        wingR = [
            6 * s, -bh / 2,
            6 * s, -bh * 2.1,
            76 * s, -bh * 2.4,
            30 * s, -bh / 2
        ]
        self.cv.create_polygon(*wingR, fill="#ffcc66", outline="#8a5a00", width=3, tags=t)

        # Овальные пятна
        def oval(cx, cy, r):
            self.cv.create_oval(cx - r, cy - r, cx + r, cy + r,
                                fill="#ff8", outline="#7a6d00", width=2, tags=t)

        oval(-35 * s, -bh * 1.68, 13 * s)
        oval(35 * s, -bh * 1.68, 13 * s)

        # Глаз
        self.cv.create_oval(hx+4*s, hy-4*s, hx+9*s, hy+1*s,
                            fill="black", outline="", tags=t)

    def update(self):
        self.t += 0.03
        x = W / 2 + 280 * math.sin(0.7 * self.t)
        y = H / 2 + 130 * math.sin(1.4 * self.t)
        self.set_pos(x, y)


class Bear(GroupObject):
    def __init__(self, cv, x, y, s=1.0, tag="bear"):
        super().__init__(cv, tag)
        self.s = s
        self._build()
        self.set_pos(x, y)
        self.vx, self.vy = 3.2, 2.4

    def _build(self):
        s = self.s
        t = self.tag

        body_w, body_h = 120 * s, 120 * s
        head_r = 32 * s

        # Тело
        self.cv.create_oval(-body_w / 2, -body_h / 2, body_w / 2, body_h / 2,
                            fill="#996633", outline="#5a3b1f", width=3, tags=t)

        # Голова
        hx, hy = 0, -body_h / 2 - head_r * 0.6
        self.cv.create_oval(hx - head_r, hy - head_r, hx + head_r, hy + head_r,
                            fill="#a06b3d", outline="#5a3b1f", width=3, tags=t)

        # Ушки
        er = 12 * s
        self.cv.create_oval(hx - 22 * s - er, hy - 22 * s - er, hx - 22 * s + er, hy - 22 * s + er,
                            fill="#a06b3d", outline="#5a3b1f", width=3, tags=t)
        self.cv.create_oval(hx + 22 * s - er, hy - 22 * s - er, hx + 22 * s + er, hy - 22 * s + er,
                            fill="#a06b3d", outline="#5a3b1f", width=3, tags=t)

        # Морда
        self.cv.create_oval(hx - 18 * s, hy - 6 * s, hx + 18 * s, hy + 16 * s,
                            fill="#d9b38c", outline="#5a3b1f", width=2, tags=t)
        # Нос
        self.cv.create_oval(hx - 6 * s, hy + 2 * s, hx + 6 * s, hy + 10 * s,
                            fill="black", outline="", tags=t)
        # Глаза
        self.cv.create_oval(hx - 12 * s, hy - 8 * s, hx - 6 * s, hy - 2 * s, fill="black", outline="", tags=t)
        self.cv.create_oval(hx + 6 * s, hy - 8 * s, hx + 12 * s, hy - 2 * s, fill="black", outline="", tags=t)

        # Лапы
        paw_r = 16 * s
        self.cv.create_oval(-body_w / 2 + 12 * s - paw_r, body_h / 2 - 8 * s - paw_r,
                            -body_w / 2 + 12 * s + paw_r, body_h / 2 - 8 * s + paw_r,
                            fill="#8f5f33", outline="#5a3b1f", width=2, tags=t)
        self.cv.create_oval(body_w / 2 - 12 * s - paw_r, body_h / 2 - 8 * s - paw_r,
                            body_w / 2 - 12 * s + paw_r, body_h / 2 - 8 * s + paw_r,
                            fill="#8f5f33", outline="#5a3b1f", width=2, tags=t)

    def update(self):
        # Прямолинейное движение с отражениями от границ Canvas
        self.move_by(self.vx, self.vy)
        l, t, r, b = self.cv.bbox(self.tag)

        if l < 0:
            self.move_by(-l, 0)
            self.vx = -self.vx
        elif r > W:
            self.move_by(W - r, 0)
            self.vx = -self.vx

        if t < 0:
            self.move_by(0, -t)
            self.vy = -self.vy
        elif b > H:
            self.move_by(0, H - b)
            self.vy = -self.vy


def main():
    root = tk.Tk()
    root.title("ЛР1: автоматическое перемещение группы объектов")
    cv = tk.Canvas(root, width=W, height=H, bg=BG, highlightthickness=0)
    cv.pack()

    butterfly = Butterfly(cv, x=W * 0.65, y=H * 0.55, s=1.1)
    bear = Bear(cv, x=W * 0.25, y=H * 0.65, s=1.0)

    def tick():
        butterfly.update()
        bear.update()
        # системный таймер, ~33 кадра/с
        root.after(25, tick)

    tick()
    root.mainloop()


if __name__ == "__main__":
    main()
