import os

import cv2
import numpy as np

from explore.explore_fight import ExploreFight
import tools.utilities as ut
from tools.game_pos import CommonPos, TansuoPos

import configparser
import logging
import random
import time
from gameLib.find_moster import FindMoster


class DriverExplore(ExploreFight):

    def __init__(self, hwnd=0):
        # 初始化
        ExploreFight.__init__(self, 'Driver: ', hwnd)

        self.find_moser = FindMoster()

        self.isDriver = True
        self.exp_templates = [
            'img/EXP.png',
            'img/EXP2.png',
            'img/EXP-XP.png',
        ]
        self.fuben_max_width = 2300
        self.now_fuben_width = 0

        self.gouliang1 = False
        self.gouliang2 = False
        self.gouliang3 = False

    def start(self):
        """
        开始战斗
        :return:
        """
        while self.run:
            logging.info(self.name + "正在检测当前场景")
            # 开始检测当前战斗情况
            is_start, is_team, is_tansuo, is_juexing, is_yaoqing = self.check_now_scene()

            if not is_start and not is_team and not is_tansuo and not is_juexing and not is_yaoqing:
                self.log.writeinfo("等待进入场景")
                continue

            if is_juexing and is_yaoqing:
                continue

            if is_juexing and not is_yaoqing:
                self.log.writeinfo('开始检测场景')
                # 检测场景
                self.yys.wait_game_img('img/JI-XU.png')

                self.click_until('继续邀请队友', 'img/JI-XU.png',
                                 *TansuoPos.jixu_btn,  0.7, False)
                continue


            self.log.writeinfo(self.name + ' 进入探索页面')

            # 开始查找经验怪
            self.find_exp_moster1()

    def fight_monster(self, pos1, pos2):
        """
        挑战怪物
        :return:
        """
        # 要挑战位置
        pos_start = (pos1[0] - 100, pos1[1] - 50)
        pos_end = (pos2[0] + 100, pos2[1] + 200)
        img_src = self.yys.window_part_shot(pos_start, pos_end)
        cv2.imwrite('Temp/' + str(time.time()) + '.png', img_src)
        # print("要挑战怪物图")
        # cv2.imshow("image", img_src)
        # cv2.waitKey(0)
        templates = [
            'img/FIGHT.png'
        ]
        res = self.yys.find_img_from_src(img_src, *templates)
        if not res:
            time.sleep(1)
            return False
        pos1 = (res[0] + pos_start[0], res[1] + pos_start[1])
        pos2 = (pos1[0] + 15, pos1[1] + 10)
        self.click_until('挑战怪物', 'img/ZHUN-BEI.png', pos1, pos2, 0.8, True)

        self.wait_game_end()

        return True

    def find_exp_moster1(self):
        """
        查找经验怪物进行挑战
        """
        pos1 = (2, 120)
        pos2 = (1127, 600)

        # 战斗次数
        fight_num = 0
        self.log.writeinfo(self.name + '正在寻找怪物')
        times = 0
        while self.run and not self.fuben_is_end() and times <= 4:
            moster = []
            # 获取屏幕截图
            self.log.writeinfo(self.name + ' 获取屏幕截图')
            times += 1
            img_src = self.yys.window_part_shot(pos1, pos2)

            # 查找怪物
            guai = []
            img_template = cv2.imread('img/FIGHT.png')
            res = cv2.matchTemplate(img_src, img_template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8

            h, w = img_template.shape[:2]

            loc = np.where(res >= threshold)  # 匹配程度大于%80的坐标y,x
            n, ex, ey = 1, 0, 0
            for pt in zip(*loc[::-1]):  # *号表示可选参数
                # 去掉相邻的点
                x, y = pt[0] + int(w / 2) + pos1[0], pt[1] + int(h / 2) + pos1[1]
                if (x - ex) + (y - ey) < 15:
                    continue
                ex, ey = x, y
                guai.append([x, y])
            #     right_bottom = (pt[0] + w, pt[1] + h)
            #     cv2.rectangle(img_src, pt, right_bottom, (0, 0, 255), 2)
            # cv2.imshow("image", img_src)
            # cv2.waitKey(0)

            # 没有怪物，拖动场景
            if times >= 4:
                times = 0
                self.log.writeinfo("拖动场景")
                self.next_scene()
                continue

            # 查找怪物是否是经验怪
            for item in guai:
                x0 = item[0] - 80
                y0 = item[1] - 220
                x1 = item[0] + 80
                y1 = item[1] + 300
                if y0 <= 0:
                    y0 = 0
                if y1 >= 340:
                    y1 = 340
                if x0 <= 0:
                    x0 = 0
                if item[1] < 340:
                    y1 = 570
                new_img = img_src[y0:y1, x0:x1]

                # 区域查找 是否有经验图片
                exp_pos = []
                for template in self.exp_templates:
                    img_template = cv2.imread(template)
                    res = cv2.matchTemplate(new_img, img_template, cv2.TM_CCOEFF_NORMED)
                    threshold = 0.68
                    h, w = img_template.shape[:2]
                    loc = np.where(res >= threshold)  # 匹配程度大于%80的坐标y,x
                    n, ex, ey = 1, 0, 0
                    for pt in zip(*loc[::-1]):  # *号表示可选参数
                        # 去掉相邻的点
                        x, y = pt[0] + int(w / 2) + pos1[0], pt[1] + int(h / 2) + pos1[1]
                        if (x - ex) + (y - ey) < 15:
                            continue
                        ex, ey = x, y
                        exp_pos.append([x, y])
                        right_bottom = (pt[0] + w, pt[1] + h)
                        cv2.rectangle(new_img, pt, right_bottom, (0, 0, 255), 2)
                    cv2.imshow("image", new_img)
                    cv2.waitKey(0)
                print(exp_pos, item, y0)
                for pos in exp_pos:
                    new_posy = y0 + pos[1]
                    if new_posy > item[1] and new_posy - 90 > item[1]:
                        fight_num += 1
                        self.fight_monster(item, (item[0] + 30, item[1] + 20))
                break

        # 没有找到怪物 但是有经验怪 挑战BOSS
        is_fight_boss = False
        bossLoc = self.yys.find_game_img('img/BOSS.png')
        if bossLoc:
            is_fight_boss = True
            self.fight_monster(bossLoc, (bossLoc[0] + 50, bossLoc[1] + 40), True)

        if fight_num <= 0:
            # 随机选择一个怪物进行挑战
            maxVal, maxLoc = self.yys.find_game_img('img/FIGHT.png')
            if maxVal> 0.9:
                self.fight_monster(maxLoc, (maxLoc[0] + 15, maxLoc[1] + 10))

        self.log.writeinfo('战斗结束 检测当前场景')
        # 开始检测当前战斗情况
        is_start, is_team, is_tansuo, is_juexing, is_yaoqing = self.check_now_scene()

        self.now_fuben_width = 0
        if is_tansuo and is_fight_boss:
            # 领取奖励
            self.receive_reward()

        if is_tansuo and not is_fight_boss:
            self.log.writeinfo('探索中 退出探索进行下一轮')
            self.quit_tansuo()

    def find_exp_moster(self):
        """
        寻找经验怪物
        :return:
        """
        pos1 = (2, 205)
        pos2 = (1127, 545)
        isSeach = True
        scene_num = 0
        fails = []
        # 战斗次数
        fight_num = 0
        self.log.writeinfo(self.name + '正在寻找怪物')

        while isSeach and not self.fuben_is_end() and self.run:
            moster = self.search_pos_exp_moster(pos1, pos2)

            # 寻找怪物
            find_pos = self.yys.find_many_game_img(
                'img/FIGHT.png',
            )
            # 对比怪物位置，跟经验怪位置
            print('找到经验怪位置', moster)
            print('找到怪物位置', find_pos)
            if len(moster) > 0:
                mos_fails = []
                for mos in find_pos:
                    new_pos1 = (mos[0] - 100, mos[1] - 30)
                    new_pos2 = (mos[0] + 100, mos[1] + 200)
                    # 区域内经验怪数量
                    exp_pos = []
                    for exp in moster:
                        if new_pos1[0] < exp[0] < new_pos2[0] and new_pos1[1] < exp[1] < new_pos2[1] and mos[1] + 90 < \
                                exp[1]:
                            # 当前经验怪在区域内
                            exp_pos.append(exp)
                    if len(exp_pos) == 1:

                        print("怪物位置", exp_pos)
                        if self.fight_monster(mos, (mos[0] + 10, mos[1] + 10)):
                            fight_num += 1
                            # 去掉已经挑战的经验怪
                            moster.remove(exp)

                    if len(exp_pos) <= 0:
                        # 没找到就进行跳过
                        continue

                    if len(exp_pos) > 1:
                        # moster1 = self.search_pos_exp_moster(new_pos1, new_pos2)
                        # if len(moster1) > 2:
                        #     # 如果还是大于两个，就跳过
                        #     continue
                        # 两个以上经验怪根据位置移动
                        mos_fails.append(exp_pos)

                    #
                    # # 挑战结束后，如果还有经验怪
                    # if len(exp_pos) > 0:
                    #     fails = fails + exp_pos
                print("当前模糊坐标", mos_fails)

                if len(mos_fails) > 0:
                    next = False
                    width = 0
                    for item in mos_fails:
                        if len(item) > 1:
                            middle = 530
                            for pos_item in item:
                                if pos_item[0] > middle:
                                    next = True
                                    width = 180
                                    break
                                elif pos_item[0] < middle:
                                    next = True
                                    width = -180
                                    break
                    if next:
                        self.next_scene(width)

            # 当前场景有移动怪物，进行挑战
            if len(fails) > 0:
                for fail in fails:
                    start_1 = time.time()
                    while time.time() - start_1 < 2 and self.run:
                        pos_fail1 = (fail[0] - 300, fail[1] - 150)
                        pos_fail2 = (fail[0] + 400, fail[1] + 100)
                        if pos_fail2[1] > 620:
                            pos_fail2[2] = 620

                        # 检查当前创建图片
                        img_src = self.yys.window_part_shot(pos_fail1, pos_fail2)
                        # TODO 保存现场
                        cv2.imwrite('temp/失败经验位置' + str(time.time()) + '.png', img_src)
                        # 识别经验位置
                        exp = self.yys.find_img_from_src(img_src, *self.exp_templates)
                        fight = self.yys.find_img_from_src(img_src, 'img/FIGHT.png')

                        if exp and fight:
                            # 是经验怪
                            result_1 = self.fight_monster(mos, (mos[0] + 10, mos[1] + 10))
                            if not result_1:
                                logging.warning('怪物移动速度太快，跳过')
                            else:
                                fight_num += 1
                                fails.remove(fail)

            # 移动场景
            self.next_scene()


        print("挑战失败的怪物物", fails)
        # 没有找到怪物 但是有经验怪 挑战BOSS
        is_fight_boss = False
        bossLoc = self.yys.find_game_img('img/BOSS.png')
        if bossLoc:
            is_fight_boss = True
            self.fight_monster(bossLoc, (bossLoc[0] + 50, bossLoc[1] + 40), True)

        if fight_num <= 0:
            # 随机选择一个怪物进行挑战
            maxVal, maxLoc = self.yys.find_game_img('img/FIGHT.png')
            if maxVal> 0.9:
                self.fight_monster(maxLoc)

        self.log.writeinfo('战斗结束 检测当前场景')
        # 开始检测当前战斗情况
        is_start, is_team, is_tansuo, is_juexing, is_yaoqing = self.check_now_scene()

        self.now_fuben_width = 0
        if is_tansuo and is_fight_boss:
            # 领取奖励
            self.receive_reward()

        if is_tansuo and not is_fight_boss:
            self.log.writeinfo('探索中 退出探索进行下一轮')
            self.quit_tansuo()

        time.sleep(1)

    def search_pos_exp_moster(self, pos1, pos2, sleep=3.5):
        """
        查找制定位置的经验怪
        :param pos1:
        :param pos2:
        :param sleep:
        :return: 经验怪位置
        """
        start = time.time()
        # 怪物坐标
        moster = []
        # 循环截图分析
        times = 0
        while self.run and time.time() - start <= sleep:
            img_src = self.yys.window_part_shot(pos1, pos2)
            times += 1
            for item in self.exp_templates:
                img_template = cv2.imread(item)

                res = cv2.matchTemplate(img_src, img_template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.65

                h, w = img_template.shape[:2]

                loc = np.where(res >= threshold)  # 匹配程度大于%80的坐标y,x
                n, ex, ey = 1, 0, 0
                for pt in zip(*loc[::-1]):  # *号表示可选参数
                    # 去掉相邻的点
                    x, y = pt[0] + int(w / 2) + pos1[0], pt[1] + int(h / 2) + pos1[1]
                    if (x - ex) + (y - ey) < 15:
                        continue
                    ex, ey = x, y
                    moster.append([x, y])
                #     right_bottom = (pt[0] + w, pt[1] + h)
                #     cv2.rectangle(img_src, pt, right_bottom, (0, 0, 255), 2)
                # cv2.imshow("image", img_src)
                # cv2.waitKey(0)

            time.sleep(0.4)

        print("识别次数", times)
        # 识别完毕，开始整理boss 位置
        new_pos = []
        n, ex, ey = 1, 0, 0
        for pos in moster:
            x, y = pos[0] + 6, pos[1] + 6
            # 高度相差10的忽略
            if (y - ey) < 10 and (x - ex) < 85:
                continue

            ex, ey = x, y
            new_pos.append([x, y])
        return new_pos

    def next_scene(self, width=400):
        '''
        移动至下一个场景，每次移动400像素
        '''
        print("移动场景", width)
        if width > 0:
            x0 = random.randint(width + 10, 1126)
            x1 = x0 - width
        else:
            x0 = random.randint(10, abs(width) - 10)
            x1 = x0 + abs(width)

        y0 = random.randint(110, 210)
        y1 = random.randint(110, 210)
        self.now_fuben_width += width
        self.yys.mouse_drag_bg((x0, y0), (x1, y1))

    def fuben_is_end(self):
        return self.now_fuben_width >= self.fuben_max_width
