import ctypes
import os
import sys
import time

from PIL import Image

from gameLib.game_ctl import GameControl

import cv2
import numpy
import win32con
import win32gui
import win32ui
import numpy as np
from explore.passenger_explore import PassengerExplore
from explore.driver_explore import DriverExplore
from boundary.boundary import Boundary

def is_admin():
    # UAC申请，获得管理员权限
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# print(a)a = np.array(np.array([[[674, 498], [655, 512], [683, 528], [789, 508]]]).min()).min()

# img_src = cv2.imread('img/1581315668.159217_color.png')
# # 140 185
# # 150 195
# new_img = img_src[192:200, 140:145]
# img = Image.fromarray(new_img, 'RGB')
# # cv2.imwrite('img/{0}_color.png'.format(time.time()), img_src)
# width, height = img.size
# print(width,height)
# tolerance = 20
# r1, g1, b1 = (134, 227, 96)
# for x in range(width):
#     for y in range(height):
#         try:
#             pixel = img.getpixel((x, y))
#             r2, g2, b2 = pixel[:3]
#             print(r2,g2,b2)
#             if abs(r1 - r2) <= tolerance and abs(g1 - g2) <= tolerance and abs(b1 - b2) <= tolerance:
#                print(x, y)
#         except:
#             print('err')

# img_src = cv2.imread('img/1581224732.8175466_color.png')
# img = Image.fromarray(img_src, 'RGB')
# color = (140, 122, 44)
# tolerance = 10
#
# width, height = img.size
# r1, g1, b1 = color[:3]
# for x in range(width):
#     for y in range(height):
#         try:
#             pixel = img.getpixel((x, y))
#             r2, g2, b2 = pixel[:3]
#             if abs(r1-r2) <= tolerance and abs(g1-g2) <= tolerance and abs(b1-b2) <= tolerance:
#                 print(x,y)
#         except:
#             print('err')

# team_id = 1
# min = (team_id - 1) * 86 + (team_id - 1) * 100 + 110
# max = min + 100
# pos = (min, 330), (max, 445)
#
# # print(pos)

# hwnd = win32gui.FindWindow(0, u'阴阳师-网易游戏')
# crl = GameControl(hwnd)
# crl.takescreenshot()
# img_src = crl.window_part_shot((139, 432), (964, 640))
#
# x1 = 96 *
# print(x1)
# print(img_src.shape)
# number = 7
# x1 = (96 + 15) * (number - 1)
# x2 = (96 + 15) * number + 8
# new_img = img_src[0:208, x1:x2]
# cv2.imshow("image", img_src)
# cv2.waitKey(0)
# # 检查是否出战
# tml_img = cv2.imread('img/ZHAN-DOU.png')
# res = cv2.matchTemplate(new_img, tml_img, cv2.TM_CCOEFF_NORMED)
# minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
# print(maxVal, maxLoc)
# # 检查是否观战
# tml_img = cv2.imread('img/EYES.png')
# res = cv2.matchTemplate(new_img, tml_img, cv2.TM_CCOEFF_NORMED)
# minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
# print(maxVal, maxLoc)
# # 检查是否满级
# tml_img = cv2.imread('img/SHI-SHEN-MAN.png')
# res = cv2.matchTemplate(new_img, tml_img, cv2.TM_CCOEFF_NORMED)
# minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
# print(maxVal, maxLoc)
# # 检查是不是白蛋
# tml_img = cv2.imread('img/BAI-DAN.png')
# res = cv2.matchTemplate(new_img, tml_img, cv2.TM_CCOEFF_NORMED)
# minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
# print(maxVal, maxLoc)
# cv2.imshow("image", new_img)
# cv2.waitKey(0)
# replace_pos = ([(953, 315), (554, 315), (187, 315)])
# shi_shen_pos = 0
# next_index = -1
# for item in replace_pos:
#     if replace_pos[shi_shen_pos] == item:
#         next_index = shi_shen_pos + 1
# if replace_pos[next_index]:
#     shi_shen_pos = next_index
# else:
#     shi_shen_pos = -1
# print(shi_shen_pos)
# hwnd = win32gui.FindWindow(0, u'阴阳师-网易游戏')
# yys = GameControl(hwnd)
# maxVal, maxLoc = yys.find_img('img/PROGESS.png')
# print(maxVal, maxLoc)
#
try:
    # 检测管理员权限
    if is_admin():
        hwnd = win32gui.FindWindow(0, u'阴阳师-网易游戏')
        crl = DriverExplore(hwnd)
        # maxVal, maxLoc = crl.find_multi_img('img/ZI-DONG.png', 'img/DUI.png', 'img/YING-BING.png')
        num = crl.test()
        print(num)
        # crl = GameControl(hwnd)
        # loc = crl.find_game_img('img/XUE-TIAO.png', 1, (192, 0), (1050, 210), 0, 0.7)
        # print(loc)
        # crl.takescreenshot()
        # crl.get_five_num()

    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
except KeyboardInterrupt:
    print('err')
    os.system('pause')
else:
    os.system('pause')


# img_src = cv2.imread('img/full.png')
#
# img_template = cv2.imread('img/SHI-SHEN-NUM.png')
#
# res = cv2.matchTemplate(img_src, img_template, cv2.TM_CCOEFF_NORMED)
# minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
# print(maxVal, maxLoc)
# th, tw = img_template.shape[:2]
# tl = maxLoc
# br = (tl[0] + tw , tl[1] + th)
# cv2.rectangle(img_src, tl, br, [255, 0, 0], 2)
# cv2.imshow("image", img_src)
# cv2.waitKey(0)
#
# print(maxVal, maxLoc)

"""
crl = GameControl(hwnd)
# maxVal, maxLoc = crl.find_multi_img('img/ZI-DONG.png', 'img/DUI.png', 'img/YING-BING.png')
# print(maxVal, maxLoc)
print(crl.find_img('img/TIAO-ZHAN.png'))

crl.takescreenshot()


# crl.takescreenshot()

img_src = cv2.imread('img/full.png')

img_template = cv2.imread('img/DUI.png')

res = cv2.matchTemplate(
    img_src, img_template, cv2.TM_CCOEFF_NORMED)
minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
print(maxVal, maxLoc)

"""

""""
team_id = 5
min = (team_id - 1) * 86 + (team_id - 1) * 100 + 110
max = min + 100
pos = (min, 330), (max, 445)
print(pos)
print(pos[0])
# img = Image.fromarray(crl.window_part_shot(pos[0], pos[1]), 'RGB')

color = (88, 160, 21)
img = cv2.imread('img/full.png')
cropped = img[y1:y2, x1:x2]
cv2.imshow("image", cropped)
cv2.waitKey(0)
img = Image.fromarray(cropped, 'RGB')
width, height = img.size
tolerance = 10
r1, g1, b1 = color[:3]

for x in range(width):
    for y in range(height):
        try:
            pixel = img.getpixel((x, y))
            r2, g2, b2 = pixel[:3]
            if abs(r1 - r2) <= tolerance and abs(g1 - g2) <= tolerance and abs(b1 - b2) <= tolerance:
                print(x, y)
        except:
            print('err')
"""