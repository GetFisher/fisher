from socket import *
import tkinter as tk
from tkinter import messagebox
import play



class PrepareWindow():
    def __init__(self, s, name):

        # 套接字
        self.sockfd = s
        self.userName = name

        self.window = tk.Tk()
        self.window.title('麻将')
        self.window.geometry('1200x800')
        # 隐藏放大功能
        self.window.resizable(0, 0)

        # 创建背景图片
        self.label_img_png = tk.PhotoImage(file="./bgimg/youxibeijing.png")
        self.label_img = tk.Label(self.window, image=self.label_img_png)
        self.label_img.pack()

        # 创建图片按钮
        self.label_img_png1 = tk.PhotoImage(file="./bgimg/createroom.png")
        self.label_img1 = tk.Label(self.window, image=self.label_img_png1, bd=0)
        self.label_img1.bind('<1>', self.create_table)
        self.label_img1.place(x=600, y=294)
        # 创建图片按钮
        self.label_img_png2 = tk.PhotoImage(file="./bgimg/joinroom.png")
        self.label_img2 = tk.Label(self.window, image=self.label_img_png2, bd=0)
        self.label_img2.bind('<1>', self.join_table)
        self.label_img2.place(x=600, y=527)

        self.label_img_png3 = tk.PhotoImage(file="./bgimg/helpbtn.png")
        self.label_img3 = tk.Label(self.window, image=self.label_img_png3, bd=0)
        self.label_img3.bind('<1>', self.show_help_label)
        self.label_img3.place(x=1112, y=722)

        # 创建帮助标签和关闭按钮并隐藏
        self.__create_help_label()
        self.__create_close_button()
        self.__hide_element()

        self.window.mainloop()

    # 创建帮助标签
    def __create_help_label(self):
        self.label_help_img = tk.PhotoImage(file="./bgimg/image3.png")
        self.text = "碰牌：如果手中有两张或者三张，有人出和此一样的牌，不论哪个座位都可以碰牌，\n\
                        口中要叫一声“碰”，以提示其他人自己需要碰牌（行牌就要中断）。\n\
                        如果是碰四张牌，还可以在牌尾去摸一张牌（这叫杠牌）。\n下一位就从碰牌者继续摸牌、出牌。\n\
                        理牌：摸好牌后之后，需要理牌、审牌：分类整理手中的牌，整齐排列，审视牌势。补花：如手\n中有花牌，可以补花，即从牌墙的尾端取一张牌。若补回来的还是花牌，则\n可以再补。最后，不要忘了出牌。无论什么缘故，多牌还是少牌，那么这位玩\n家就没有再赢牌的机会了，俗称“做相公”，只能继续陪其他三家玩。\n \
                        听牌：当手中的十三张牌都凑成了有用的牌，只需再加上第十四张便可和牌，此状态称为听牌的\n阶段。如果三组牌经过吃牌、碰牌都已经亮相了，那么还剩最后一张牌。\n如果赢牌，积分就会翻一番。\n赢牌：赢牌的一般标准是，三个组合（三张一样，或者三张顺子），\n再加上两张一样（俗称将牌）的对牌，即为赢牌。"
        self.label_help = tk.Label(self.window, image=self.label_help_img, text=self.text, compound='center', bd=0)
        self.label_help.place(x=300, y=200)

    def __create_close_button(self):
        self.button_img_png = tk.PhotoImage(file="./bgimg/d12.png")
        self.button_img = tk.Button(self.window, image=self.button_img_png, command=self.hide_help_label)
        self.button_img.place(x=872, y=200)

    # 隐藏元素
    def __hide_element(self):
        self.label_help.place_forget()
        self.button_img.place_forget()

    # 显示帮助标签
    def show_help_label(self, event):
        self.flag = True
        if self.flag == True:
            self.__create_help_label()
            self.__create_close_button()

    # 隐藏帮助标签
    def hide_help_label(self):
        self.flag = False
        if self.flag == False:
            self.__hide_element()

    def create_table(self, event):
        self.window.destroy()
        msg = 'CT ' + self.userName
        self.sockfd.send(msg.encode())
        play.Mj(self.userName, self.sockfd)

    def join_table(self, event):
        self.window.destroy()
        msg = 'JT ' + self.userName
        self.sockfd.send(msg.encode())
        play.Mj(self.userName, self.sockfd)


class Login_Register():
    def __init__(self, s):
        self.sockfd = s
        self.window = tk.Tk()
        self.window.title('登录')
        self.window.geometry('450x300')
        self.window.resizable(0, 0)
        # 创建画布
        canvas = tk.Canvas(self.window, height=200, width=500)
        image_file = tk.PhotoImage(file='./bgimg/welcome.gif')
        image = canvas.create_image(0,0, anchor='nw', 
                image=image_file)#将图片置于画布上
        canvas.pack(side='top')#放置画布（为上端）

        tk.Label(self.window, text='帐号: ').place(x=100, y= 150)
        tk.Label(self.window, text='密码: ').place(x=100, y= 190)

        # 创建一个`entry`，显示为变量`uerName`,即用户名
        self.uerName = tk.StringVar()
        entry_usr_name = tk.Entry(self.window, textvariable=self.uerName)
        entry_usr_name.place(x=160, y=150)
        self.userPwd = tk.StringVar()
        entry_usr_pwd = tk.Entry(self.window, textvariable=self.userPwd, show='*')
        entry_usr_pwd.place(x=160, y=190)

        # 定义登录,注册`button`按钮
        btn_login = tk.Button(self.window, text='登录', command=self.loading)
        btn_login.place(x=160, y=230)
        btn_sign_up = tk.Button(self.window, text='注册', command = self.registerWindow)
        btn_sign_up.place(x=255, y=230)

        self.window.mainloop()

    def registerWindow(self):
        self.window.destroy()
        self.root = tk.Tk()
        self.root.title('登录')
        self.root.geometry('450x300')
        self.root.resizable(0, 0)

        img1 = tk.PhotoImage(file='./bgimg/zhucebeijing.png')
        img2 = tk.PhotoImage(file='./bgimg/tijiao.png')
        img3 = tk.PhotoImage(file='./bgimg/denglu.png')

        self.lab1 = tk.Label(self.root, image=img1)
        self.lab1.pack()
        
        self.uname = tk.StringVar()
        entry_usr_name = tk.Entry(self.root, textvariable=self.uname)
        entry_usr_name.place(x=200, y=57)
        
        self.upwd = tk.StringVar()
        entry_usr_pwd = tk.Entry(self.root, textvariable=self.upwd, show='*')
        entry_usr_pwd.place(x=200, y=95)

        self.cpwd = tk.StringVar()
        entry_usr_name = tk.Entry(self.root, textvariable=self.cpwd, show='*')
        entry_usr_name.place(x=200, y=133)
        
        self.user_name = tk.StringVar()
        entry_usr_pwd = tk.Entry(self.root, textvariable=self.user_name)
        entry_usr_pwd.place(x=200, y=170)
        
        btn_login = tk.Button(self.root, image = img2, command=self.register)
        btn_login.place(x=200, y=230)
        
        btn_sign_up = tk.Button(self.root, image = img3, command=self.quit)
        btn_sign_up.place(x=285, y=230)
        self.root.mainloop()

    def quit(self):
        self.root.destroy()
        Login_Register(self.sockfd)
    
    def loading(self):
        print(self.uerName.get(), self.userPwd.get())
        if (' ' in self.uerName.get()) or (' ' in self.userPwd.get()):
            messagebox.showerror(message = '用户名或密码中不允许有空格！')
        if not self.uerName.get() or not self.userPwd.get():
            messagebox.showerror(message = '用户名或密码不能为空！')
        elif 0 < len(self.uerName.get()) <= 8 and 5 < len(self.userPwd.get()) <= 12:
            msg = 'D ' + self.uerName.get() + ' ' + self.userPwd.get()
            self.sockfd.send(msg.encode())

            # 等待服务端确认
            data = self.sockfd.recv(1024).decode()
            if data == 'OK':
                messagebox.showinfo(message = '登录成功！')
                self.window.destroy()
                pw = PrepareWindow(self.sockfd, self.uerName.get())
            elif data == 'E':
                messagebox.showerror(message = '用户名或密码错误！')
        else:
            messagebox.showerror(message = '用户名或密码格式错误！')

    def register(self):
        print(self.uname.get(), self.upwd.get(), self.cpwd.get(), self.user_name.get())
        if (' ' in self.uname.get()) or (' ' in self.upwd.get()):
            messagebox.showerror(message = '用户名或密码中不允许有空格！')
        if not self.uname.get() or not self.upwd.get():
            messagebox.showerror(message = '用户名或密码不能为空！')
        if self.upwd.get() != self.cpwd.get():
            messagebox.showerror(message = '密码不一致!')
        elif 0 < len(self.uname.get()) <= 8 and 5 < len(self.upwd.get()) <= 12:
            msg = 'Z ' + self.uname.get() + ' ' + self.upwd.get() + ' ' + self.user_name.get()
            self.sockfd.send(msg.encode())

            # 等待服务端确认
            data = self.sockfd.recv(1024).decode()
            if data == 'OK':
                messagebox.showinfo(message = '注册成功！')
            elif data == 'NE':
                messagebox.showerror(message = '该用户名或昵称已被注册！')
        else:
            messagebox.showerror(message = '用户名或密码格式错误！')


def main(): 
    # 创建连接(和服务端进行交互)
    HOST = '176.215.140.119'
    PORT = 5297
    ADDR = (HOST, PORT)
    s = socket()
    s.connect(ADDR)

    Login_Register(s)


if __name__ == "__main__":
    main()