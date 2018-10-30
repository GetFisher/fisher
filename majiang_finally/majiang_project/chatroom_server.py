from socket import *

class Server_chat():
    '''
    麻将游戏中期项目
    聊天功能服务器
    '''
    flag = False #记录是否第一次进入房间
    def __init__(self, s, lst):
        self.s = s
        self.lst = lst

    #循环接受客户端消息并处理
    def receiveMessage(self):
        while True:
            data, addr = self.s.recvfrom(1024)
            data_list = data.decode().split(' ')
            if data_list[0] == 'C':
                self.flag = True
                msg = "%s 进入到房间\n"%data_list[1]
                self.send_to(msg, addr)
                self.lst.append(addr)
            elif data_list[0] == 'S':
                msg = '%s:%s'%(data_list[1],' '.join(data_list[2:]))
                self.send_to(msg, addr)
            elif data_list[0] == 'Q':
                msg = '%s 退出房间'%data_list[1]
                self.send_to(msg)
                self.do_quit(addr)

    #消息发送给客户端
    def send_to(self, msg, addr):
        #第一次进入房间运行
        if self.flag == True:
            joinmsg = "您已加入该房间\n"
            self.s.sendto(joinmsg.encode(), addr)
            self.flag = False
        #发送消息给房间里除了自己以外的用户
        for i in self.lst:
            if i == addr:
                continue
            else:
                self.s.sendto(msg.encode(), i)

    #客户端退出删除用户列表对应用户地址
    def do_quit(self,addr):
        user.remove(addr)

#启动聊天服务端
def startChatroomServer():
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(('0.0.0.0', 8888))
    #存储用户信息
    user = []
    sc = Server_chat(s,user)
    sc.receiveMessage()
    s.close()