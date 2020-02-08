import ctypes
import sys

from PIL import Image

from gameLib.game_ctl import GameControl

import cv2
import numpy
import win32con
import win32gui
import win32ui
import numpy as np

# team_id = 1
# min = (team_id - 1) * 86 + (team_id - 1) * 100 + 110
# max = min + 100
# pos = (min, 330), (max, 445)
#
# print(pos)

hwnd = win32gui.FindWindow(0, u'阴阳师-网易游戏')

crl = GameControl(hwnd)
# crl.takescreenshot()

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
