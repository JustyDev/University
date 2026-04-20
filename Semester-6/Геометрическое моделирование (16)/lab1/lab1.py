import tkinter as tk
import random
import math

# ── Константы ──────────────────────────────────────────────────────────────
CANVAS_W = 620
CANVAS_H = 520
BOTTOM_Y = 475          # y-координата нижней линии
CIRCLE_R = 22           # радиус синих кругов
RECT_W = 110            # ширина красного прямоугольника
RECT_H = 18             # высота красного прямоугольника
RECT_Y = BOTTOM_Y - RECT_H - 4   # y верхнего края прямоугольника
CIRCLES_PER_ROUND = 10   # сколько кругов в раунде
BASE_VY = 1.6           # начальная вертикальная скорость (пикс/кадр)
ACCEL = 0.038           # ускорение (пикс/кадр²)
TICK_MS = 15            # ≈67 FPS


class FallingCircle:
    """Один падающий синий круг."""

    def __init__(self, canvas: tk.Canvas, x: int, speed_mult: float) -> None:
        self.canvas = canvas
        self.x = x
        self.y = -CIRCLE_R           # стартует выше верхней границы
        self.vy = BASE_VY * speed_mult
        self.caught = False
        self.triggered_next = False  # уже запустил следующий круг?
        r = CIRCLE_R
        self.item = canvas.create_oval(
            x - r, -r, x + r, r,
            fill="#3a86ff", outline="#023e8a", width=2, tags="circle"
        )

    def step(self) -> None:
        self.vy += ACCEL
        self.y += self.vy
        r = CIRCLE_R
        self.canvas.coords(self.item,
                           self.x - r, self.y - r,
                           self.x + r, self.y + r)

    def remove(self) -> None:
        self.canvas.delete(self.item)


class CatchGame:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Поймай синие круги! — Лаб. 1, вариант 16")
        root.resizable(False, False)
        root.configure(bg="#1d2d44")

        # ── Верхняя панель ────────────────────────────────────────────────
        bar = tk.Frame(root, bg="#1d2d44")
        bar.pack(fill=tk.X, padx=8, pady=(6, 2))

        self.lbl_round = tk.Label(bar, text="Раунд: 1",
                                   font=("Arial", 14, "bold"),
                                   bg="#1d2d44", fg="#f8f9fa")
        self.lbl_round.pack(side=tk.LEFT)

        self.lbl_score = tk.Label(bar, text=f"Поймано: 0 / {CIRCLES_PER_ROUND}",
                                   font=("Arial", 14),
                                   bg="#1d2d44", fg="#f8f9fa")
        self.lbl_score.pack(side=tk.RIGHT)

        # ── Холст ─────────────────────────────────────────────────────────
        self.canvas = tk.Canvas(root, width=CANVAS_W, height=CANVAS_H,
                                 bg="#caf0f8", highlightthickness=0)
        self.canvas.pack(padx=8)

        # Нижняя зона-«земля»
        self.canvas.create_rectangle(0, BOTTOM_Y, CANVAS_W, CANVAS_H,
                                     fill="#e63946", outline="", tags="static")
        self.canvas.create_text(CANVAS_W // 2, BOTTOM_Y + 14,
                                text="▼  НИЖНЯЯ ГРАНИЦА  ▼",
                                font=("Arial", 10, "bold"),
                                fill="white", tags="static")

        # Красный прямоугольник (ракетка игрока)
        self.rect_x = CANVAS_W // 2
        self.rect_item = self.canvas.create_rectangle(
            self.rect_x - RECT_W // 2, RECT_Y,
            self.rect_x + RECT_W // 2, RECT_Y + RECT_H,
            fill="#e63946", outline="#9d0208", width=2
        )
        self.canvas.bind("<Motion>", self._on_mouse)

        # ── Нижняя панель ─────────────────────────────────────────────────
        bot = tk.Frame(root, bg="#1d2d44")
        bot.pack(fill=tk.X, padx=8, pady=(2, 6))

        self.lbl_status = tk.Label(bot, text="Нажмите «Начать» для старта",
                                    font=("Arial", 11), bg="#1d2d44", fg="#adb5bd")
        self.lbl_status.pack(side=tk.LEFT, padx=4)

        self.btn = tk.Button(bot, text="  Начать  ",
                              font=("Arial", 12, "bold"),
                              bg="#3a86ff", fg="white",
                              activebackground="#023e8a", activeforeground="white",
                              relief=tk.FLAT, cursor="hand2",
                              command=self._new_game)
        self.btn.pack(side=tk.RIGHT, padx=4)

        # ── Состояние игры ────────────────────────────────────────────────
        self._round = 1
        self._speed = 1.0
        self._circles: list = []
        self._spawned = 0
        self._caught = 0
        self._running = False
        self._after_id = None

    # ── Управление игрой ──────────────────────────────────────────────────

    def _new_game(self) -> None:
        """Сброс до первого раунда."""
        self._round = 1
        self._speed = 1.0
        self._start_round()

    def _start_round(self) -> None:
        self.canvas.delete("circle")
        self.canvas.delete("overlay")
        self._circles = []
        self._spawned = 0
        self._caught = 0
        self._running = True
        self.btn.config(state=tk.DISABLED)
        self._refresh_labels()
        self._spawn()
        self._tick()

    def _next_round(self) -> None:
        self._round += 1
        self._speed = round(self._speed * 1.25, 4)
        self._start_round()

    # ── Создание кругов ───────────────────────────────────────────────────

    def _spawn(self) -> None:
        """Добавить следующий круг (x — случайный)."""
        if self._spawned >= CIRCLES_PER_ROUND:
            return
        x = random.randint(CIRCLE_R + 12, CANVAS_W - CIRCLE_R - 12)
        self._circles.append(FallingCircle(self.canvas, x, self._speed))
        self._spawned += 1

    # ── Главный цикл ──────────────────────────────────────────────────────

    def _tick(self) -> None:
        if not self._running:
            return

        for c in self._circles:
            if c.caught:
                continue

            c.step()

            # Когда круг проходит половину пути до нижней линии — запустить следующий
            if not c.triggered_next and c.y >= BOTTOM_Y / 2:
                c.triggered_next = True
                self._spawn()

            # Пойман прямоугольником?
            if self._hits_rect(c):
                c.caught = True
                # Если круг ещё не активировал следующий — сделать это сейчас
                if not c.triggered_next:
                    c.triggered_next = True
                    self._spawn()
                c.remove()
                self._caught += 1
                self._refresh_labels()
                continue

            # Достиг нижней линии — игра окончена
            if c.y + CIRCLE_R >= BOTTOM_Y:
                self._end_game()
                return

        # Все круги раунда пойманы?
        if self._spawned >= CIRCLES_PER_ROUND and all(c.caught for c in self._circles):
            self._win_round()
            return

        self._after_id = self.root.after(TICK_MS, self._tick)

    # ── Определение столкновения ──────────────────────────────────────────

    def _hits_rect(self, c) -> bool:
        rx1 = self.rect_x - RECT_W // 2
        rx2 = self.rect_x + RECT_W // 2
        ry1 = RECT_Y
        ry2 = RECT_Y + RECT_H
        # Ближайшая точка прямоугольника к центру круга
        cx = max(rx1, min(c.x, rx2))
        cy = max(ry1, min(c.y, ry2))
        return math.hypot(c.x - cx, c.y - cy) < CIRCLE_R

    # ── Мышь ──────────────────────────────────────────────────────────────

    def _on_mouse(self, event: tk.Event) -> None:
        half = RECT_W // 2
        self.rect_x = max(half, min(event.x, CANVAS_W - half))
        self.canvas.coords(
            self.rect_item,
            self.rect_x - half, RECT_Y,
            self.rect_x + half, RECT_Y + RECT_H,
        )

    # ── Завершение раунда/игры ────────────────────────────────────────────

    def _win_round(self) -> None:
        self._running = False
        next_speed = self._speed * 1.25
        self._overlay(
            f"Раунд {self._round} пройден!",
            f"Скорость следующего раунда: ×{next_speed:.2f}",
            "#2dc653"
        )
        self.lbl_status.config(text=f"Раунд {self._round} завершён!")
        self.btn.config(state=tk.NORMAL, text="  Далее  ",
                        command=self._next_round)

    def _end_game(self) -> None:
        self._running = False
        if self._after_id:
            self.root.after_cancel(self._after_id)
            self._after_id = None
        self._overlay(
            "ИГРА ОКОНЧЕНА",
            f"Сыграно раундов: {self._round}",
            "#e63946"
        )
        self.lbl_status.config(text="Игра окончена!")
        self.btn.config(state=tk.NORMAL, text="  Заново  ",
                        command=self._new_game)

    def _overlay(self, title: str, subtitle: str, color: str) -> None:
        cx, cy = CANVAS_W // 2, CANVAS_H // 2
        # Полупрозрачный фон (белый прямоугольник)
        self.canvas.create_rectangle(cx - 220, cy - 55, cx + 220, cy + 55,
                                     fill="white", outline=color, width=3,
                                     tags="overlay")
        self.canvas.create_text(cx, cy - 18, text=title,
                                font=("Arial", 24, "bold"),
                                fill=color, tags="overlay")
        self.canvas.create_text(cx, cy + 22, text=subtitle,
                                font=("Arial", 13),
                                fill="#1d2d44", tags="overlay")

    # ── Обновление надписей ───────────────────────────────────────────────

    def _refresh_labels(self) -> None:
        self.lbl_round.config(text=f"Раунд: {self._round}")
        self.lbl_score.config(text=f"Поймано: {self._caught} / {CIRCLES_PER_ROUND}")


def main() -> None:
    root = tk.Tk()
    CatchGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
