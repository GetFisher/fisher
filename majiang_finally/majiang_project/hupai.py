class Hupai(object):
    def __init__(self, board, userBoardList):
        '''
        board: 用户出的牌
        userBoardList: 用户手牌
        '''
        self.board = board
        self.userBoardList = userBoardList
        self.totalBoardList = [int(self.board)]
        for i in self.userBoardList:
            self.totalBoardList.append(int(i))
        self.totalBoardList.sort()
        self.cpBoardList = self.totalBoardList[:]
        self.mutiBoardList = []


    def check_hupai(self):
        # 查看玩家手牌是否有这张牌
        countBoard = self.userBoardList.count(self.board)
        
        result = self.checkSuccess()
        print(result)
        
        if countBoard == 0:
            if result == 0:
                return 'G'
            elif result == 1:
                return 'HP'

        elif countBoard == 1:
            if result == 0:
                return 'G'
            elif result == 1:
                return 'HP'

        elif countBoard == 2:
            if result == 0:
                return 'PP'
            elif result == 1:
                return 'HPPP'

        elif countBoard == 3:
            if result == 0:
                return 'GP'
            elif result == 1:
                return 'HPGP'

    def check_moPai(self):
        # 查看玩家手牌是否有这张牌
        countBoard = self.userBoardList.count(self.board)
        
        result = self.checkSuccess()
        print(result)

        for i in self.userBoardList:
            if self.userBoardList.count(i) == 4:
                msg = 'GP'
                if result == 0:
                    return 'GP'
                elif result == 1:
                    return 'HPGP'
        
        if countBoard == 0:
            if result == 0:
                return 'G'
            elif result == 1:
                return 'HP'

        elif countBoard == 1:
            if result == 0:
                return 'G'
            elif result == 1:
                return 'HP'

        elif countBoard == 2:
            if result == 0:
                return 'G'
            elif result == 1:
                return 'HP'

        elif countBoard == 3:
            if result == 0:
                return 'GP'
            elif result == 1:
                return 'HPGP'


    def checkSuccess(self):
        for i in self.totalBoardList:
            if self.totalBoardList.count(i) > 1 and i not in self.mutiBoardList:
                    self.mutiBoardList.append(i)               
        
        n = 0
        for j in self.mutiBoardList:# 遍历将牌所有情况，分别进行如下判断
            if self.cpBoardList == []:# 胡牌跳出条件
                return 1 # 判定胡牌
            self.step1(self.cpBoardList,j)
        if self.cpBoardList == []:# 判定胡牌防止漏判
            return 1
        else:
            return 0
    
    def step1(self,l,j):
        l = self.totalBoardList.copy() 
        l.remove(j)
        l.remove(j)
        # print('step1====',j,'移除i后的列表是',l)
        return self.step2(l)


    def step2(self,l):
        # print('step2,检查剩余牌数')
        if len(l) == 0:
            # print('可以胡牌')
            self.cpBoardList.clear()# 胡牌判定条件lc列表为空跳出判定
            return
        else:
            # print('余数不少，下一步')
            return self.step3(l)

    def step3(self,l):
        # print('step3，检查前三张牌')
        if l.count(l[0]) == 3:
            # print('前三张相同,进入第四步')
            return self.step4(l)
        else:
            # print('前三张不相同,进入step5')
            return self.step5(l)

    def step4(self,l):
        # print('step4')
        l=l[3:]
        # print('第四步后l为',l)
        return self.step2(l)
        

    def step5(self,l):
        # print('step5，l现在是',l)
        if (l[0]+1) in l and (l[0]+2) in l:
            l.remove(l[0]+2)
            l.remove(l[0]+1)
            l.remove(l[0])
            # print('前三张为顺子step5====',l)
            return self.step2(l)
        else:
            # print('第一张牌的顺子不在')
            return

