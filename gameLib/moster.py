
class Moster():

    def __init__(self):
        # 查找次数
        self.find_times = 0
        # 式神截图
        self.img_src = None
        # 是否是经验怪
        self.is_exp = False
        # 式神位置

    def need_find(self):
        """
        是否需要查找
        """
        return self.find_times <= 6

    