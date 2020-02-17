import time

import win32con
import win32gui

from gameLib.game_ctl import GameControl
from gameLib.game_window import GameWindow

start = time.time()
while True:

    if time.time() - start >= 3300:
        hwndlist = GameWindow.get_game_hwnd()

        for item in hwndlist:
            win32gui.SendMessage(item, win32con.WM_DESTROY, 0, 0)