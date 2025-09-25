import tkinter as tk

W, H = 1080, 920
BG = "#eaf3ff"

# Палитры для чередования цветов (ромб/прямоугольник)
COL_RH = ["#7fcdf2", "#9ae6a6", "#ffe184", "#c9a7f5"]
COL_RC = ["#5fb0ff", "#6cd9c8", "#ffbe55", "#9fe29f"]

go = False         # включение/выключение таймера кликом
depth = 1          # текущая глубина
d_dir = 1          # направление изменения глубины
DEPTH_MIN = 1
DEPTH_MAX = 15
DELAY = 80         # мс

def midpoint(x1, y1, x2, y2):
    return (x1 + x2) / 2.0, (y1 + y2) / 2.0

def romb_rect(xa, ya, xb, yb, xc, yc, xd, yd, n, is_romb=True, level=0):
    if n <= 0:
        return
    # Цвет в зависимости от типа фигуры и уровня
    if is_romb:
        fill = COL_RH[level % len(COL_RH)]
    else:
        fill = COL_RC[level % len(COL_RC)]

    # Рисуем текущий четырёхугольник (параллелограмм).
    # При старте это ромб, на следующем шаге из середины сторон получится прямоугольник и т.д.
    cvs.create_polygon(xa, ya, xb, yb, xc, yc, xd, yd,
                       fill=fill, outline="#2b2b2b", width=1, tags="fr")

    # Половинное деление рёбер — соединяем середины соседних сторон
    mAB = midpoint(xa, ya, xb, yb)
    mBC = midpoint(xb, yb, xc, yc)
    mCD = midpoint(xc, yc, xd, yd)
    mDA = midpoint(xd, yd, xa, ya)

    # Следующая фигура: тип чередуется
    romb_rect(*mAB, *mBC, *mCD, *mDA, n-1, not is_romb, level+1)

def draw(n):
    cvs.delete("fr")
    # Исходный ромб по центру
    cx, cy = W/2, H/2
    a = W * 0.36   # половина горизонтальной диагонали
    b = H * 0.28   # половина вертикальной диагонали
    # Вершины ромба (по часовой стрелке: верх, право, низ, лево)
    xa, ya = cx,      cy - b
    xb, yb = cx + a,  cy
    xc, yc = cx,      cy + b
    xd, yd = cx - a,  cy

    romb_rect(xa, ya, xb, yb, xc, yc, xd, yd, n, is_romb=True, level=0)

def animate():
    global depth, d_dir
    draw(depth)
    if not go:
        return
    depth += d_dir
    if depth >= DEPTH_MAX or depth <= DEPTH_MIN:
        d_dir *= -1
    root.after(DELAY, animate)

def click(_event):
    global go
    go = not go
    if go:
        animate()
    else:
        draw(depth)  # статическая отрисовка на текущей глубине

# GUI
root = tk.Tk()
root.title("ЛР2: Ромбы и прямоугольники (половинное деление рёбер)")
cvs = tk.Canvas(root, width=W, height=H, bg=BG, highlightthickness=0)
cvs.pack(fill="both", expand=True)
cvs.bind("<Button-1>", click)

# Начальная статическая картинка
draw(depth)

root.mainloop()