import ctypes
import os
import sys
import time
import tools.utilities as ut
from tools.game_pos import CommonPos, YuhunPos, TuPoPos

from PIL import Image

from gameLib.game_ctl import GameControl

import cv2
import numpy
import win32con
import win32gui
import win32ui
import numpy as np
from gameLib.fighter import Fighter


class Boundary(Fighter):

    def __init__(self, hwnd=0):
        # 初始化
        Fighter.__init__(self, 'Boundary: ', 0, hwnd)

    def start_fight(self, pos):
        """
        进攻结界
            :return pos 挑战失败的位置
        """
        mood2 = ut.Mood()
        # 挑战失败的结界
        fail_pos = []
        # 挑战成功的个数
        success_num = 9 - len(pos)

        is_tiaozhan = True
        # 开始循环点击
        for item in pos:
            # 开始挑战
            pos = item[0]
            pos_end = item[1]
            start_time = time.time()

            # 点击

            is_end = False
            while time.time() - start_time <= 20 and self.run and not is_end:
                result = self.yys.find_game_img('img/JIN-GONG.png', 0, None, None, 0, 0.94)
                if result:
                    self.log.writeinfo(self.name + '选择突破对象成功')
                    # 开始进攻
                    jin_gong_pos = (result[0] + 10, result[1] + 10), (result[0] + 110, result[1] + 50)
                    jin_gong = self.click_until('开始进攻', 'img/ZHUN-BEI.png', *jin_gong_pos, 0.7)
                    if not jin_gong:
                        # 进攻失败，结界突破券不足
                        self.log.writeinfo(self.name + '结界突破券不足')
                        os.system('pause')
                        return fail_pos
                    # 准备
                    self.click_until('准备', 'img\\ZI-DONG.png', *CommonPos.zhunbei_btn, mood2.get1mood() / 1000)

                    time.sleep(0.8)

                    # 标记式神
                    self.click_team(2)

                    time.sleep(5)

                    # 检测游戏结果
                    res = self.check_result()
                    print(res)
                    if res == -1:
                        # 超时退出游戏
                        self.yys.quit_game()

                    if res == 1:
                        # 战斗失败
                        fail_pos.append((pos, pos_end))

                    if res == 2:
                        success_num += 1

                    # 对比奖励个数，是否进行继续挑战
                    max_jingong = 9
                    fail_num = len(fail_pos)
                    if fail_num > 0 and fail_num <= 3:
                        max_jingong = 6
                    elif fail_num > 3 and fail_num <= 6:
                        max_jingong = 3
                    elif fail_num <= 0:
                        max_jingong = 9
                    else:
                        max_jingong = 0

                    if success_num >= max_jingong:
                        is_tiaozhan = False

                    print("计算次数", max_jingong, is_tiaozhan)

                    # 手动结算
                    self.yys.mouse_click_bg(ut.threeposition())
                    time.sleep(0.5)
                    print("点击过了")
                    # 等待下一轮
                    self.yys.wait_game_img('img/JIE-JIE-TU-PO.png', 10)
                    self.log.writeinfo(self.name + '回到结界突破页面')

                    is_end = True

                else:
                    # 点击指定位置并等待下一轮
                    self.yys.mouse_click_bg(pos, pos_end)
                    self.log.writeinfo(self.name + '点击 选择突破对象')
                    time.sleep(0.6)

        return fail_pos

    def check_result(self):
        """
        检测游戏结果
            : return 1 战斗失败 2 战斗胜利 -1 超时
        """
        # 检测是否打完
        self.log.writeinfo(self.name + '检测是战斗是否结束')
        start_time = time.time()
        while time.time() - start_time <= 500 and self.run:
            maxVal, maxLoc = self.yys.find_multi_img('img/YIN-BI.png', 'img/SHI-BAI.png', 'img/SHENG-LI.png')
            yingVal, shibaiVal, shengliVal = maxVal
            # print(maxVal)
            if shibaiVal > 0.97:
                self.log.writeinfo(self.name + "战斗结束: 失败")
                return 1

            if yingVal > 0.97:
                self.log.writeinfo(self.name + "战斗结束: 胜利")
                return 2

            if shengliVal > 0.97:
                self.click_until('第一次结算', 'img/YIN-BI.png', ut.threeposition(), None, 0.2)

            time.sleep(0.2)

        return -1


    def start(self):
        # self.yys.takescreenshot()
        # os.system('pause')
        number = 0
        while self.run:
            po_start_x1 = 110
            po_start_y1 = 80
            po_start_x2 = 1030
            po_start_y2 = 440
            # new_img = img_src[po_start_y1:po_start_y2, po_start_x1:po_start_y2]
            img_src = self.yys.window_part_shot((po_start_x1, po_start_y1), (po_start_x2, po_start_y2))
            th, tw = img_src.shape[:2]
            # 计算坐标
            h = int(th / 3)
            w = int(tw / 3)
            # 当前突破数量
            po_num = 0
            # 需要突破位置列表
            po_pos = []
            # 是否突破图片
            img_template_po = cv2.imread('img/PO.png')

            for width in range(3):
                for height in range(3):
                    x1 = w * width
                    y1 = h * height
                    x2 = x1 + w
                    y2 = y1 + h
                    split_img = img_src[y1:y2, x1:x2]
                    # 是否突破
                    res = cv2.matchTemplate(split_img, img_template_po, cv2.TM_CCOEFF_NORMED)
                    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
                    # cv2.imshow("image", split_img)
                    # cv2.waitKey(0)
                    # print("当前对比", maxVal)
                    # os.system('pause')
                    if maxVal < 0.9:
                        po_num += 1
                        po_pos.append(((x1 + po_start_x1 + 85, y1 + po_start_y1), (x2 + po_start_x1, y2 + po_start_y1)))

            if po_num > 0:
                print("需要进攻的结界",po_pos)
                # 开始挑战
                fail = self.start_fight(po_pos)

                number += po_num - len(fail)
                # 刷新结界

            self.yys.mouse_click_bg(*TuPoPos.refresh_btn)
            time.sleep(1)
            self.yys.mouse_click_bg(*TuPoPos.refresh_sure_btn)
