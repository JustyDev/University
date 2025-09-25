from tkinter import *
import math
import random

def rgb(r, g, b):
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    return f"#{r:02x}{g:02x}{b:02x}"

def grad_color(level, levels):
    t = level / max(1, levels)
    r = int(90 * (1 - t) + 30 * t)
    g = int(60 * (1 - t) + 170 * t)
    b = int(40 * (1 - t) + 60 * t)
    return rgb(r, g, b)

def draw_mirrored(axis_x, x1, y1, x2, y2, color, width):
    c.create_line(x1, y1, x2, y2, fill=color, width=width, capstyle="round")
    xm1 = 2 * axis_x - x1
    xm2 = 2 * axis_x - x2
    c.create_line(xm1, y1, xm2, y2, fill=color, width=width, capstyle="round")

def sym_tree(axis_x, x, y, length, angle_deg, depth, width, max_depth):
    if depth <= 0 or length < 2:
        return

    # случайные параметры — общие для пары ветвей на этом узле
    delta = random.uniform(15, 32)
    shrink = random.uniform(0.64, 0.78)
    w2 = max(1.0, width * 0.76)
    color = grad_color(max_depth - depth, max_depth)

    # левая ветвь (+delta)
    aL = math.radians(angle_deg + delta)
    xL = x + length * math.cos(aL)
    yL = y - length * math.sin(aL)
    draw_mirrored(axis_x, x, y, xL, yL, color, width)
    sym_tree(axis_x, xL, yL, length * shrink, angle_deg + delta, depth - 1, w2, max_depth)

    # правая ветвь (−delta)
    aR = math.radians(angle_deg - delta)
    xR = x + length * math.cos(aR)
    yR = y - length * math.sin(aR)
    draw_mirrored(axis_x, x, y, xR, yR, color, width)
    sym_tree(axis_x, xR, yR, length * shrink, angle_deg - delta, depth - 1, w2, max_depth)

def click(event):
    # не очищаем холст — каждое новое дерево добавляется к предыдущим
    axis_x = event.x

    H = c.winfo_height()
    L = random.uniform(H * 0.11, H * 0.17)   # поменьше
    depth = random.randint(7, 9)             # немного меньше глубина
    width0 = random.uniform(3.5, 4.8)

    x0 = event.x
    y0 = event.y
    x1 = x0
    y1 = y0 - L

    # ствол (самосимметричен)
    c.create_line(x0, y0, x1, y1, fill=rgb(90, 60, 30), width=width0, capstyle="round")

    # симметричные ветви от верхушки
    sym_tree(axis_x, x1, y1, L * 0.75, 90, depth, width0 * 0.85, depth)

window = Tk()
window.title('Симметричный стохастический фрактал — дерево')
window.geometry('1000x600')

c = Canvas(window, bg='white')
c.pack(fill=BOTH, expand=1)

c.bind('<1>', click)

window.mainloop()