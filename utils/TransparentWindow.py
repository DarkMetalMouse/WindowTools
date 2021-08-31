import tkinter as tk

class TransparentWindow:
    def __init__(self) -> None:
        self._root = None
        self._window = None
    
    @staticmethod
    def make_geometry(x : int, y : int, w : int, h : int) -> str:
        # e.g.: "100x100+1800+920"
        return f"{w}x{h}+{x}+{y}"
    
    def create(self, geometry : tuple = (100,100,100,100), alpha : float = 0.7, transparent_bg : bool = False, bg : str = "white") -> None:
        self._root = tk.Tk()
        self._root.iconify()
        self._root.withdraw()

        self._window = tk.Toplevel(self._root)
        self._window.geometry(self.make_geometry(*geometry))
        self._window.overrideredirect(1)  # Remove border
        # self._window.attributes('-topmost', 1)
        self._window.attributes('-alpha', alpha)
        # self._window.lift()
        self._window.attributes("-topmost", True)
        # self._window.attributes("-disabled", True)
        if transparent_bg:
            self._window.configure(bg=bg)
            self._window.attributes("-transparentcolor", self._window['bg'])

    
    def destroy(self):
        if self._root is not None:
            self._root.destroy()
            self._root = None
    
    def update(self):
        if self._root is not None:
            self._root.update()
    
    def is_displaying(self) -> bool:
        return self._root is not None