from tkinter import *
import random
import time
import re
from tkinter import messagebox

class Mj:
    def __init__(self,sockfd):
        # 存储按钮对象
        self.sockfd = sockfd
        self.obj_but = {}  # 按钮对象与地址保存位置
        self.chupai = {}  # 选择出的牌
        self.url1 = []  # 图片对象
        self.paidui = []  # 牌堆
        self.qipaidui = []  # 弃牌堆
        self.root = Tk()
        self.root.geometry('1200x850+250+80')
        self.root.resizable(0, 0)
        self.pict = PhotoImage(file='bj.png')
        self.lab1 = Label(self.root, image=self.pict).pack()
        self.but2 = Button(self.root, text='发牌', font=('微软雅黑', 10), command=self.do_main).place(x=10, y=20)
        self.but3 = Button(self.root, text='摸牌', font=('微软雅黑', 10), command=self.putimg).place(x=50, y=20)
        self.img_start()
        self.root.mainloop()
    # 获得筛子
    def get_sz(self,shaizi):
        self.shaizi = shaizi  # 筛子

    def get_xy(self, event):
        print(event.x, event.y)

    # # 获得13张牌
    # def get_13(self,fapai):
    #     self.ser_send = fapai

    # 得到一张牌
    def get_card(self, card):
        self.come = card

    # c创建麻将
    def img_start(self):
        # self.ser_send.sort()
        # picc = [PhotoImage(file=i + '.png') for i in self.ser_send]
        # self.url1 = picc
        p1_x, p1_y = 820, 580  # 14对牌
        p2_x, p2_y = 240, 580  # 13对牌
        p3_x, p3_y = 339, 137  # 14对牌
        p4_x, p4_y = 911, 137  # 13对牌
        for j in range(0, 108):
            picc = PhotoImage(file='bei2.png')
            lab = Label(self.root, image=picc)
            lab.image = picc
            picc1 = PhotoImage(file='bei.png')
            lab1 = Label(self.root, image=picc1)
            lab1.image = picc1
            lab.bind('<1>', self.get_xy)
            lab1.bind('<1>', self.get_xy)
            # 1号位置
            if j <= 13:
                lab.place(x=p1_x, y=p1_y)
                p1_x -= 37
            if 13 < j <= 27:
                p1_x += 37
                p1_y = 575
                lab.place(x=p1_x, y=p1_y)
            # 2号位置
            if 27 < j <= 40:
                lab1.place(x=p2_x, y=p2_y)
                p2_y -= 37
            if 40 < j <= 53:
                p2_y += 37
                p2_x = 245
                lab1.place(x=p2_x, y=p2_y)
            # 3号位置
            if 53 < j <= 67:
                lab.place(x=p3_x, y=p3_y)
                p3_x += 37
            if 67 < j <= 81:
                p3_x -= 37
                p3_y = 133
                lab.place(x=p3_x, y=p3_y)
            # 4号位置
            if 81 < j <= 94:
                lab1.place(x=p4_x, y=p4_y)
                p4_y += 37
            if 94 < j <= 107:
                p4_y -= 37
                p4_x = 915
                lab1.place(x=p4_x, y=p4_y)
        # self.but3.destroy()

    def img_heigh(self, event):
        wid = event.widget
        if wid in self.obj_but:
            wid.place(x=self.obj_but[wid], y=680)
        else:
            wid.place(x=1050, y=680)

    def img_low(self, event):
        wid = event.widget
        if wid in self.obj_but:
            wid.place(x=self.obj_but[wid], y=700)
        else:
            wid.place(x=1050, y=700)

    # 出牌
    def img_del(self, event):
        wid = event.widget
        img = wid.image['file']
        self.ser_send.remove(img[:2])  # 删除打出的牌
        self.ser_send.append(self.come)  # 添加发过来的牌
        self.url1.clear()  # 清空原图片对象
        self.img_url()  # 调用图片对象生成函数，重新生成图片对象
        b = self.url1.copy()
        for i in self.obj_but:
            for j in b:
                i['image'] = j
                i.image = j
                b.remove(j)
                break
        a = self.chupai.keys()
        for j in a:
            j.destroy()

    # 删除单独发过来的牌
    def img_del2(self, event):
        wid = event.widget
        wid.destroy()

    # 创建来牌图片
    def putimg(self):
        img = PhotoImage(file=(self.come+'.png'))
        but3 = Button(self.root, command=self.img_del, image=img, bg='#025237')
        but3.image = img
        but3.bind('<Enter>', self.img_heigh)
        but3.bind('<Leave>', self.img_low)
        but3.bind('<1>', self.img_del2)
        self.chupai[but3] = (1100)
        but3.place(x=1050, y=700)

    # 得到十三张牌
    def but_max(self):
        # 初始坐标
        p1_x_s = 80
        p1_y_s = 700
        for i in self.url1:
            lab = Label(self.root, image=i, bg='#025237')
            lab.image = i
            lab.bind('<Enter>', self.img_heigh)
            lab.bind('<Leave>', self.img_low)
            lab.bind('<1>', self.img_del)
            lab.place(x=p1_x_s, y=p1_y_s)
            self.obj_but[lab] = p1_x_s
            p1_x_s += 71
        p2_x_s = 100
        p2_y_s = 600
        for j in range(13):
            j_img = PhotoImage(file='left-1.png')
            lab2 = Label(self.root, image=j_img, bg='#025237')
            lab2.image = j_img
            lab2.place(x=p2_x_s, y=p2_y_s)
            p2_y_s -= 40
        p3_x_s = 340
        p3_y_s = 40
        for j in range(13):
            j_img = PhotoImage(file='dm.png')
            lab3 = Label(self.root, image=j_img, bg='#025237')
            lab3.image = j_img
            lab3.place(x=p3_x_s, y=p3_y_s)
            p3_x_s += 38
        p4_x_s = 1070
        p4_y_s = 130
        for j in range(13):
            j_img = PhotoImage(file='right.png')
            lab3 = Label(self.root, image=j_img, bg='#025237')
            lab3.image = j_img
            lab3.place(x=p4_x_s, y=p4_y_s)
            p4_y_s += 40

    def show_order(self, a, b, c):
        url_sz0 = './mj/sz'+a+'.png'
        url_sz1 = './mj/sz'+b+'.png'
        print(url_sz0,url_sz0)
        picc0 = PhotoImage(file=url_sz0)
        lab0 = Label(self.root, image=picc0)
        lab0.image = picc0
        lab0.place(x=600, y=300)
        picc1 = PhotoImage(file=url_sz1)
        lab1 = Label(self.root, image=picc1)
        lab1.image = picc1
        lab1.place(x=520, y=300)
        messagebox.showinfo('轮换开始', '庄家是：'+c)
        lab0.destroy()
        lab1.destroy()
        self.sockfd.send(b'P fapai')
    # 重复接收服务器消息，展示消息
    def do_main(self):
        # while True:
            self.sockfd.send(b'P sz')
            data1 = self.sockfd.recv(1024).decode()
            data = data1.split(' ')
            # 先摇一摇筛子
            if data[0] == 'sz':
                print(data[0], data[1], data[2], data[3])
                self.show_order(data[1], data[2], data[3])
            if data[0] == 'fapai':
                b = data[1:]
                self.ser_send = b
                self.img_url()
                self.but_max()

    def img_url(self):
        self.ser_send.sort()
        picc = [PhotoImage(file=i + '.png') for i in self.ser_send]
        self.url1 = picc
        # self.but3.destroy()

