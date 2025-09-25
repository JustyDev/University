from tkinter import *
import math
import random

def fractal(x1, y1, x2, y2, num, max_depth=8):
    # углы и коэффициенты
    a = 0.2
    b = 1.2
    s1, c1 = math.sin(a), math.cos(a)
    s2, c2 = math.sin(b), math.cos(b)
    k = 0.2
    k1 = 0.5

    if num >= max_depth:
        return

    # 3 — поворот точки 2 вокруг 1 на угол a
    vx, vy = (x2 - x1), (y2 - y1)
    x3 = vx * c1 - vy * s1 + x1
    y3 = vx * s1 + vy * c1 + y1

    # 4 — деление 1–3 по k
    x4 = x1 * (1 - k) + x3 * k
    y4 = y1 * (1 - k) + y3 * k

    # 5 — деление 4–3 по k1
    x5 = x4 * (1 - k1) + x3 * k1
    y5 = y4 * (1 - k1) + y3 * k1

    # 6,7 — поворот 5 вокруг 4 на ±b
    ux, uy = (x5 - x4), (y5 - y4)
    x6 = ux * c2 - uy * s2 + x4
    y6 = ux * s2 + uy * c2 + y4
    x7 = ux * c2 + uy * s2 + x4
    y7 = -ux * s2 + uy * c2 + y4

    # рисуем сегмент 1–4
    hex_rand = f"#{10:02X}{random.randrange(255):02X}{10:02X}"
    c.create_line(x1, y1, x4, y4, fill=hex_rand, width=1)

    # рекурсия
    fractal(x4, y4, x3, y3, num + 1, max_depth)
    fractal(x4, y4, x6, y6, num + 1, max_depth)
    fractal(x4, y4, x7, y7, num + 1, max_depth)

def click(event):
    x = event.x
    y = event.y
    fractal(x, y, x - random.randrange(300), y - random.randrange(400), 0)

window = Tk()
window.title('Стохастический фрактал')
window.geometry('1000x600')

c = Canvas(window, bg='white')
c.pack(fill=BOTH, expand=1)

c.bind('<1>', click)

window.mainloop()