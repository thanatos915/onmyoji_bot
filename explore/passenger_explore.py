import os

import cv2

from gameLib.fighter import Fighter
import tools.utilities as ut
from tools.game_pos import CommonPos, TansuoPos

import configparser
import logging
import random
import time


class PassengerExplore(Fighter):
    """
    探索打手脚本
    """

    def __init__(self, hwnd=0):
        # 初始化
        Fighter.__init__(self, 'Passenger: ', 0, hwnd)

        # 读取配置文件
        # conf = configparser.ConfigParser()
        # conf.read('conf.ini')
        # self.fight_boss_enable = conf.getboolean('explore', 'fight_boss_enable')
        # self.slide_shikigami = conf.getboolean('explore', 'slide_shikigami')
        # self.slide_shikigami_progress = conf.getint('explore', 'slide_shikigami_progress')
        # self.zhunbei_delay = conf.getfloat('explore', 'zhunbei_delay')
        self.gouliang1 = True
        self.gouliang2 = True
        self.gouliang3 = True
        # 式神种类 1:素材 2: N卡 3: R卡
        self.level = 2

    def quit_tansuo(self):
        """
        退出探索页
        """
        # 点击退出探索
        self.click_until('退出按钮', 'img\\QUE-REN.png',
                         *TansuoPos.quit_btn, 0.5)

        # 点击确认
        self.click_until('确认按钮', 'img\\QUE-REN.png',
                         *TansuoPos.confirm_btn, 0.6, False)

        return self.yys.wait_game_img('img/TIAO-ZHAN.png')

    def check_exp_full(self):
        """
        检查狗粮经验
        """
        self.log.writeinfo(self.name + '开始检测狗粮经验状态')
        maxVal, maxLoc = self.yys.find_multi_img('img/MAN3.png', 'img/MAN1.png', 'img/MAN2.png', part=1,
                                                 pos1=TansuoPos.gouliang_exp_passenger[0], pos2=TansuoPos.gouliang_exp_passenger[1], gray=1)
        posV1, posV2, posV3 = maxVal
        gouliang1 = posV1 > 0.97 and self.gouliang1
        gouliang2 = posV2 > 0.97 and self.gouliang2
        gouliang3 = posV3 > 0.97 and self.gouliang3

        if not gouliang1 and not gouliang3 and not gouliang2:
            return

        # 开始换狗粮
        while self.run:
            # 点击狗粮位置
            self.yys.mouse_click_bg(*TansuoPos.change_monster)
            if self.yys.wait_game_img('img/QUAN-BU.png', 3, False):
                break

        time.sleep(1)
        pos = []
        if gouliang1:
            pos.append((953, 315))

        if gouliang2:
            pos.append((554, 315))

        if gouliang3:
            pos.append((187, 315))

        print('需要更换式神', pos)
        down = False
        while not down:
            res = self.check_gouliang_level(pos)
            print(res)
            if res == 2:
                down = True
            elif res == -1:
                # 当前所有式神满街更换等级式神
                self.level += 1
                if self.level >= 4:
                    self.log.writewarning('暂无式神进行更换')
                    self.yys.quit_game()

        return True

    def check_gouliang_level(self, replace_pos):
        """
        更换指定等级的式神当狗粮
            :param replace_pos 替换的位置的素组
        """

        # 点击“全部”选项
        self.yys.mouse_click_bg(*TansuoPos.quanbu_btn)
        time.sleep(1)

        pos = {
            1: TansuoPos.s_tab_btn,
            2: TansuoPos.n_tab_btn,
            3: TansuoPos.r_tab_btn,
        }.get(self.level, TansuoPos.n_tab_btn)

        # 点击式神种类卡
        self.yys.mouse_click_bg(*pos)
        time.sleep(1)

        # 获取式神截图 进行对比
        part_pos_start = (135, 423)
        part_pos_end = (935, 640)
        img_src = self.yys.window_part_shot(part_pos_start, part_pos_end)
        # 当前式神序号
        number = 1
        down = False
        # 当前需要替换式神位置
        shi_shen_pos = 0
        while not down and shi_shen_pos >= 0:
            if number >= 8:
                # 检查当前进度条是否到顶
                maxVal, maxLoc = self.yys.find_img('img/PROGESS.png')
                # print("滚动条位置", maxVal)
                if maxVal > 0.97 and maxLoc[0] >= 744:
                    # 当前进度条已经到顶更换等级再来
                    return -1
                # 调整进度条重新获取截取
                # 拖动的位置
                x1 = (96 + 15) * (number - 2) + 50 + part_pos_start[0]
                y1 = 520
                # 拖动到的位置
                x2 = x1 - (96 * (number - 2) + 15 * number + 31)
                print('滚动条',(x1, y1), (x2, y1))
                self.yys.mouse_drag_bg((x1, y1), (x2, y1))
                time.sleep(0.5)
                img_src = self.yys.window_part_shot(part_pos_start, part_pos_end)

                # new_img = img_src[0:208, 333:456]
                # # 检查是否满级
                # tml_img = cv2.imread('img/SHI-SHEN-MAN.png')
                # res = cv2.matchTemplate(new_img, tml_img, cv2.TM_CCOEFF_NORMED)
                # minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
                # print('满级测试', maxVal)
                # cv2.imshow("image", new_img)
                # cv2.waitKey(0)
                number = 1

            # 计算当前截图位置
            x1 = (96 + 15) * (number - 1)
            x2 = (96 + 15) * number + 12
            new_img = img_src[0:208, x1:x2]

            # 检查是否出战
            tml_img = cv2.imread('img/ZHAN-DOU.png')
            res = cv2.matchTemplate(new_img, tml_img, cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
            if maxVal > 0.97:
                print("式神{0}: 已出战".format(number))
                number += 1
                continue
            # 检查是否观战
            tml_img = cv2.imread('img/EYES.png')
            res = cv2.matchTemplate(new_img, tml_img, cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
            if maxVal > 0.97:
                print("式神{0}：已观战".format(number))
                number += 1
                continue

            # 检查是否满级
            tml_img = cv2.imread('img/SHI-SHEN-MAN.png')
            res = cv2.matchTemplate(new_img, tml_img, cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
            print('满级测试', maxVal)
            if maxVal > 0.93:
                print("式神{0}：已满级".format(number))
                number += 1
                continue
            if self.level == 1:
                # 检查是不是白蛋 (素材只有白蛋才当狗粮)
                tml_img = cv2.imread('img/BAI-DAN.png')
                res = cv2.matchTemplate(new_img, tml_img, cv2.TM_CCOEFF_NORMED)
                minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
                if maxVal < 0.97:
                    print('式神{0}：不是白蛋'.format(number))
                    number += 1
                    continue

            # 排除式神星级
            xing = ['img/XING-5-1.png', 'img/XING-5-2.png', 'img/XING-5-3.png']
            is_set = False
            for item in xing:
                tml_img = cv2.imread(item)
                res = cv2.matchTemplate(new_img, tml_img, cv2.TM_CCOEFF_NORMED)
                minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
                print("{0} {1}".format(item, maxVal))
                if maxVal > 0.97:
                    is_set = True
                    break

            if is_set:
                print('式神{0}：大于五星'.format(number))
                number += 1
                continue

            # 当前式神可出战
            replace_x1 = int(part_pos_start[0] + x2 - 55)
            print('式神位置', (replace_x1, 520), replace_pos[shi_shen_pos])
            self.yys.mouse_drag_shishen_bg((replace_x1, 520), replace_pos[shi_shen_pos])
            number += 1

            time.sleep(1)
            # 更新下一个需要替换的式神
            next_index = -1
            for item in replace_pos:
                if replace_pos[shi_shen_pos] == item:
                    next_index = shi_shen_pos + 1

            if next_index < len(replace_pos):
                shi_shen_pos = next_index
            else:
                shi_shen_pos = -1

        return 2


    def start(self):
        """
        开始执行
        """
        mood1 = ut.Mood(1)
        # 进入脚本循环
        while self.run:
            # 等待接受邀请
            if not self.yys.wait_game_img('img/FU-BEN-28.png', 100, False):
                continue

            # 接受邀請
            self.click_until('接受探索邀请', 'img/FU-BEN-28.png', *TansuoPos.jie_shou_btn, 0.4, False)

            # 等待开始战斗
            isRun = True
            while isRun:
                # 开始检测当前战斗情况
                # 是否开始战斗
                is_start = False
                # 是否正在组队
                is_team = False
                # 是否再探索页面中
                is_tansuo = False
                # 是否在探索中
                is_juexing = False
                start = time.time()
                self.log.writeinfo(self.name + '正在检测当前场景')
                while time.time() - start <= 2.5 and not is_start and self.run:
                    maxVal, maxLoc = self.yys.find_multi_img('img/ZHUN-BEI.png', 'img/DUI.png', 'img/YING-BING.png', 'img/JUE-XING.png')
                    startVal, teamVal, tanVal, tuVal = maxVal
                    # print(maxVal)
                    if startVal > 0.97:
                        # 当前正在战斗中
                        is_start = True
                    # 是否在队伍中
                    is_team = teamVal > 0.97
                    # 是否在副本中
                    is_tansuo = tanVal > 0.97


                if tuVal > 0.97:
                    isRun = False
                    break

                if not is_start and not is_team and is_tansuo:
                    # 队伍解散 退出副本
                    self.quit_tansuo()
                    isRun = False
                    # 退出本次循环
                    break

                if is_start:
                    # 检查狗粮
                    self.check_exp_full()

                    # 点击准备，直到进入战斗
                    self.click_until_multi('准备按钮', 'img/YI-ZHUN-BEI.png', 'img/ZI-DONG.png',
                                           pos=TansuoPos.ready_btn[0], pos_end=TansuoPos.ready_btn[1], sleep_time=mood1.get1mood() / 1000)

                    # 检查战斗是否结束
                    self.check_end()

                    # 二次结算
                    self.yys.mouse_click_bg(ut.firstposition())
                    self.click_until('结算', 'img/JIN-BI.png',
                                     *CommonPos.second_position, 0.3)
                    self.click_until('结算', 'img/JIN-BI.png',
                                     *CommonPos.second_position, 0.2, False)
                    # 保证游戏结束
                    self.yys.mouse_click_bg(ut.firstposition())


def main():
    # hwnd = win32gui.FindWindow(0, u'阴阳师-网易游戏')
    yys = PassengerExplore()
    yys.start()


if __name__ == '__main__':
    main()
