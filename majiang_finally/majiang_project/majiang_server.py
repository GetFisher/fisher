from socket import *
import threading, sys, time
from majiang_sql import *
import random as R
from hupai import *
import chatroom_server



class Handler():
    def __init__(self, c, user):
        # connfd: 连接套接字
        self.connfd = c
        self.user = user
        # 创建数据库类的实例化对象
        self.userSql = Mysqlpython()
                
    def register(self):
        data = self.userSql.insert(self.user[1], self.user[2], self.user[3])
        # print(data)
        
        # 等待数据库返回信息
        if data == 'E':
            # print('userName重复')
            self.connfd.send(b'NE')
        else:
            # print('成功注册')
            self.connfd.send(b'OK')
    
    def loading(self):
        data = self.userSql.select(self.user[1], self.user[2])
        
        if data == ():
            self.connfd.send(b'E')
        else:
            self.connfd.send(b'OK')



def create_thread(sockfd):
    cmdList = []
    totalUserList = []
    while True:
        try:
            connfd, addr = sockfd.accept()
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue
        print('客户端登录:', addr)

        table = Table(connfd)
        request = Request(connfd, cmdList, table, totalUserList)
        # 创建线程
        t = threading.Thread(target = request.receive_cmd)
        t.setDaemon(True)
        t.start()



total_table = []
class Table(object):
    def __init__(self, connfd):
        self.connfd = connfd
        # self.userName = userName
        # self.userSql = Mysqlpython()
        # data = self.userSql.get_name(self.userName)
        # self.name = data[0]

    def __createTable(self):
        # 创建房间的次序列表
        tableList = []
        seat_list = []
        seat_list.append(self.name)
        seat_list.append(self.connfd)
        tableList.append(seat_list)
        # seat_list[self.name] = self.connfd

        global total_table
        total_table.append(tableList)
    
    def create_table(self, userName):
        self.userName = userName
        self.userSql = Mysqlpython()
        data = self.userSql.get_name(self.userName)
        self.name = data[0]
        t = threading.Thread(target = self.__createTable)
        t.setDaemon(True)
        t.start()

    def join_table(self, userName):
        self.userName = userName
        self.userSql = Mysqlpython()
        data = self.userSql.get_name(self.userName)
        self.name = data[0]
        n = 0
        if not total_table:
            self.create_table(userName)
        else:
            for i in total_table:
                if len(i) < 4:
                    tList = []
                    tList.append(self.name)
                    tList.append(self.connfd)
                    i.append(tList)
                    break
                else:
                    n += 1
            if len(total_table) == n:
                print(n)
                self.create_table(userName)
        

    def start_game(self):
        print('1')
        lst = []
        for i in total_table:
            for j in i:
                if self.name == j[0]:
                    print('2')
                    msg = self.select_player(i)
                    board_list = boardList()
                    i.append(board_list)
                    print(total_table)
                    for _ in i[0:4]:
                        msg = msg + ' ' + _[0]
                    for uList in i[0:4]:
                        uList[1].send(msg.encode())


    def select_player(self, user_list):
        print('3')
        # 两个骰子的点数
        dice1 = R.randrange(1, 7)
        dice2 = R.randrange(1, 7)
        # 确定哪个先摸牌和出牌
        n = (dice1 + dice2) % 4

        firstPlayer = user_list[n][0]
        print(firstPlayer)
        msg = 'SP ' + str(dice1) + ' ' + str(dice2) + ' ' + firstPlayer
        return msg

    def fapai(self):
        print('4')
        totalUserList = []
        for i in total_table:
            for j in i:
                if j[0] == self.name:
                    for k in range(4):
                        user = i[k]
                        msg = 'Fp ' + user[0]
                        lst = i[4][(k*13):((k+1)*13)]
                        user.extend(lst)
                        for _ in lst:
                            msg = msg + ' ' + _
                            i[4].remove(_)
                        print(msg)
                        user[1].send(msg.encode())


    def requestOneBoard(self, name):
        print('5')
        for i in total_table:
            for j in i:
                if j[0] == name:
                    if not i[4]:
                        for k in i[0:4]:
                            k[1].send(b'Empty')
                    else:
                        board = i[4][0]
                        print(board)
                        print(j[2:])
                        i[4].remove(board)
                        char = self.checkMopai(board, j[2:])
                        print('胡牌消息:',char)
                        j.append(board)
                        for k in i[0:4]:
                            if k[0] == name:
                                msg = 'OB ' + name + ' ' + board + ' ' + char
                                k[1].send(msg.encode())
                            else:
                                msg = 'wait ' + '15s'
                                k[1].send(msg.encode())
    
    def checkMopai(self, board, board_list):
        print('checkMopai')
        check = Hupai(board, board_list)
        result = check.check_moPai()
        print(result)
        return result

    def checkHupai(self, board, board_list):
        print('checkHupai')
        check = Hupai(board, board_list)
        result = check.check_hupai()
        print(result)
        return result

    def ChuPai(self, board):
        for i in total_table:
            for user in i:
                if self.name == user[0]:
                    for j in i[0:4]:
                        if j[0] == self.name:
                            print('已经出牌')
                            j.remove(board)
                            msg = 'YCP 15s'
                            j[1].send(msg.encode())
                        elif j[0] != self.name:
                            print('检测')
                            char = self.checkHupai(board, j[2:])
                            if char == 'HP':
                                msg = 'CS ' + j[0] + ' ' + board + ' ' + char + ' ' + self.name
                                j[1].send(msg.encode())
                            elif char == 'HPGP':
                                msg = 'CS ' + j[0] + ' ' + board + ' ' + char + ' ' + self.name
                                j[1].send(msg.encode()) 
                            elif char == 'HPPP':
                                msg = 'CS ' + j[0] + ' ' + board + ' ' + char + ' ' + self.name
                                j[1].send(msg.encode())
                            elif char == 'GP':
                                msg = 'CS ' + j[0] + ' ' + board + ' ' + char + ' ' + self.name
                                j[1].send(msg.encode())
                            elif char == 'PP':
                                msg = 'CS ' + j[0] + ' ' + board + ' ' + char + ' ' + self.name
                                j[1].send(msg.encode())
                            elif char == 'G':
                                msg = 'Pass ' + j[0] + ' ' + board + ' ' + self.name
                                j[1].send(msg.encode())

    
    def nextPosition(self, name):
        for i in total_table:
            for j in i:
                if j[0] == name:
                    lst = []
                    for _ in i:
                        lst.append(_[0])
                    index = lst.index(name)
                    print(name)
                    nextPlayer = lst[(index+1)%4]
                    print(nextPlayer)
                    self.requestOneBoard(nextPlayer)

    def chuli(self, lst):
        for i in total_table:
            for j in i:
                if j[0] == self.name:
                    for k in lst:
                        for _ in j:
                            if _ == k:
                                j.remove(k)
                    if len(lst) == 2:
                        for l in i[0:4]:
                            if l[0] == self.name:
                                msg = 'Pre ' + self.name
                                for m in lst:
                                    msg = msg + ' ' + m
                                l[1].send(msg.encode())
                            else:
                                msg = 'Peng ' + self.name
                                for m in lst:
                                    msg = msg + ' ' + m
                                l[1].send(msg.encode())      
                    else:
                        for i in total_table:
                            for j in i:
                                if j[0] == self.name:
                                    if not i[4]:
                                        for k in i[0:4]:
                                            k[1].send(b'Empty')
                                    else:
                                        board = i[4][0]
                                        i[4].remove(board)
                                        char = self.checkMopai(board, j[2:])
                                        j.append(board)
                                        for k in i[0:4]:
                                            if k[0] == self.name:
                                                msg = 'OB ' + self.name + ' ' + board + ' ' + char
                                                k[1].send(msg.encode())
                                            else:
                                                msg = 'Peng ' + self.name
                                                for m in lst:
                                                    msg = msg + ' ' + m
                                                k[1].send(msg.encode())
    def Win(self, winner):
        for i in total_table:
            for j in i:
                if j[0] == winner:
                    for k in i[0:4]:
                        if k[0] != winner:
                            msg = 'Lose ' + winner
                            k[1].send(msg.encode())



def boardList():
    #　牌堆剩余打牌
    board_list = []
    for i in range(4):
        for j in range(11, 20):
            board_list.append(str(j))
        for j in range(21, 30):
            board_list.append(str(j))
        for j in range(31, 40):
            board_list.append(str(j))
        for j in range(41, 44):
            board_list.append(str(j))
    R.shuffle(board_list)
    return board_list




class Request():
    def __init__(self, connfd, cmdList, table, totalUserList):
        self.connfd = connfd
        self.cmdList = cmdList
        self.table = table
        self.totalUserList = totalUserList

    def receive_cmd(self): 
        while True:
            data = self.connfd.recv(1024).decode()
            user = data.split(' ')
            handle = Handler(self.connfd, user)
            print(data)
            # table = Table(self.connfd, user[1])
            
            if user[0] == 'Z':
                handle.register()

            elif user[0] == 'D':
                handle.loading()

            elif user[0] == 'CT':
                self.table.create_table(user[1])

            elif user[0] == 'JT':
                self.table.join_table(user[1])
            
            elif user[0] == 'P':
                #　牌堆剩余打牌
                self.cmdList.append(user[0])
                print(self.cmdList)
                if len(self.cmdList) == 4:
                    self.cmdList.clear()
                    self.table.start_game()
                
            elif user[0] == 'FP':
                self.cmdList.append(user[0])
                print(self.cmdList)
                if len(self.cmdList) == 4:
                    self.cmdList.clear()
                    self.table.fapai()

            elif user[0] == 'OK':
                print('a')
                self.cmdList.append(user[0])
                print(self.cmdList)
                if len(self.cmdList) == 4:
                    self.cmdList.clear()
                    self.table.requestOneBoard(user[2])

            elif user[0] == 'Wait':
                pass

            elif user[0] == 'CP':
                print('c')
                self.table.ChuPai(user[1])

            elif user[0] == 'Guo':
                print('e')
                self.cmdList.append(user[0])
                print(self.cmdList)
                if len(self.cmdList) == 3:
                    self.cmdList.clear()
                    self.table.nextPosition(user[1])
            
            elif user[0] == 'M':
                self.cmdList.clear()
                self.table.chuli(user[1:])

            elif user[0] == 'Win':
                print(user)
                self.table.Win(user[1])




def main():
    # 创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 5297))
    s.listen(10)

    t = threading.Thread(target = chatroom_server.startChatroomServer)
    t.setDaemon(True)
    t.start()

    # 创建连接和线程
    create_thread(s)

if __name__ == "__main__":
    main()