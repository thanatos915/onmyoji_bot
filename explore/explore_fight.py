import os
import time

import cv2

import tools.utilities as ut
from tools.game_pos import CommonPos, TansuoPos

from gameLib.fighter import Fighter


class ExploreFight(Fighter):

    def __init__(self, name, hwnd=0):
        # 初始化
        Fighter.__init__(self, name, 0, hwnd)

        # 读取配置文件
        # conf = configparser.ConfigParser()
        # conf.read('conf.ini')
        # self.fight_boss_enable = conf.getboolean('explore', 'fight_boss_enable')
        # self.slide_shikigami = conf.getboolean('explore', 'slide_shikigami')
        # self.slide_shikigami_progress = conf.getint('explore', 'slide_shikigami_progress')
        # self.zhunbei_delay = conf.getfloat('explore', 'zhunbei_delay')
        self.isDriver = False

        self.gouliang1 = True
        self.gouliang2 = True
        self.gouliang3 = True
        # 式神种类 1:素材 2: N卡 3: R卡
        self.level = 2

    def check_exp_full(self):
        """
        检查狗粮经验
        """
        self.log.writeinfo(self.name + '开始检测狗粮经验状态')
        maxVal, maxLoc = self.yys.find_multi_img('img/MAN3.png', 'img/MAN1.png', 'img/MAN2.png', part=1,
                                                 pos1=TansuoPos.gouliang_exp_passenger[0],
                                                 pos2=TansuoPos.gouliang_exp_passenger[1], gray=1)
        posV1, posV2, posV3 = maxVal
        gouliang1 = posV1 > 0.97 and self.gouliang1
        gouliang2 = posV2 > 0.97 and self.gouliang2
        gouliang3 = posV3 > 0.97 and self.gouliang3

        if self.isDriver:
            # 司机
            shishen_1 = (0, 220), (330, 380)
            shishen_2 = (380, 420), (610, 575)
            shishen_3 = (163, 351), (303, 511)
        else:
            # 打手
            shishen_1 = (170, 180), (330, 380)
            shishen_2 = (330, 230), (540, 430)
            shishen_3 = (590, 270), (810, 490)

        # 获取当前屏幕截图
        img_src = self.yys.window_full_shot()

        man = [
            'img/MAN1.png',
            'img/MAN2.png',
            'img/MAN3.png',
        ]

        # 式神1
        new_img = img_src[shishen_1[0][1]: shishen_1[1][1], shishen_1[0][0]: shishen_1[1][0]]
        posLoc1 = self.yys.find_img_from_src(new_img, *man)
        new_img = img_src[shishen_2[0][1]: shishen_2[1][1], shishen_2[0][0]: shishen_2[1][0]]
        posLoc2 = self.yys.find_img_from_src(new_img, *man)
        new_img = img_src[shishen_3[0][1]: shishen_3[1][1], shishen_3[0][0]: shishen_3[1][0]]
        posLoc3 = self.yys.find_img_from_src(new_img, *man)

        print('式神经验检查', posLoc1, posLoc2, posLoc3)
        gouliang1 = posLoc1 and self.gouliang1
        gouliang2 = posLoc2 and self.gouliang2
        gouliang3 = posLoc3 and self.gouliang3

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
                print('滚动条', (x1, y1), (x2, y1))
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
            if maxVal > 0.9:
                print("式神{0}: 已出战".format(number))
                number += 1
                continue
            # 检查是否观战
            tml_img = cv2.imread('img/EYES.png')
            res = cv2.matchTemplate(new_img, tml_img, cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
            if maxVal > 0.9:
                print("式神{0}：已观战".format(number))
                number += 1
                continue

            # 检查是否满级
            tml_img = cv2.imread('img/SHI-SHEN-MAN.png')
            res = cv2.matchTemplate(new_img, tml_img, cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
            print('满级测试', maxVal)
            if maxVal > 0.9:
                print("式神{0}：已满级".format(number))
                number += 1
                continue
            if self.level == 1:
                # 检查是不是白蛋 (素材只有白蛋才当狗粮)
                tml_img = cv2.imread('img/BAI-DAN.png')
                res = cv2.matchTemplate(new_img, tml_img, cv2.TM_CCOEFF_NORMED)
                minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
                if maxVal < 0.9:
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
                if maxVal > 0.9:
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

    def check_now_scene(self):
        """
        检测当前副本场景
        :return:
        """
        start = time.time()
        # 是否开始战斗
        is_start = False
        # 是否正在组队
        is_team = False
        # 是否再探索页面中
        is_tansuo = False
        # 是否在探索中
        is_juexing = False
        while time.time() - start <= 2.5 and not is_start and not is_juexing and self.run:
            maxVal, maxLoc = self.yys.find_multi_img('img/ZHUN-BEI.png', 'img/DUI.png', 'img/YING-BING.png',
                                                 'img/TIAO-ZHAN.png', 'img/YAO-QING.png')
            startVal, teamVal, tanVal, tuVal, yaoqingVal = maxVal
            # print(maxVal)
            # print(maxVal)
            # print(maxVal)
            # 是否在队伍中
            is_team = teamVal > 0.9
            # 是否在副本中
            is_tansuo = tanVal > 0.9
            # 是否回到章节页面
            is_juexing = tuVal > 0.9
            # 战斗是否开始
            is_start = startVal > 0.9
            is_yaoqing = yaoqingVal > 0.9

        return is_start, is_team, is_tansuo, is_juexing, is_yaoqing

    def receive_reward(self):
        """
        领取奖励
        :return:
        """
        while self.run:
            self.log.writeinfo('开始领取奖励')
            time.sleep(0.8)
            loc = self.yys.find_game_img('img/TAN-JIANG-LI.png')
            if loc:
                time.sleep(0.5)
                self.click_until('领取奖励', 'img/HUO-DE-JIANG-LI.png', loc, (loc[0] + 30, loc[1] + 30))
                self.yys.mouse_click_bg(ut.firstposition())
            else:
                return

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


    def wait_game_end(self):

        # 游戏已开始
        time.sleep(1)

        # 检查狗粮
        self.check_exp_full()

        # 点击准备，直到进入战斗
        self.click_until_multi('准备按钮', 'img/YI-ZHUN-BEI.png', 'img/ZI-DONG.png',
                               pos=TansuoPos.ready_btn[0], pos_end=TansuoPos.ready_btn[1], sleep_time=0.3)

        # 检查战斗是否结束
        self.check_end()

        time.sleep(2.5)
        self.yys.mouse_click_bg(ut.firstposition())

        # 二次结算
        self.yys.mouse_click_bg(ut.firstposition())
        self.click_until('第一次结算', 'img/JIN-BI.png',
                         *CommonPos.second_position, 0.3)
        self.click_until('第二次结算', 'img/JIN-BI.png',
                         *CommonPos.second_position, 0.2, False)

        #保证游戏结束
        self.yys.mouse_click_bg(ut.firstposition())

