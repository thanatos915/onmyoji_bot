import os

import cv2

from gameLib.fighter import Fighter
from explore.explore_fight import ExploreFight
import tools.utilities as ut
from tools.game_pos import CommonPos, TansuoPos

import configparser
import logging
import random
import time


class PassengerExplore(ExploreFight):
    """
    探索打手脚本
    """

    def __init__(self, hwnd=0):
        # 初始化
        ExploreFight.__init__(self, 'Passenger: ', hwnd)

        # 读取配置文件
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        self.gouliang1 = conf.getboolean('explore', 'driver_passenger_1')
        self.gouliang2 = conf.getboolean('explore', 'driver_passenger_2')
        self.gouliang3 = conf.getboolean('explore', 'driver_passenger_3')



    def start(self):
        """
        开始执行
        """
        mood1 = ut.Mood(1)
        # 进入脚本循环
        while self.run:
            logging.info(self.name + "正在检测当前场景")

            self.check_quit_game()

            # 开始检测当前战斗情况
            is_start, is_team, is_tansuo, is_juexing, is_yaoqing = self.check_now_scene()
            print('passenger', is_start, is_team, is_juexing, is_yaoqing)

            if is_tansuo:
                self.unlock_team()

            if is_juexing:
                # 等待接受邀请
                if not self.yys.wait_game_img('img/JIE-SHOU.png', 100, False):
                    continue

                # 接受邀請
                self.click_until('接受探索邀请', 'img/JIE-SHOU.png', *TansuoPos.jie_shou_btn, 0.4, False)

            if not is_start and not is_team and is_tansuo:
                # 检查boss
                if self.yys.find_game_img('img/BOSS.png'):
                    return

                loc = self.yys.find_game_img('img/TAN-JIANG-LI.png')
                if loc:
                    # 检查奖励
                    self.receive_reward()
                else:
                    if self.yys.find_img('img/FIGHT.png'):
                        # 队伍解散 退出副本
                        self.quit_tansuo()

                # 退出本次循环
                continue

            if is_start:
                print('passenger 正在战斗')
                self.wait_game_end()

def main():
    # hwnd = win32gui.FindWindow(0, u'阴阳师-网易游戏')
    yys = PassengerExplore()
    yys.start()


if __name__ == '__main__':
    main()
