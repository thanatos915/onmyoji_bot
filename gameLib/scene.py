import cv2


class Scene():

    def __init__(self):
        # 庭院
        self.isHome = False
        # 探索页
        self.isTansuo = False
        # 章节页
        self.isArt = False
        # 探索中
        self.isTanSuoIng = False
        # 组队探索中
        self.isTeamTansuoIng = False
        # 战斗中
        self.isFighting = False
        # 悬赏
        self.isXuanShang = False

    def get_scene(self, img_src):
        """
        识别当前场景
            :param img_src 当前场景图片
        """
        # 区分大场景
        imgs = {
            # 庭院
            'home': 'img/JIA-CHENG.png',
            # 探索页
            'tansuo':'img/JUE-XING.png',
            # 章节页
            'art': 'img/TAN-SUO.png',
            # 探索中
            'tansuoing': 'img/YING-BING.png',
            # 组队探索中
            'team_tansuo': 'img/DUI.png',
            # 结界突破
            'tupo': 'img/JIE-JIE-TU-PO.png',
            # 悬赏
            'xuanshang': 'img/XUAN-SHANG.png',
            # 战斗中
            'fighting': 'img/ZHUN-BEI.png',
        }
        result = {}
        maxVal_list = []
        maxLoc_list = []
        for item in imgs:
            # 开始识别
            img_template = cv2.imread(imgs[item])
            res = cv2.matchTemplate(
                img_src, img_template, cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
            if maxVal > 0.97:
                result[item] = True
            else:
                result[item] = False

        # 开始识别
        self.isHome = result.get('home')
        self.isArt = result.get('art')
        self.isTansuo = result.get('tansuo')
        self.isTanSuoIng = result.get('tansuoing')
        self.isTeamTansuoIng = result.get('team_tansuo')
        self.isFighting = result.get('fighting')
        self.isXuanShang = result.get('fighting')


    def getIsHome(self):
        """
        当前是否是庭院
        """
        return self.isHome

    def getIsTansuo(self):
        """
        当前是否是探索
        """
        return self.isTansuo

    def getIsTansuoIng(self):
        """
        是否再探索中
        """
        return self.isTanSuoIng

    def getIsTeamTansuo(self):
        """
        当前是否组队探索中
        """
        return self.isTeamTansuoIng

    def getIsFighting(self):
        """
        当前是否战斗中
        """
        return self.isFighting
