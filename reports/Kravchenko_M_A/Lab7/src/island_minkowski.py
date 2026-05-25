# pylint: disable=too-many-arguments, too-many-positional-arguments, too-many-locals, too-many-ancestors, too-few-public-methods, line-too-long
"""
Фрактал: Остров Минковского
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
from datetime import datetime
from PIL import ImageGrab


class MinkowskiIsland:
    """Генератор фрактала Остров Минковского."""

    def __init__(self, level: int, scale: float = 1.0):
        self.level = level
        self.scale = scale
        self.points = []

    def generate(self, cx: float, cy: float, size: float):
        """Генерация острова из 4 сторон."""
        self.points = []
        s = size
        self._gen_side(cx - s, cy - s, cx + s, cy - s)
        self._gen_side(cx + s, cy - s, cx + s, cy + s)
        self._gen_side(cx + s, cy + s, cx - s, cy + s)
        self._gen_side(cx - s, cy + s, cx - s, cy - s)
        return self.points

    def _gen_side(self, x1: float, y1: float, x2: float, y2: float):
        """Рекурсивная генерация одной стороны."""
        self._gen_side_rec(x1, y1, x2, y2, self.level)

    def _gen_side_rec(self, x1: float, y1: float, x2: float, y2: float, lvl: int):
        """Рекурсивная генерация с уровнем."""
        if lvl == 0:
            self.points.append((x1, y1))
            self.points.append((x2, y2))
            return

        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)

        if length < 0.1:
            self.points.append((x1, y1))
            self.points.append((x2, y2))
            return

        ux = dx / length
        uy = dy / length
        px = -uy
        py = ux
        spike = length / 3.0 * self.scale
        t = length / 3.0
        tt = length * 2.0 / 3.0

        p2x = x1 + ux * t
        p2y = y1 + uy * t
        p3x = p2x + px * spike
        p3y = p2y + py * spike
        p4x = p2x + ux * t + px * spike
        p4y = p2y + uy * t + py * spike
        p5x = x1 + ux * tt
        p5y = y1 + uy * tt
        p6x = p5x - px * spike
        p6y = p5y - py * spike
        p7x = p5x + ux * t - px * spike
        p7y = p5y + uy * t - py * spike

        nl = lvl - 1
        self._gen_side_rec(x1, y1, p2x, p2y, nl)
        self._gen_side_rec(p2x, p2y, p3x, p3y, nl)
        self._gen_side_rec(p3x, p3y, p4x, p4y, nl)
        self._gen_side_rec(p4x, p4y, p5x, p5y, nl)
        self._gen_side_rec(p5x, p5y, p6x, p6y, nl)
        self._gen_side_rec(p6x, p6y, p7x, p7y, nl)
        self._gen_side_rec(p7x, p7y, x2, y2, nl)

    def get_point_count(self) -> int:
        """Вернуть количество точек."""
        return len(self.points)

    def clear(self):
        """Очистить точки."""
        self.points = []


class FractalCanvas(tk.Canvas):
    """Канва для рисования фрактала."""

    def __init__(self, parent, width=800, height=600):
        super().__init__(parent, width=width, height=height, bg="white")
        self.points = []
        self.zoom = 1.0
        self.off_x = 0.0
        self.off_y = 0.0
        self.last_x = None
        self.last_y = None

        self.bind("<Button-1>", self._on_press)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<MouseWheel>", self._on_zoom)

    def set_points(self, pts):
        """Установить точки для отрисовки."""
        self.points = pts
        self._redraw()

    def reset(self):
        """Сбросить масштаб и позицию."""
        self.zoom = 1.0
        self.off_x = 0.0
        self.off_y = 0.0
        self._redraw()

    def zoom_in(self):
        """Приблизить."""
        self.zoom *= 1.2
        self._redraw()

    def zoom_out(self):
        """Отдалить."""
        self.zoom /= 1.2
        self._redraw()

    def _on_press(self, e):
        self.last_x = e.x
        self.last_y = e.y

    def _on_drag(self, e):
        if self.last_x is not None:
            dx = e.x - self.last_x
            dy = e.y - self.last_y
            self.off_x += dx / self.zoom
            self.off_y += dy / self.zoom
            self.last_x = e.x
            self.last_y = e.y
            self._redraw()

    def _on_zoom(self, e):
        if e.delta > 0:
            self.zoom *= 1.1
        else:
            self.zoom /= 1.1
        self.zoom = max(0.1, min(10.0, self.zoom))
        self._redraw()

    def _to_screen(self, x, y):
        w = self.winfo_width()
        h = self.winfo_height()
        sx = w // 2 + x * self.zoom + self.off_x * self.zoom
        sy = h // 2 + y * self.zoom + self.off_y * self.zoom
        return int(sx), int(sy)

    def _redraw(self):
        self.delete("all")
        if len(self.points) < 2:
            return
        for i in range(len(self.points) - 1):
            x1, y1 = self._to_screen(self.points[i][0], self.points[i][1])
            x2, y2 = self._to_screen(self.points[i + 1][0], self.points[i + 1][1])
            self.create_line(x1, y1, x2, y2, fill="#0066cc", width=2)
        self._draw_info()

    def _draw_info(self):
        h = self.winfo_height()
        txt = f"Точек: {len(self.points)} | Масштаб: {self.zoom:.1f}x"
        txt += " | Колесико - масштаб, ЛКМ - панорамирование"
        self.create_text(10, h - 20, anchor="sw", text=txt, font=("Arial", 9), fill="gray")


class App:
    """Главное окно."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Фрактал - Остров Минковского")
        self.root.geometry("1200x700")

        self.level_var = tk.IntVar(value=2)
        self.size_var = tk.IntVar(value=200)
        self.scale_var = tk.DoubleVar(value=1.0)

        self.canvas = None
        self._setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_ui(self):
        main = ttk.Frame(self.root)
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left = ttk.Frame(main, width=300)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left.pack_propagate(False)

        self.canvas = FractalCanvas(main, 800, 600)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._make_controls(left)

    def _make_controls(self, parent):
        # Параметры
        frame = ttk.LabelFrame(parent, text="Параметры")
        frame.pack(fill=tk.X, padx=5, pady=5)

        row = 0
        ttk.Label(frame, text="Глубина (0-5):").grid(row=row, column=0, padx=5, pady=5)
        ttk.Spinbox(frame, from_=0, to=5, textvariable=self.level_var, width=8).grid(row=row, column=1, padx=5, pady=5)
        row += 1

        ttk.Label(frame, text="Размер (50-400):").grid(row=row, column=0, padx=5, pady=5)
        ttk.Spinbox(frame, from_=50, to=400, textvariable=self.size_var, width=8).grid(
            row=row, column=1, padx=5, pady=5
        )
        row += 1

        ttk.Label(frame, text="Масштаб шипов:").grid(row=row, column=0, padx=5, pady=5)
        ttk.Spinbox(frame, from_=0.5, to=1.5, increment=0.1, textvariable=self.scale_var, width=8).grid(
            row=row, column=1, padx=5, pady=5
        )
        row += 1

        btn = ttk.Button(frame, text="Сгенерировать", command=self._gen)
        btn.grid(row=row, column=0, columnspan=2, pady=10, sticky="ew")

        # Вид
        frame = ttk.LabelFrame(parent, text="Вид")
        frame.pack(fill=tk.X, padx=5, pady=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="+", width=3, command=self.canvas.zoom_in).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="-", width=3, command=self.canvas.zoom_out).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Сброс", width=5, command=self.canvas.reset).pack(side=tk.LEFT, padx=2)

        # Скриншот
        frame = ttk.LabelFrame(parent, text="Скриншот")
        frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(frame, text="Сделать скриншот", command=self._shot).pack(pady=5)

        # Инфо
        frame = ttk.LabelFrame(parent, text="О фрактале")
        frame.pack(fill=tk.X, padx=5, pady=5)

        txt = tk.Text(frame, height=8, wrap=tk.WORD)
        txt.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        txt.insert(
            tk.END,
            "Остров Минковского - классический фрактал.\n\n"
            "Глубина: количество итераций (0-5)\n"
            "Размер: сторона квадрата (50-400)\n"
            "Масштаб шипов: размер выступов (0.5-1.5)",
        )
        txt.config(state=tk.DISABLED)

    def _gen(self):
        lvl = self.level_var.get()
        sz = self.size_var.get()
        sc = self.scale_var.get()

        if lvl < 0 or lvl > 5:
            messagebox.showerror("Ошибка", "Глубина от 0 до 5")
            return

        fractal = MinkowskiIsland(lvl, sc)
        pts = fractal.generate(0, 0, sz)
        self.canvas.set_points(pts)
        self.canvas.reset()

    def _shot(self):
        name = f"fractal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        img.save(name)
        messagebox.showinfo("Скриншот", f"Сохранен: {name}")

    def _on_close(self):
        self.root.destroy()

    def run(self):
        """Запуск приложения."""
        self.root.mainloop()


if __name__ == "__main__":
    App().run()
