import threading

import win32gui

from gameLib.game_ctl import GameControl
from gameLib.game_window import GameWindow
from explore.driver_explore import DriverExplore
from explore.passenger_explore import PassengerExplore
import logging

class DualExplore():

    def __init__(self):

        # 初始化窗口信息
        hwndlist = GameWindow.get_game_hwnd()

        # 检测窗口信息是否正确
        num = len(hwndlist)
        if num == 2:
           logging.info('检测到两个窗口，窗口信息正常')
        else:
            logging.warning('检测到'+str(num)+'个窗口，窗口信息异常！')

        # 初始化司机和打手
        for hwnd in hwndlist:
            yys = GameControl(hwnd)
            if yys.find_multi_game_img('img/JI-XU.png', 'img/YAO-QING.png'):
                self.driver = DriverExplore(hwnd=hwnd)
                hwndlist.remove(hwnd)
                logging.info('发现司机')

        self.passenger = PassengerExplore(hwnd=hwndlist[0])
        logging.info('发现乘客')

    def start(self):
        task1 = threading.Thread(target=self.driver.start)
        task2 = threading.Thread(target=self.passenger.start)
        task1.start()
        task2.start()

        task1.join()
        task2.join()