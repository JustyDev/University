import tkinter as tk

W, H = 1080, 920                # Размеры холста (ширина, высота)
BG = "#eaf3ff"                  # Цвет фона холста

# Палитры цветов для ромба и прямоугольника
COL_RH = ["#7fcdf2", "#9ae6a6", "#ffe184", "#c9a7f5"]   # Цвета для ромбов
COL_RC = ["#5fb0ff", "#6cd9c8", "#ffbe55", "#9fe29f"]   # Цвета для прямоугольников

go = False         # Флаг - идёт/не идёт анимация (изменяется щелчком мыши)
depth = 1          # Текущая глубина рекурсии/рисования
d_dir = 1          # Направление изменения глубины (+1 или -1)
DEPTH_MIN = 1      # Минимальная глубина
DEPTH_MAX = 15     # Максимальная глубина
DELAY = 80         # Задержка (мс) между кадрами

def midpoint(x1, y1, x2, y2):
    # Возвращает координаты середины отрезка между (x1, y1) и (x2, y2)
    return (x1 + x2) / 2.0, (y1 + y2) / 2.0

def romb_rect(xa, ya, xb, yb, xc, yc, xd, yd, n, is_romb=True, level=0):
    """
    Рекурсивная функция для рисования последовательности вложенных ромбов и прямоугольников.
    (xa, ya), ..., (xd, yd) - координаты четырёх вершин.
    n - оставшаяся глубина рекурсии.
    is_romb - текущая фигура (ромб или прямоугольник).
    level - уровень глубины (для выбора цвета).
    """
    if n <= 0:
        return

    # Определяем цвет текущей фигуры по типу и уровню рекурсии
    if is_romb:
        fill = COL_RH[level % len(COL_RH)]
    else:
        fill = COL_RC[level % len(COL_RC)]

    # Рисуем четырёхугольник (ромб или прямоугольник)
    cvs.create_polygon(xa, ya, xb, yb, xc, yc, xd, yd,
                       fill=fill, outline="#2b2b2b", width=1, tags="fr")

    # Находим середины рёбер
    mAB = midpoint(xa, ya, xb, yb)
    mBC = midpoint(xb, yb, xc, yc)
    mCD = midpoint(xc, yc, xd, yd)
    mDA = midpoint(xd, yd, xa, ya)

    # Рекурсивно вызываем функцию для внутренней фигуры, чередуем тип (ромб/прямоугольник)
    romb_rect(*mAB, *mBC, *mCD, *mDA, n-1, not is_romb, level+1)

def draw(n):
    # Очищаем холст и рисуем начальный ромб с вложенными фигурами заданной глубины n
    cvs.delete("fr")
    # Центр и размеры исходного ромба
    cx, cy = W/2, H/2
    a = W * 0.36   # Половина горизонтальной диагонали
    b = H * 0.28   # Половина вертикальной диагонали

    # Координаты вершин ромба (по часовой стрелке: верх, право, низ, лево)
    xa, ya = cx,      cy - b
    xb, yb = cx + a,  cy
    xc, yc = cx,      cy + b
    xd, yd = cx - a,  cy

    # Запускаем рекурсивную отрисовку
    romb_rect(xa, ya, xb, yb, xc, yc, xd, yd, n, is_romb=True, level=0)

def animate():
    """
    Анимация: изменяем глубину на каждом кадре,
    инвертируем направление при достижении границ
    """
    global depth, d_dir
    draw(depth)
    if not go:      # Если анимация выключена - ничего не делаем
        return
    depth += d_dir
    if depth >= DEPTH_MAX or depth <= DEPTH_MIN:
        d_dir *= -1     # Разворачиваем "анимацию" в другую сторону
    root.after(DELAY, animate)   # Планируем следующий кадр

def click(_event):
    """
    Обработчик щелчка мыши: включает/выключает анимацию.
    """
    global go
    go = not go
    if go:
        animate()
    else:
        draw(depth)  # Показываем статическую картинку для текущей глубины

# --- GUI ---
root = tk.Tk()
root.title("ЛР2: Ромбы и прямоугольники (половинное деление рёбер)")
cvs = tk.Canvas(root, width=W, height=H, bg=BG, highlightthickness=0)
cvs.pack(fill="both", expand=True)
cvs.bind("<Button-1>", click)   # Привязываем обработчик нажатия мышки

# Отрисовываем картинку для начальной глубины
draw(depth)

root.mainloop()
