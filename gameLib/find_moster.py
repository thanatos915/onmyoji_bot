import cv2
from gameLib.moster import Moster

class FindMoster():

    def __init__(self):

        self.shishen_list = []


    def add(self, img_src, pos):
        """
        添加过滤式神
        """
        print(pos)
        cv2.imshow("image", img_src)
        cv2.waitKey(0)
        moster = Moster()
        return moster