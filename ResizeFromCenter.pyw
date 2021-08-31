from time import sleep
import keyboard
# import mouse # was too slow / unreliable. used win32api directly instead
import numpy as np
import pywintypes
import win32api
import win32gui
import tkinter as tk
from utils.TransparentWindow import TransparentWindow

class OutlineWindow(TransparentWindow):
    def __init__(self) -> None:
        super().__init__()
    
    def create(self, x : int, y : int, w : int, h : int) -> None:
        super().create(geometry=(x,y,h,w),transparent_bg=True)
        _canvas = tk.Canvas(self._window, width=h, height=w, bg=self._window['bg'])
        _canvas.pack(fill="both", expand=True)
    
    def move(self, x : int, y : int, w : int, h : int):
        if self._window is not None:
            self._window.geometry(self.make_geometry(x,y,w,h))

def get_rect(hwnd : int) -> np.ndarray or None:
    try:
        return np.array(win32gui.GetWindowRect(hwnd))
    except pywintypes.error as e:
        if(e.args[0] != 1400): # invalid window handle
            raise e
        return None

def is_left_click_pressed() -> bool:
    return (win32api.GetKeyState(0x01) | 1) != 1 # 0 or 1 is up

def point_point_to_point_size(rect : np.ndarray) -> np.ndarray:
    return np.array([rect[0],rect[1],rect[2]-rect[0],rect[3]-rect[1]])

def mirror_point_point(rect : np.ndarray) -> np.ndarray:
    rect = np.copy(rect)
    if(rect[0]):
        rect[2] = -rect[0]
    else:
        rect[0] = -rect[2]
    if(rect[1]):
        rect[3] = -rect[1]
    else:
        rect[1] = -rect[3]
    
    return rect


if __name__ == "__main__":
    outline = OutlineWindow()
    while(True):
        if (is_left_click_pressed() and keyboard.is_pressed("ctrl")):
            foreground_hwnd = win32gui.GetForegroundWindow()
            last_rect = get_rect(foreground_hwnd)
            if (last_rect is not None):
                outline.create(*point_point_to_point_size(last_rect))
                while(is_left_click_pressed()):
                    rect = get_rect(foreground_hwnd)
                    if(rect is not None):
                        delta = rect-last_rect
                        new_rect = last_rect + mirror_point_point(delta)
                        if(new_rect[2] > new_rect[0] and  new_rect[3] > new_rect[1]):
                            outline.move(*point_point_to_point_size(new_rect))
                    outline.update()
                    sleep(0.01)
                outline.destroy()
                rect = get_rect(foreground_hwnd)
                if (rect is not None):
                    delta = rect-last_rect
                    if(not (delta[0] == delta[2] and delta[1] == delta[3]) # ignore window move
                        and np.count_nonzero(delta) <= 2): # the user can only control up to 2 coords, if more than 2 changed, it's probably something else
                        #calculate new position
                        new_rect = last_rect + mirror_point_point(delta)
                        # print(win32gui.GetWindowText(foreground_hwnd).split("-")[-1].strip(),last_rect,delta,new_rect)
                        win32gui.MoveWindow(foreground_hwnd,*point_point_to_point_size(new_rect),True)
        else:
            sleep(0.01)
