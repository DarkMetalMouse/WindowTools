'''
Switches all open windows from one display to the other
'''
import win32con
import win32gui
import win32api


def getMonSize(id):
    mon = win32api.EnumDisplayMonitors()[id][2]
    return (mon[2] - mon[0], mon[3] - mon[1])


SIZES = (getMonSize(0), getMonSize(1))


def isRealWindow(hwnd):
    '''Return True if given window is a real Windows application window.
    function from https://stackoverflow.com/a/152454/9721937'''
    if not win32gui.IsWindowVisible(hwnd):
        return False
    if win32gui.GetParent(hwnd) != 0:
        return False
    hasNoOwner = win32gui.GetWindow(hwnd, win32con.GW_OWNER) == 0
    lExStyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
            or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
        if win32gui.GetWindowText(hwnd):
            return True
    return False


def moveWindows(hwnd, extra):
    if isRealWindow(hwnd):
        rect = win32gui.GetWindowRect(hwnd)
        if rect[0] >= SIZES[0][0] - 8:  # why 8? because Windows is quirky and special
            # window in 2nd screen
            ratios = ((SIZES[1][0] / SIZES[0][0]), (SIZES[0][1] / SIZES[1][1]))
            x = round((rect[0] - SIZES[1][0]) * ratios[0])
        else:
            # window in 1st screen
            ratios = ((SIZES[0][0] / SIZES[1][0]), (SIZES[1][1] / SIZES[0][1]))
            x = round((rect[0] * ratios[0]) + SIZES[0][0])

        y = round(rect[1] * ratios[1])
        w = round((rect[2] - rect[0]) * ratios[0])
        h = round((rect[3] - rect[1]) * ratios[1])

        win32gui.MoveWindow(hwnd, x, y, w, h, True)


if __name__ == "__main__":
    win32gui.EnumWindows(moveWindows, None)
