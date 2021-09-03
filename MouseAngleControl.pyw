'''
Move the curser in a straight line with a certain angle determined by a GUI
Change the constants to fit your preferred key bindings
'''

from utils.TransparentWindow import TransparentWindow
import keyboard
import mouse
import tkinter as tk
from time import time, sleep
from math import radians, cos, sin

TOGGLE_WINDOW_KEY = 'f15'
INCREASE_ANGLE_KEY = 'f17'
DECREASE_ANGLE_KEY = 'f18'
MOVE_FORWARD_KEY = 'f19'
MOVE_BACKWARDS_KEY = 'f20'
MODIFIER_KEY = 'ctrl'

class BriefWindow(TransparentWindow):
    def __init__(self, time_to_live: int, geometry: tuple = (1800,920,100,100)) -> None:
        super().__init__()
        self._geometry = geometry
        self._text = None
        self._after = None
        self._time_to_live = time_to_live

    def set_display_value(self, value: int):
        if self._root is None:
            self._create()

        if self._after is not None:
            self._root.after_cancel(self._after)
        if self._time_to_live > 0:
            self._after = self._root.after(self._time_to_live, self.destroy)

        self._text.set(str(value))
        self._make_line(deg)

    def _create(self) -> None:
        super().create(self._geometry)

        self._window.grid_rowconfigure(0, weight=1)
        self._window.grid_columnconfigure(0, weight=1)
        self._text = tk.StringVar()

        label = tk.Label(self._window,
                         textvariable=self._text,
                         font=("Consolas", 16), fg="black")

        label.grid(row=0, column=0)
        self._canvas = tk.Canvas(self._window, height=50, width=50)
        self._canvas.grid(row=1, column=0)

    def _make_line(self, deg):
        center = (25, 25)
        x1 = center[0] - cos(radians(deg)) * 20
        y1 = center[1] - sin(radians(deg)) * 20
        x2 = center[0] + cos(radians(deg)) * 20
        y2 = center[1] + sin(radians(deg)) * 20
        self._canvas.delete("all")
        # self._canvas.create_line(
        #     x1, y1, x2, y2, fill="#CCCCCC", width=3.5, arrow=tk.LAST)
        self._canvas.create_line(
            x1, y1, x2, y2, fill="#000000", width=3, arrow=tk.LAST)

    def set_ttl(self, ttl: int) -> None:
        self._time_to_live = ttl

    def get_ttl(self) -> int:
        return self._time_to_live


class KeyHandler:
    START_INTERVAL = 0.35
    LOOP_INTERVAL = 0.025

    def __init__(self, key: str) -> None:
        self._key = key
        self._press_start_time = 0
        self._press_time = 0
        self._is_down = False
        self._last_time = 0

    def is_pressed(self) -> bool:
        if not keyboard.is_pressed(self._key):
            self._is_down = False
            return False
        if not self._is_down:
            self._is_down = True
            self._first_press = True
            self._press_start_time = time()
            # self._press_time = time()

            return True
        self._first_press = False
        if (time() - self._press_start_time) > KeyHandler.START_INTERVAL:
            if (time() - self._press_time) > KeyHandler.LOOP_INTERVAL:
                self._press_time = time()
                return True

        return False

    def is_first(self) -> bool:
        return self._first_press


def move_mouse(key: KeyHandler) -> None:
    global virtualpos
    if key.is_first():
        if tuple([int(x) for x in virtualpos]) != mouse.get_position():
            virtualpos = list(mouse.get_position())
    mul = 1 if key is f19 else -1
    virtualpos[0] += cos(radians(deg)) * mul
    virtualpos[1] += sin(radians(deg)) * mul

    mouse.move(virtualpos[0], virtualpos[1])


TIME_TO_LIVE = 2000  # ms
window = BriefWindow(TIME_TO_LIVE)
deg = 0
virtualpos = list(mouse.get_position())
f15 = KeyHandler(TOGGLE_WINDOW_KEY)
f17 = KeyHandler(INCREASE_ANGLE_KEY)
f18 = KeyHandler(DECREASE_ANGLE_KEY)
f19 = KeyHandler(MOVE_FORWARD_KEY)
f20 = KeyHandler(MOVE_BACKWARDS_KEY)

while True:
    if f15.is_pressed():
        if window.is_displaying():
            if window.get_ttl() == -1:
                window.set_ttl(TIME_TO_LIVE)
                window.destroy()
            else:
                window.destroy()
        else:
            window.set_ttl(-1)
            window.set_display_value(deg)
    if f17.is_pressed():
        deg = (deg + (45 if keyboard.is_pressed(MODIFIER_KEY) else 5)) % 360
        window.set_display_value(str(deg))
    elif f18.is_pressed():
        deg = (deg - (45 if keyboard.is_pressed(MODIFIER_KEY) else 5)) % 360
        window.set_display_value(str(deg))

    if f19.is_pressed():
        move_mouse(f19)
    if f20.is_pressed():
        move_mouse(f20)

    window.update()
    sleep(0.01)
