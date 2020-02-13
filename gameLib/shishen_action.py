import logging
import os
import time

import cv2

from gameLib.game_ctl import GameControl
from gameLib.fighter import Fighter
from tools.game_pos import CommonPos


class ShishenAction():
    """
    定义式神操作类
    """

    def __init__(self, fighter: Fighter, name, avator):
        self.fighter = fighter
        # 式神名字
        self.name = name
        self.avator = avator
        # 当前使用技能
        self.skill = 1
        # 技能使用方式 True 敌方 False 友方
        self.skill_way = True
        # 技能使用对象 0 全部 1-6式神
        self.skill_obj = 1
        # 鬼火数量
        self.fire_num = 0

        # 是否使用技能前切换节能
        self.skill_change = False

        self.skill_change_way = None

        # 对队友使用技能记录
        self.you_list = set()

        self.img_src = None


    def set_skill(self, skill, fire_num, skill_way, skill_obj=0):
        """
        设置式神使用技能方式
        """
        self.skill = skill

        self.fire_num = fire_num

        self.skill_way = skill_way

        if skill_obj < 0 or skill_obj > 6:
            logging.info("技能使用对象出错")

        self.skill_obj = skill_obj
        return self

    def change_skill(self):
        """
        使用节能前切换
        """
        if self.name == '茶几' and self.skill_change == False:
            self.fighter.log.writeinfo(self.name + "开始切换技能")

            self.fighter.click_until(self.name + '切换技能', 'img/CHA-JI-SKILL1.png', *CommonPos.shishen_skill_two, 0.8)

            self.fighter.click_until('', 'img/CHA-JI-BU-DONG.png', *CommonPos.cha_ji_change_skill_2, 0.8)

            self.fighter.click_until('', 'img/CHA-JI-BU-DONG.png', *CommonPos.cha_ji_change_skill_1, 1, False)

            self.skill_change = True

    def get_skill_obj(self):
        """
        检查使用技能
        """
        obj = 0
        if self.name == '大蛇':
            if obj in self.you_list:
                for item in [1, 2, 3, 4, 5]:
                    if not (item in self.you_list):
                        obj = item

                if obj == 0:
                    # 大蛇改使用1技能
                    self.use_1_skill()
                    return 0

        self.you_list.add(obj)
        return obj

    def use_skill(self):
        """
        式神行动
        """
        five_num = self.fighter.yys.get_five_num()
        self.fighter.log.writeinfo("当前鬼火数量: {0}".format(five_num))
        if self.fire_num <= five_num:
            # 使用技能
            pos = self.get_skill_pos(self.skill)
            if not self.skill_way:
                # 对友方使用技能
                if self.skill_obj > 0 and self.skill_obj <= 6:

                    obj = self.get_skill_obj()

                    if obj <= 0:
                        return

                    self.fighter.yys.mouse_click_bg(*pos)
                    time.sleep(0.4)

                    shishen = {
                        1: ((79, 385), (142, 418)),
                        2: ((315, 335), (360, 358)),
                        3: ((523, 270), (570, 325)),
                        4: ((715, 340), (750, 380)),
                        5: ((955, 400), (1055, 430)),
                    }

                    pos1 = shishen.get(obj)

                    self.fighter.click_until("{0}对己方{1}号式神使用{2}技能".format(self.name, obj, self.skill),
                                             self.get_avator_path(), pos1[0], pos1[1], 0.5, False)



                else:
                    self.use_1_skill()
            else:
                # 对敌方使用技能
                self.change_skill()

                self.fighter.click_until("{0}对敌方使用{1}技能".format(self.name, self.skill), self.get_avator_path(), pos[0], pos[1], 0.7,
                                         False)
                self.fighter.yys.mouse_click_bg(*pos)
                time.sleep(0.4)

        else:
            # 使用1一技能完善
            self.use_1_skill()

    def use_1_skill(self):
        pos = self.get_skill_pos(1)
        self.fighter.yys.mouse_click_bg(*pos)
        time.sleep(0.8)
        xuetiaoPos1 = CommonPos.enemy_region[0]
        xuetiaoPos2 = CommonPos.enemy_region[1]
        xuetiaoLoc = self.fighter.yys.find_game_img('img/XUE-TIAO.png', 1, xuetiaoPos1, xuetiaoPos2, 0, 0.7)
        if xuetiaoLoc:
            attack_po1 = (xuetiaoLoc[0] + 20 + xuetiaoPos1[0], xuetiaoLoc[1] + 20 + xuetiaoPos1[1])
            attack_pos2 = (attack_po1[0] + 80, attack_po1[1] + 100)

            self.fighter.yys.mouse_click_bg(attack_po1, attack_pos2)
            self.fighter.click_until("对敌方使用{0}技能".format(1), self.get_avator_path(), attack_po1, attack_pos2, 0.7,
                                     False)

    def get_skill_pos(self, skill):
        if skill == 3:
            return CommonPos.shishen_skill_three
        elif skill == 2:
            return CommonPos.shishen_skill_two
        else:
            return CommonPos.shishen_skill_one

    def get_avator_img(self):
        if self.img_src is None:
            self.img_src = cv2.imread('img/shishen/' + self.avator)
        return self.img_src

    def get_avator_path(self):
        return 'img/shishen/' + self.avator