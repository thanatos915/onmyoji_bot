import time

import cv2

from gameLib.fighter import Fighter
from gameLib.shishen_action import ShishenAction
from tools.game_pos import CommonPos


class FightWay():

    def __init__(self, fighter: Fighter):
        self.fighter = fighter
        self.actions: list[ShishenAction] = []
        self.change_zi_dong = None

    def add_action(self, action: ShishenAction):
        """
        添加式神战斗方式
        """
        self.actions.append(action)
        return self


    def start(self):
        """
        开始手动战斗
        """
        if len(self.actions) < 6:
            self.fighter.log("自定义动作不满6个无法继续")
            return

        # 切换手动
        if self.fighter.yys.find_game_img('img/ZI-DONG.png'):
            self.fighter.click_until("切换成手动战斗", 'img/SHOU-DONG.png', *CommonPos.zi_dong_bth)

        is_end = False
        while self.fighter.run and not is_end:
            # 获取截图
            img_src = self.fighter.yys.window_full_shot()
            for action in self.actions:
                # 对比
                res = cv2.matchTemplate(img_src, action.get_avator_img(), cv2.TM_CCOEFF_NORMED)
                minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
                if maxVal > 0.9:
                    action.use_skill()

                # 检测是否要切换回自动
                if self.change_zi_dong(action):

                    self.fighter.click_until("切换成自动战斗", 'img/ZI-DONG.png', *CommonPos.zi_dong_bth)
                    # 标记式神
                    self.fighter.click_team(2)
                    return True

            # 检查是否结束
            if not self.fighter.yys.find_game_img('img/SHOU-DONG.png'):
                is_end = True