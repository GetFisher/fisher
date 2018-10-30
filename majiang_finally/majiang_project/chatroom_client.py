from socket import *
from threading import *
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import sys

class WindowUI():
    def __init__(self, name):
        '''
        麻将游戏中期项目
        聊天功能客户端及界面
        '''
        HOST = '176.215.140.119'
        PORT = 8888
        self.ADDR = (HOST, PORT)
        #记录是否第一次进入房间
        self.flag = False
        # 绑定用户名称
        self.name = name
        self.window = Tk()
        self.window.title('聊天')
        self.window.geometry('350x300')
        # 隐藏放大功能
        self.window.resizable(0, 0)
        # 创建文本框和滑块
        self.t = ScrolledText(self.window, height=18, width=47)
        self.t.pack(side='top')
        # 创建变量来动态绑定输入框的值
        self.message = StringVar()
        # 创建输入框
        self.e = Entry(self.window, width=38, textvariable=self.message)
        # self.e.bind('<KeyPress-Return>', self.__printkey)  # 绑定回车
        self.e.place(x=20, y=265)
        # 创建发送按钮
        self.b = Button(self.window, text='发送', width=1, height=1, command=self.sendMessage)
        self.b.place(x=300, y=260)
        self.create_new_thread()
        self.window.mainloop()

    # 发送绑定回车
    # def __printkey(self, event):
    #     if event.keysym == 'Return':
    #         self.sendMessage()

    # 新线程循环所有接受消息
    def receiveMessage(self):
        self.sockfd = socket(AF_INET, SOCK_DGRAM)
        self.sockfd.connect(self.ADDR)
        self.sendMessage()
        while True:
            data, addr = self.sockfd.recvfrom(1024)
            self.t.config(state=NORMAL)
            msg = data.decode()
            self.t.insert(END, msg)
            self.t.see(END)
            self.t.config(state=DISABLED)

    #发送消息
    def sendMessage(self):
        if self.flag == False:
            self.sockfd.sendto(('C ' + self.name).encode(), self.ADDR)
            print(self.flag)
            self.flag = True
            print(self.flag)

        else:
            msg = self.e.get()
            if not msg:
                return
            msg += '\n'
            self.t.config(state=NORMAL)
            self.t.insert(END, '你说:' + msg)
            self.t.see(END)
            #清空输入框内容
            self.e.delete(0,END)
            self.t.config(state=DISABLED)
            lastmsg = 'S %s %s' % (self.name, msg)
            self.sockfd.sendto(lastmsg.encode(), self.ADDR)

    # 退出房间
    def quit(self):
        s.sendto(('Q ' + self.name).encode(), self.ADDR)
        s.close()
        sys.exit(0)

    # 创建新线程
    def create_new_thread(self):
        th = Thread(target=self.receiveMessage)
        th.setDaemon(True)
        th.start()

#启动聊天客户端
def startChatroomClient(name):
    print('1')
    w = WindowUI(name)

