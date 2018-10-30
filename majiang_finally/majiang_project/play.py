# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from tkinter import *
import random
import threading
import time
import re
from tkinter import messagebox
from threading import Timer
import chatroom_client



class Mj:
    def __init__(self, userName, sockfd):
        self.userName = userName
        # 存储按钮对象
        self.sockfd = sockfd
        # self.prePlayer = ''
        self.obj_but = {}  # 按钮对象与地址保存位置
        self.obj_but2 = []
        self.chupai = []  # 选择出的牌
        self.url1 = []  # 图片对象
        self.paidui = []  # 牌堆
        self.qipai = []  # 弃牌堆
        self.qipaiduixiang = []  # 弃牌堆对象，初始化处理
        self.p1qipai = [[], []]  # 存放p1的摸牌堆第二层、第一层
        self.p2qipai = [[], []]  # 存放p2的摸牌堆第二层、第一层
        self.p3qipai = [[], []]  # 存放p3的摸牌堆第二层、第一层
        self.p4qipai = [[], []]  # 存放p4的摸牌堆第二层、第一层
        self.display = [[], []]  # 存放碰杠牌
        self.pg_position = [[300, 620, []], [
            180, 140, []], [850, 70, []], [970, 640, []]]
        self.root = Tk()
        self.root.geometry('1200x850+250+80')
        self.root.resizable(0, 0)
        self.pict = PhotoImage(file='./playImg/bj.png')
        self.lab1 = Label(self.root, image=self.pict).pack()
        self.but2 = Button(self.root, text='准备', font=(
            '微软雅黑', 10), command=self.send_ready)
        self.but2.place(x=600, y=425)
        # self.peng_img = PhotoImage(file='./playImg/peng.png')
        # self.guo_img = PhotoImage(file='./playImg/pass.png')
        # self.gang_img = PhotoImage(file='./playImg/gang.png')
        # self.hu_img = PhotoImage(file='./playImg/hu.png')
        self.img_start()
        self.root.mainloop()

    # c创建麻将
    def img_start(self):
        p1_x, p1_y = 850, 640  # 15对牌2
        p2_x, p2_y = 260, 650  # 15对牌4
        p3_x, p3_y = 339, 137  # 15对牌2
        p4_x, p4_y = 911, 137  # 15对牌4
        for j in range(0, 120):
            picc = PhotoImage(file='./playImg/bei2.png')  # 上下图片
            lab = Label(self.root, image=picc)
            lab.image = picc
            picc1 = PhotoImage(file='./playImg/bei.png')  # 左右图片
            lab1 = Label(self.root, image=picc1)
            lab1.image = picc1
            # 1号位置
            if j <= 14:  # [12 11] [22 21] [32 31] [42 41]
                lab.place(x=p1_x, y=p1_y)
                self.p1qipai[1].append(lab)
                p1_x -= 37
            if 14 < j <= 29:
                p1_x += 37
                p1_y = 635
                lab.place(x=p1_x, y=p1_y)
                self.p1qipai[0].append(lab)
            # 2号位置
            if 29 < j <= 44:
                lab1.place(x=p2_x, y=p2_y)
                self.p2qipai[1].append(lab1)
                p2_y -= 37
            if 44 < j <= 59:
                p2_y += 37
                p2_x = 255
                lab1.place(x=p2_x, y=p2_y)
                self.p2qipai[0].append(lab1)
            # 3号位置
            if 59 < j <= 74:
                lab.place(x=p3_x, y=p3_y)
                self.p3qipai[1].append(lab)
                p3_x += 37
            if 74 < j <= 89:
                p3_x -= 37
                p3_y = 133
                lab.place(x=p3_x, y=p3_y)
                self.p3qipai[0].append(lab)
            # 4号位置
            if 89 < j <= 104:
                lab1.place(x=p4_x, y=p4_y)
                self.p4qipai[1].append(lab1)
                p4_y += 37
            if 104 < j <= 119:
                p4_y -= 37
                p4_x = 915
                lab1.place(x=p4_x, y=p4_y)
                self.p4qipai[0].append(lab1)
    #　动画效果

    def img_heigh(self, event):
        wid = event.widget
        if wid in self.obj_but:
            wid.place(x=self.obj_but[wid], y=680)
        else:
            wid.place(x=1050, y=680)
    #　动画效果

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
        try:
            if self.come != '':
                self.ser_send.append(self.come)  # 添加发过来的牌
            elif self.come == '':
                a = self.obj_but2.pop()
                a.destroy()
                del self.obj_but[a]
                self.ser_send.remove(img[10:12])  # 原始服务器发送牌减对应牌
                self.url1.clear()  # 清空原图片对象
                self.img_url()  # 调用图片对象生成函数，重新生图成片对象
                b = self.url1.copy()
                msg = 'CP ' + img[10:12]
                self.sockfd.send(msg.encode())
                for i in self.obj_but2:
                    for j in b:
                        i['image'] = j
                        i.image = j
                        b.remove(j)
                        break
                self.qipai.append(img)  # 弃牌堆添加打出去的牌xx.png格式
                self.createCenter()  # 显示在中心出去的牌
                del self.come  # 删除出牌对象
                self.chupai.clear()  # 清空出牌列表
                return
        except AttributeError:
            messagebox.showinfo('提示', '还没到你出牌')
            return
        self.qipai.append(img)  # 弃牌堆添加打出去的牌xx.png格式
        self.ser_send.remove(str(img[10:12]))  # 删除打出的牌
        msg = 'CP ' + img[10:12]
        self.sockfd.send(msg.encode())
        self.createCenter()  # 显示出牌
        self.url1.clear()  # 清空原图片对象
        self.img_url()  # 调用图片对象生成函数，重新生成图片对象
        b = self.url1.copy()
        for i in self.obj_but2:
            for j in b:
                i['image'] = j
                i.image = j
                b.remove(j)
                break
        for i in self.chupai:
            i[0].destroy()
        del self.come  # 删除出牌对象
        self.chupai.clear()  # 清空出牌列表

    # 桌面显示出牌
    def createCenter(self):
        '''出的牌存放在桌面上的位置'''
        j = 45
        i = 0
        q_x = 300
        q_y = 185
        length = len(self.qipai)
        for le in range(length):
            if i == 15:
                i = 1
                q_x = 300  # x的值回归
                q_y += j
            q_x += 37
            i += 1
        # print(self.qipai)
        url = self.qipai[-1]
        url = url[10:]
        url = "cpImage/" + url
        image = PhotoImage(file=url)
        b = Label(self.root, image=image)
        b.image = image
        b.place(x=q_x, y=q_y)
        self.qipaiduixiang.append(b)
    # 桌牌减一

    def table_plus(self):  # 桌牌减一
        self.total[0].destroy()
        self.total.remove(self.total[0])

    # 显示自己的碰、杠牌
    # def show_pg(self):
    #     pg_img = PhotoImage(file="cpImage/" + self.card + ".png")
    #     pg_lab = Label(self.root, image=pg_img)
    #     pg_lab.image = pg_img
    #     pg_lab.place(x=self.pg_position[0][0] + pg_x, y=620)
    #     self.pg_position[0][0] += 37
    #     self.display[1].append(pg_lab)
    #     if pg_x > 818:
    #         messagebox.showinfo('我去', '你怎么有这么多牌')

    # 删除单独发过来的牌
    def img_del2(self, event):
        wid = event.widget
        img = wid.image['file']
        self.qipai.append(img)  # 弃牌堆添加打出去的牌xx.png格式
        self.createCenter()
        wid.destroy()
        msg = 'CP ' + img[10:12]
        self.sockfd.send(msg.encode())
        del self.come  # 删除出牌对象
        self.chupai.clear()  # 清空出牌列表

    # 得到一张牌,创建来牌按钮
    def get_one(self, card):
        self.come = card
        img = PhotoImage(file=('./playImg/' + self.come + '.png'))
        but3 = Button(self.root, command=self.img_del, image=img, bg='#025237')
        but3.image = img
        but3.bind('<Enter>', self.img_heigh)
        but3.bind('<Leave>', self.img_low)
        but3.bind('<1>', self.img_del2)
        self.chupai.append((but3, 1100))
        but3.place(x=1050, y=700)
        self.table_plus()  # 牌堆减一

    # 十三张牌对象，排序
    def img_url(self):
        self.ser_send.sort()
        picc = [PhotoImage(file='./playImg/' + i + '.png')
                           for i in self.ser_send]
        self.url1 = picc

    # 得到十三张牌
    def but_max(self, name, firstPlayer):
        self.clearLaber = []
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
            self.obj_but2.append(lab)
            p1_x_s += 71
        p2_x_s = 100
        p2_y_s = 600
        for j in range(13):
            j_img = PhotoImage(file='./playImg/left-1.png')
            lab2 = Label(self.root, image=j_img, bg='#025237')
            lab2.image = j_img
            lab2.place(x=p2_x_s, y=p2_y_s)
            p2_y_s -= 40
            self.clearLaber.append(lab2)  # 　列表添加对象方便后期初始化
        p3_x_s = 340
        p3_y_s = 10
        for j in range(13):
            j_img = PhotoImage(file='./playImg/dm.png')
            lab3 = Label(self.root, image=j_img, bg='#025237')
            lab3.image = j_img
            lab3.place(x=p3_x_s, y=p3_y_s)
            p3_x_s += 38
            self.clearLaber.append(lab3)  # 　列表添加对象方便后期初始化
        p4_x_s = 1070
        p4_y_s = 130
        for j in range(13):
            j_img = PhotoImage(file='./playImg/right.png')
            lab4 = Label(self.root, image=j_img, bg='#025237')
            lab4.image = j_img
            lab4.place(x=p4_x_s, y=p4_y_s)
            p4_y_s += 40
            self.clearLaber.append(lab4)  # 　列表添加对象方便后期初始化
        self.total = []  # 顺序生成摸牌堆，创建copy()对象c方便比照删除
        a = self.p1qipai[0][::-1]
        b = self.p1qipai[1]
        for i in a:
            for j in b:
                self.total.append(i)
                self.total.append(j)
                b.remove(j)
                break
        a = self.p2qipai[0][::-1]
        b = self.p2qipai[1]
        for i in a:
            for j in b:
                self.total.append(i)
                self.total.append(j)
                b.remove(j)
                break
        a = self.p3qipai[0][::-1]
        b = self.p3qipai[1]
        for i in a:
            for j in b:
                self.total.append(i)
                self.total.append(j)
                b.remove(j)
                break
        a = self.p4qipai[0][::-1]
        b = self.p4qipai[1]
        for i in a:
            for j in b:
                self.total.append(i)
                self.total.append(j)
                b.remove(j)
                break
        n = 0
        c = self.total.copy()
        for i in c:
            self.total.remove(i)
            i.destroy()
            n += 1
            if n == 52:
                break
        del n
        del c
        self.p1qipai = [[], []]
        self.p2qipai = [[], []]
        self.p3qipai = [[], []]
        self.p4qipai = [[], []]
        msg = 'OK ' + self.userName + ' ' + firstPlayer
        self.sockfd.send(msg.encode())
        self.handler()

    # 显示筛子信息
    def show_order(self, a, b, c):
        url_sz0 = './playImg/mj/sz' + a + '.png'
        url_sz1 = './playImg/mj/sz' + b + '.png'
        picc0 = PhotoImage(file=url_sz0)
        self.lab0 = Label(self.root, image=picc0, bd=0)
        self.lab0.image = picc0
        self.lab0.place(x=600, y=300)
        picc1 = PhotoImage(file=url_sz1)
        self.lab1 = Label(self.root, image=picc1, bd=0)
        self.lab1.image = picc1
        self.lab1.place(x=520, y=300)
        wait = Timer(3, self.wait)
        wait.start()
        msg = 'FP ' + self.userName
        self.sockfd.send(msg.encode())
        self.handler()

    # 删除筛子
    def wait(self):
        self.lab0.destroy()
        self.lab1.destroy()
    # 碰函数

    def Peng(self, event):
        '''碰牌事件'''
        # img = "./playImg/" + self.card + ".png"
        # for i in range(3):
        #     self.display[0].append(img)  # 弃牌堆添加出去的牌
        #     self.show_pg()  # 桌面出去的牌
        self.show_other_pg(self.name, self.card)
        self.ser_send.remove(self.card)
        self.ser_send.remove(self.card)
        self.obj_but2[-1].destroy()
        a = self.obj_but2.pop()
        del self.obj_but[a]
        self.obj_but2[-1].destroy()
        a = self.obj_but2.pop()
        del self.obj_but[a]
        self.url1.clear()  # 清空原图片对象
        self.img_url()  # 调用图片对象生成函数，重新生图成片对象
        b = self.url1.copy()
        for i in self.obj_but2:
            for j in b:
                i['image'] = j
                i.image = j
                b.remove(j)
                break
        msg = 'M ' + self.card + ' ' + self.card
        self.sockfd.send(msg.encode())
        self.cPeng.destroy()
        self.btn_pas.destroy()

    # 碰按钮
    def peng_btn_list(self, name, card):
        '''碰牌按钮'''
        self.card = card
        self.name = name
        self.peng_img = PhotoImage(file='./playImg/peng.png')
        self.cPeng = Label(self.root, image=self.peng_img, bd=0)
        self.cPeng.bind('<1>', self.Peng)
        self.cPeng.place(x=600, y=620)

        self.guo_img = PhotoImage(file='./playImg/pass.png')
        self.btn_pas = Label(self.root, image=self.guo_img, bd=0)
        self.btn_pas.bind('<1>', self.pas)
        self.btn_pas.place(x=650, y=620)
    # 过按钮

    def pas(self, event):
        try:
            self.btn_gang.destroy()
        except:
            pass
        try:
            self.btn_hu.destroy()
        except:
            pass
        msg = 'Guo ' + self.prePlayer
        self.sockfd.send(msg.encode())
        self.cPeng.destroy()
        self.btn_pas.destroy()

    # 杠按钮
    def gang_btn_list(self, name, card, cmd):
        # b = data.split(' ')
        # print(b)
        self.card = card# 碰牌
        self.name = name  # 碰牌人姓名
        if cmd == 'ZG':
            # self.btn_gang=Button(self.root,text="自杠",bg="#014C33",command =self.zigang)
            # self.btn_gang.place(x=550,y=620)

            self.peng_img = PhotoImage(file='./playImg/peng.png')
            self.cPeng = Label(self.root, image=self.peng_img, bd=0)
            self.cPeng.bind('<1>', self.Peng)
            self.cPeng.place(x=600, y=620)

            self.guo_img = PhotoImage(file='./playImg/pass.png')
            self.btn_pas = Label(self.root, image=self.guo_img, bd=0)
            self.btn_pas.bind('<1>', self.pas)
            self.btn_pas.place(x=650, y=620)
        else:
            self.gang_img = PhotoImage(file='./playImg/gang.png')
            self.btn_gang = Label(self.root, image=self.gang_img, bd=0)
            self.btn_gang.bind('<1>', self.gang)
            self.btn_gang.place(x=550, y=620)

            self.peng_img = PhotoImage(file='./playImg/peng.png')
            self.cPeng = Label(self.root, image=self.peng_img, bd=0)
            self.cPeng.bind('<1>', self.Peng)
            self.cPeng.place(x=600, y=620)

            self.guo_img = PhotoImage(file='./playImg/pass.png')
            self.btn_pas = Label(self.root, image=self.guo_img, bd=0)
            self.btn_pas.bind('<1>', self.pas)
            self.btn_pas.place(x=650, y=620)

    # 杠
    def gang(self, event):
        if self.ser_send.count(self.card) == 4:
            print('g1')
            img = "./playImg/" + self.card + ".png"
            for i in range(4):
                self.ser_send.remove(self.card)  # 删除杠牌删除
            self.url1.clear()  # 清空图片对象
            self.img_url()  # 重新生成图片对象
            self.obj_but2[-1].destroy()  # 删除列表字典对应按钮对象
            for i in range(4):
                a = self.obj_but2.pop()
                del self.obj_but[a]
                self.obj_but2[-1].destroy()
            b = self.url1.copy()
            for i in self.obj_but2:
                for j in b:
                    i['image'] = j
                    i.image = j
                    b.remove(j)
                    break
            # for i in range(4):  # 展示自己碰杠
            #     self.display[0].append(img)
            #     self.show_pg()
            print('self.name---',self.name)
            print('self.card---',self.card)
            self.show_other_pg(self.name, self.card)
            msg = 'M ' + self.card + ' ' + self.card + ' ' + self.card + ' ' + self.card
            self.sockfd.send(msg.encode())
        # 杠其他玩家
        if self.ser_send.count(self.card) == 3 and self.chupai == []:
            print('g2')
            print(self.chupai)
            for i in range(3):
                self.ser_send.remove(self.card)  # 删除杠牌删除
            self.img_url()  # 重新生成图片对象
            for i in range(3):
                self.obj_but2[-1].destroy()  # 删除对应控件对象
                a = self.obj_but2.pop()  # 删除列表对应控件对象元素
                del self.obj_but[a]  # 删除字典对应控件对象元素
            b = self.url1.copy()
            for i in self.obj_but2:  # 按钮重新绑定图片
                for j in b:
                    i['image'] = j
                    i.image = j
                    b.remove(j)
                    break
            img = "./playImg/" + self.card + ".png"
            # for i in range(4):
            #     self.display[0].append(img)
            #     self.show_pg()
            self.show_other_pg(self.name, self.card)
            msg = 'M ' + self.card + ' ' + self.card + ' ' + self.card
            self.sockfd.send(msg.encode())
            # 自摸第四张杠
        if self.ser_send.count(self.card) == 3 and self.chupai != []:
            self.chupai[0][0].destroy()
            del self.come  # 删除出牌对象
            self.chupai.clear()  # 清空出牌列表
            msg = 'M ' + self.card + ' ' + self.card + ' ' + self.card
            self.sockfd.send(msg.encode())
            for i in range(3):
                self.ser_send.remove(self.card)  # 删除杠牌删除
            self.img_url()  # 重新生成图片对象
            for i in range(3):
                self.obj_but2[-1].destroy()  # 删除对应控件对象
                a = self.obj_but2.pop()  # 删除列表对应控件对象元素
                del self.obj_but[a]  # 删除字典对应控件对象元素
            b = self.url1.copy()
            for i in self.obj_but2:  # 按钮重新绑定图片
                for j in b:
                    i['image'] = j
                    i.image = j
                    b.remove(j)
                    break
            # img = "./playImg/" + self.card + ".png"
            # for i in range(4):
            #     self.display[0].append(img)
            #     self.show_pg()
        try:
            self.hu_btn.destroy()
        except:
            pass
        self.btn_gang.destroy()
        self.cPeng.destroy()
        self.btn_pas.destroy()

    def checkHuPai(self, name, board, cmd):
        # if cmd == 'ZG':
        #     self.gang_btn_list(data1)
        if cmd == 'GP':
            self.gang_btn_list(name, board, cmd)
        if cmd == 'PP':
            self.peng_btn_list(name, board)
        if cmd == "HP":
            self.hu_btn(name)
        if cmd == 'HPGP':
            # 胡牌杠牌
            self.hu_btn(name)
            self.gang_btn_list(cmd, board)
        if cmd == 'HPPP':
            # 胡牌碰牌
            self.hu_btn(name)
            self.peng_btn_list(board)
        if cmd == 'G':
            pass

    def send_ready(self):
        msg = 'P ' + self.userName
        self.sockfd.send(msg.encode())
        self.but2.destroy()
        t = threading.Thread(target=self.handler)
        t2 = threading.Thread(target = chatroom_client.startChatroomClient, args = (self.userName,))
        t.setDaemon(True)
        t2.setDaemon(True)
        t.start()
        t2.start()

    def hu_btn(self, userwin):
        self.userwin = userwin
        self.hu_img = PhotoImage(file='./playImg/hu.png')
        self.btn_hu = Button(self.root, image=self.hu_img, command=self.hu, bd=0)
        self.btn_hu.place(x=550, y=620)

        self.guo_img = PhotoImage(file='./playImg/pass.png')
        self.btn_pas = Label(self.root, image=self.guo_img, bd=0)
        self.btn_pas.bind('<1>', self.pas)
        self.btn_pas.place(x=650, y=620)

    def show_other_pg(self, user, lst):
        # num为具体碰还是杠，需要知道显示的数量
        index_first = self.seatPosition.index(self.name)  # 判断自己的顺序编号
        index_after = self.seatPosition.index(user)  # 判断事件玩家的顺序编号
        print('自己的编号', index_first)
        print("事件玩家编号", index_after)
        if type(lst) is list:
            card = lst[0]
            num = len(lst) + 1
        else:
            card = lst
            if self.ser_send.count(card) == 2:
                num = 3
            else:
                num = 4
        if index_first == 0:
            if index_after == 0:
                for i in range(num):
                    img = PhotoImage(file="cpImage/" + card + ".png")
                    lab = Label(self.root, image=img)
                    lab.image = img
                    lab.place(x=self.pg_position[0][0], y=self.pg_position[0][1])
                    self.pg_position[0][0] += 37
                    self.pg_position[0][2].append(lab)
            if index_after == 1:
                for i in range(num):
                    img = PhotoImage(file="cpImagel/" + card + ".png")
                    lab = Label(self.root, image=img)
                    lab.image = img
                    lab.place(x=self.pg_position[1][0], y=self.pg_position[1][1])
                    self.pg_position[1][1] += 37
                    self.pg_position[1][2].append(lab)
            if index_after == 2:
                for i in range(num):
                    img = PhotoImage(file="cpImaged/" + card + ".png")
                    lab = Label(self.root, image=img)
                    lab.image = img
                    lab.place(x=self.pg_position[2][
                              0], y=self.pg_position[2][1])
                    self.pg_position[2][0] -= 37
                    self.pg_position[2][2].append(lab)
            if index_after == 3:
                for i in range(num):
                    img = PhotoImage(file="cpImager/" + card + ".png")
                    lab = Label(self.root, image=img)
                    lab.image = img
                    lab.place(x=self.pg_position[3][
                              0], y=self.pg_position[3][1])
                    self.pg_position[3][1] -= 37
                    self.pg_position[3][2].append(lab)
        if index_first == 1: 
            if index_after == 1:
                for i in range(num):
                    img = PhotoImage(file="cpImage/" + card + ".png")
                    lab = Label(self.root, image=img)
                    lab.image = img
                    lab.place(x=self.pg_position[0][0], y=self.pg_position[0][1])
                    self.pg_position[0][0] += 37
                    self.pg_position[0][2].append(lab)
            if index_after == 2:
                for i in range(num):
                    img = PhotoImage(file="cpImagel/"+card+".png")
                    lab = Label(self.root, image=img)
                    lab.image = img
                    lab.place(x=self.pg_position[1][0], y=self.pg_position[1][1])
                    self.pg_position[1][1] += 37
                    self.pg_position[1][2].append(lab)
            if index_after == 3:
                for i in range(num):
                    img = PhotoImage(file="cpImaged/"+card+".png")
                    lab = Label(self.root, image=img)
                    lab.image = img
                    lab.place(x=self.pg_position[2][0], y=self.pg_position[2][1])
                    self.pg_position[2][0] -= 37
                    self.pg_position[2][2].append(lab)
            if index_after == 0:
                for i in range(num):
                    img = PhotoImage(file="cpImager/"+card+".png")
                    lab = Label(self.root, image=img)
                    lab.image = img
                    lab.place(x=self.pg_position[3][0], y=self.pg_position[3][1])
                    self.pg_position[3][1] -= 37
                    self.pg_position[3][2].append(lab)
        if index_first == 2:
            if index_after == 2:
                for i in range(num):
                    img = PhotoImage(file="cpImage/" + card + ".png")
                    lab = Label(self.root, image=img)
                    lab.image = img
                    lab.place(x=self.pg_position[0][0], y=self.pg_position[0][1])
                    self.pg_position[0][0] += 37
                    self.pg_position[0][2].append(lab)     
            if index_after == 3:
                for i in range(num):
                    img = PhotoImage(file="cpImagel/"+card+".png")
                    lab = Label(self.root, image=img)
                    lab.image = img
                    lab.place(x=self.pg_position[1][0], y=self.pg_position[1][1])
                    self.pg_position[1][1] += 37
                    self.pg_position[1][2].append(lab)
            if index_after == 0:
                for i in range(num):
                    img = PhotoImage(file="cpImaged/"+card+".png")
                    lab = Label(self.root, image=img)
                    lab.image = img
                    lab.place(x=self.pg_position[2][0], y=self.pg_position[2][1])
                    self.pg_position[2][0] -= 37
                    self.pg_position[2][2].append(lab)
            if index_after == 1:
                for i in range(num):
                    img = PhotoImage(file="cpImager/"+card+".png")
                    lab = Label(self.root, image=img)
                    lab.image = img
                    lab.place(x=self.pg_position[3][0], y=self.pg_position[3][1])
                    self.pg_position[3][1] -= 37
                    self.pg_position[3][2].append(lab)
        if index_first == 3: 
            if index_after == 3:
                for i in range(num):
                    img = PhotoImage(file="cpImage/" + card + ".png")
                    lab = Label(self.root, image=img)
                    lab.image = img
                    lab.place(x=self.pg_position[0][0], y=self.pg_position[0][1])
                    self.pg_position[0][0] += 37
                    self.pg_position[0][2].append(lab)    
            if index_after == 0:
                for i in range(num):
                    img = PhotoImage(file="cpImagel/"+card+".png")
                    lab = Label(self.root, image=img)
                    lab.image = img
                    lab.place(x=self.pg_position[1][0], y=self.pg_position[1][1])
                    self.pg_position[1][1] += 37
                    self.pg_position[1][2].append(lab)
            if index_after == 1:
                for i in range(num):
                    img = PhotoImage(file="cpImaged/"+card+".png")
                    lab = Label(self.root, image=img)
                    lab.image = img
                    lab.place(x=self.pg_position[2][0], y=self.pg_position[2][1])
                    self.pg_position[2][0] -= 37
                    self.pg_position[2][2].append(lab)
            if index_after == 2:
                for i in range(num):
                    img = PhotoImage(file="cpImager/"+card+".png")
                    lab = Label(self.root, image=img)
                    lab.image = img
                    lab.place(x=self.pg_position[3][0], y=self.pg_position[3][1])
                    self.pg_position[3][1] -= 37
                    self.pg_position[3][2].append(lab)



    def handler(self):
        while True:
            data1 = self.sockfd.recv(1024).decode()
            data = data1.split(' ')
            print(data)
            # 先摇一摇筛子
            if data[0] == 'SP':
                self.firstPlayer = data[3]
                self.seatPosition = data[4:]
                self.show_order(data[1], data[2], data[3])

            if data[0] == 'Fp':
                self.name = data[1]
                b = data[2:]
                self.ser_send = b
                self.img_url()
                self.but_max(self.name, self.firstPlayer)

            if data[0] == 'OB':
                self.get_one(data[2])
                self.checkHuPai(data[1], data[2], data[3])

            if data[0] == 'wait':
                self.table_plus()

            if data[0] == 'Pass':
                board = data[2]
                # print(board)
                prePlayer = data[3]
                # print(prePlayer)
                # 掉用显示一张牌
                url = "./cpImage/"+board+'.png'
                self.qipai.append(url)
                # print(self.qipai)
                self.createCenter()
                msg = 'Guo ' + prePlayer
                self.sockfd.send(msg.encode())
                # self.sockfd.send(b'Wait')

            if data[0] == 'Peng':
                playerPP = data[1]
                pengPai = data[2:]
                self.show_other_pg(playerPP, pengPai)

            if data[0] == 'CS':
                self.prePlayer = data[4]
                print(self.prePlayer)
                self.checkHuPai(data[1], data[2], data[3])

            if data[0] == 'Pre':
                self.playerPP = data[1]
                self.pengPai = data[2:]
                self.come = ''

            if data[0] == 'Lose':
                print(data)
                self.userwin = data[1]
                self.hu()
            if data[0]  == 'Empty':
                messagebox.showinfo('牌发完，是否开始下一句')
                sys.exit(0)

        

 #    #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #  
    def btn_restart(self):
        jg=messagebox.askyesno("YesNo","玩家是否重新开始！")
        return jg
    def hu(self):
        # print(self.ser_send)  # 删除打出的牌
        # 1.把自己的牌反过来
        # 2把所有玩家的牌返回来
        # 3,删除所有数组的值，如果开始下一局就重新加载所有所有程序
        self.huMy()
        mess="玩家"+self.userwin+"win!!!"
        msg = 'Win ' + self.userwin
        self.sockfd.send(msg.encode())
        jg = self.btn_restart()
        if not jg:
            sys.exit()#退出游戏，回收socket
        else:
            # 重新开始
            # 1,清除收列表中的东西，清除所有窗口中的对象，2，重新加载handle函数
            for x in self.total:
                x.destroy()
            for x in self.clearLaber:
                x.destroy()
            print(self.qipaiduixiang)
            for x in self.qipaiduixiang:
                x.destroy()
            # 游戏开始
            self.qipaiduixiang.clear()
            print(len(self.qipaiduixiang))
            self.img_start()
            print('重新开始－－－－－－－－－－－－－－－－－－－')

    def huMy(self):
        '''得到手牌数组，和位置'''
        self.url1.clear()  # 清空原图片对象

        # 1删除所有的牌的对象

        for x in range(len(self.obj_but2)):
            self.obj_but2[-1].destroy()
            a=self.obj_but2.pop()
            del self.obj_but[a]
        self.url1.clear()
        print(self.url1)
        # 2把牌都反过来
        arrayHU = []

        q_x=320
        q_y=500
        picc = [PhotoImage(file='./cpImage/' + i + '.png') for i in self.ser_send]
        for x in picc:
            b = Label(self.root, image=x, relief=FLAT)
            b.image = x
            self.qipaiduixiang.append(b)
        # self.qipaiduxiang.append(b)
            b.place(x=q_x, y=q_y)
            q_x+=37
        # for i in self.display[1]:# 删除碰、杠牌初始化
        #     i.destroy()
        self.display.clear()
        for i in self.pg_position:
            for j in i[2]:
                j.destroy()
        self.pg_position = [[300, 620, []], [180, 140, []], [850, 70, []], [970, 640, []]]

