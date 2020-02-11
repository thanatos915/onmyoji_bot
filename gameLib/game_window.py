import win32gui


class GameWindow:
    # 阴阳师窗口句柄
    yys_hwnd = []

    @staticmethod
    def __my_call_back(hwnd, extra):
        """
        获取所有阴阳师窗口
        :param hwnd:
        :param extra:
        :return:
        """
        windows = extra
        window = [hwnd, win32gui.GetClassName(hwnd), win32gui.GetWindowText(hwnd)]
        windows[hwnd] = window

    @staticmethod
    def get_game_hwnd() -> list:
        """
        获取游戏窗体句柄并返回，同时保存在类静态成员变量下
        :return:
        """
        windows = {}
        win32gui.EnumWindows(GameWindow.__my_call_back, windows)
        yys_hwnd = []
        for key, window in windows.items():
            if window[2] == u'阴阳师-网易游戏':
                yys_hwnd.append(window[0])
        GameWindow.yys_hwnd = yys_hwnd
        return yys_hwnd
