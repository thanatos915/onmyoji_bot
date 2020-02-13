class GamePos():
    def __init__(self,pos,pos_end=None):
        self.pos=pos
        self.pos_end=pos_end

class CommonPos():
    second_position = (943, 56), (1111, 452)  # 第二次结算所点击的位置
    zhunbei_btn = (935, 465), (1080, 530)
    five_num_region = (418, 552), (762, 626) # 获取鬼火数量区域
    shishen_skill_one = (855, 580), (893, 610) # 式神一技能位置
    shishen_skill_two = (960, 580), (990, 610) # 式神一技能位置
    shishen_skill_three = (1060, 580), (1090, 610) # 式神一技能位置
    zi_dong_bth = (25, 570), (81, 615)
    enemy_region =  (192, 0), (1050, 210) # 地方式神位置
    cha_ji_change_skill_2 = (900, 450), (940, 490)
    cha_ji_change_skill_1 = (1040, 450), (1090, 490)

class TansuoPos():
    last_chapter = (934, 493), (1108, 572)  # 列表最后一章
    tansuo_btn=(787,458),(890,500) #探索按钮
    tansuo_denglong = (424, 118), (462, 158)  # 探索灯笼
    ready_btn = (1000, 460), (1069, 513)  # 准备按钮
    fight_quit=GamePos((1055,462),(1121,518)) #退出战斗
    quit_btn = (32, 45), (58, 64)  # 退出副本
    confirm_btn = (636, 350), (739, 370)  # 退出确认按钮
    change_monster = (427, 419), (457, 452)  # 切换狗粮点击区域
    quanbu_btn = (37, 574), (80, 604)  # “全部”按钮
    n_tab_btn = (142, 288), (164, 312)  # n卡标签
    s_tab_btn = (41, 272), (87, 303)  # n卡标签
    r_tab_btn = (221, 327), (259, 362)  # n卡标签
    n_slide = (168, 615), (784, 615)  # n卡进度条，从头至尾
    quit_change_monster=GamePos((19,17),(43,38)) #退出换狗粮界面
    gouliang_middle = (397, 218), (500, 349)  # 中间狗粮位置
    gouliang_right = (628, 293), (730, 430)  # 右边狗粮位置
    jie_shou_btn = (107, 203), (143, 251)  # 接受探索邀请
    gouliang_exp_passenger = (191, 134), (725, 470)  # 打手 狗粮查找位置
    gouliang_exp_driver = (1, 258), (547, 537)  # 打手 狗粮查找位置
    jixu_btn = (310, 372), (738, 400) #继续邀请队友
    ji_xu_btn = (672, 389), (680, 395) # 继续邀请



class YuhunPos():
    tiaozhan_btn = (995, 533), (1055, 595)    # 御魂挑战按钮
    kaishizhandou_btn = (1048, 535), (1113, 604)   # 御魂开始战斗按钮

class TuPoPos():
    refresh_btn = (860, 460), (1000, 500) # 结界刷新按钮
    refresh_sure_btn = (605, 365), (745, 400),

