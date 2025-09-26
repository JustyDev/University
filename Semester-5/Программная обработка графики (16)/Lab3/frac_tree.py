from tkinter import *
import math
import random

def rgb(r, g, b):
    # Функция для перевода RGB-цвета в формат строки tkinter "#RRGGBB"
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    return f"#{r:02x}{g:02x}{b:02x}"

def grad_color(level, levels):
    # Генерация цвета с плавным переходом по глубине дерева (градиент)
    t = level / max(1, levels)
    r = int(90 * (1 - t) + 30 * t)
    g = int(60 * (1 - t) + 170 * t)
    b = int(40 * (1 - t) + 60 * t)
    return rgb(r, g, b)

def draw_mirrored(axis_x, x1, y1, x2, y2, color, width):
    # Рисуем одну ветку и её зеркальное отражение относительно вертикальной оси axis_x
    c.create_line(x1, y1, x2, y2, fill=color, width=width, capstyle="round")
    xm1 = 2 * axis_x - x1    # Отражение x1 относительно axis_x
    xm2 = 2 * axis_x - x2    # Отражение x2
    c.create_line(xm1, y1, xm2, y2, fill=color, width=width, capstyle="round")

def sym_tree(axis_x, x, y, length, angle_deg, depth, width, max_depth):
    # Рекурсивная функция для рисования симметричного бинарного дерева
    # axis_x — вертикальная ось зеркальной симметрии
    # x, y — начало ветви, length — длина, angle_deg — угол в градусах
    # depth — сколько слоёв рекурсии ещё рисовать
    if depth <= 0 or length < 2:
        return

    # Генерируем случайно углы и коэффициент уменьшения длины ветви для стохастичности, но они едины для пары ветвей — чтобы дерево было симметричным
    delta = random.uniform(15, 32)                # Угол отклонения ветки
    shrink = random.uniform(0.64, 0.78)           # Насколько короче следующая ветвь
    w2 = max(1.0, width * 0.76)                   # Сужаем толщину веток вниз по дереву
    color = grad_color(max_depth - depth, max_depth)  # Цвет ветви

    # Левая ветвь (+delta к углу)
    aL = math.radians(angle_deg + delta)
    xL = x + length * math.cos(aL)
    yL = y - length * math.sin(aL)
    draw_mirrored(axis_x, x, y, xL, yL, color, width)  # Рисуем ветку и её отражение
    sym_tree(axis_x, xL, yL, length * shrink, angle_deg + delta, depth - 1, w2, max_depth)  # Рекурсия

    # Правая ветвь (−delta к углу)
    aR = math.radians(angle_deg - delta)
    xR = x + length * math.cos(aR)
    yR = y - length * math.sin(aR)
    draw_mirrored(axis_x, x, y, xR, yR, color, width)
    sym_tree(axis_x, xR, yR, length * shrink, angle_deg - delta, depth - 1, w2, max_depth)

def click(event):
    # Обработчик клика мышкой: рисует аналоговое бинарное симметричное стохастическое дерево
    # Дерево не очищает холст, может быть наложено несколько деревьев
    axis_x = event.x                # Ось симметрии проходит через точку клика

    H = c.winfo_height()            # Высота текущего холста — для масштаба
    L = random.uniform(H * 0.11, H * 0.17)      # Длина ствола дерева (константа плюс стохастика)
    depth = random.randint(7, 9)                # Глубина дерева (случайно в диапазоне)
    width0 = random.uniform(3.5, 4.8)           # Толщина ствола (случайно)

    x0 = event.x                            # Начало ствола (по x — где кликнули)
    y0 = event.y                            # Начало ствола (по y — где кликнули)
    x1 = x0
    y1 = y0 - L                             # Верхушка ствола

    # Ствол дерева (одинарная вертикальная линия, по центру симметрии)
    c.create_line(x0, y0, x1, y1, fill=rgb(90, 60, 30), width=width0, capstyle="round")

    # Симметрично рекурсивно дорисовываем ветви
    sym_tree(axis_x, x1, y1, L * 0.75, 90, depth, width0 * 0.85, depth)

window = Tk()
window.title('Симметричный стохастический фрактал — дерево')
window.geometry('1000x600')

c = Canvas(window, bg='white')
c.pack(fill=BOTH, expand=1)

c.bind('<1>', click)  # Обработка левого клика мыши

window.mainloop()
