import sys
from collections import OrderedDict
import copy
import re

evalMatrix = [[99,-8,8,6,6,8,-8,99],[-8,-24,-4,-3,-3,-4,-24,-8],[8,-4,7,4,4,7,-4,8],[6,-3,4,0,0,4,-3,6],[6,-3,4,0,0,4,-3,6],[8,-4,7,4,4,7,-4,8],[-8,-24,-4,-3,-3,-4,-24,-8],[99,-8,8,6,6,8,-8,99]]
Totaldepth = 0
logOutput = ''
cnt = 0
playa = ''
class Node:
    '''state = []
    player = ''
    depth = ''
    parent = ''
    value = ''
    terminal = '''
    def __init__(self,currstate,player,depth,parent,value,position,terminal):
        self.state = copy.deepcopy(currstate)
        self.player = player
        self.depth = depth
        self.parent = parent
        self.value = value
        self.children = []
        self.position = position
        self.terminal = terminal
        #print self.position
        if self.depth % 2 == 0:
            self.value = float('-inf')
        else:
            self.value = float('inf')


    def convert_position(self,line):
        words = line.strip().split(' ')
        row = int(words[0])+1
        if (words[1]) == '0':
            col = 'a'
        elif (words[1] == '1'):
            col = 'b'
        elif (words[1] == '2'):
            col = 'c'
        elif (words[1] == '3'):
            col = 'd'
        elif (words[1] == '4'):
            col = 'e'
        elif (words[1] == '5'):
            col = 'f'
        elif (words[1] == '6'):
            col = 'g'
        elif (words[1] == '7'):
            col = 'h'
        return str(col+''+str(row))


    def generate_child(self,validmoves):
        global Totaldepth,cnt
        for line in validmoves:
            cnt = 0
            st = self.play(line,validmoves[line])
            position = self.convert_position(line)
            if self.depth+1 == Totaldepth:
                terminal = True
            else:
                terminal= False
            self.children.append(Node(st,self.return_opponent(self.player),(self.depth)+1,self,float('-inf'),position,terminal))
        if not validmoves:
            cnt+=1
            if cnt <=1:
                st = copy.deepcopy(self.state)
                self.children.append(Node(st, self.return_opponent(self.player), (self.depth) + 1, self,float('-inf'), 'pass',False))
            elif cnt == 2:
                st = copy.deepcopy(self.state)
                if self.depth+1 == Totaldepth:
                    self.children.append(Node(st, self.return_opponent(self.player), (self.depth) + 1, self, float('-inf'), 'pass', True))
                else:
                    self.children.append(Node(st, self.player, (self.depth) + 1, self, float('-inf'), 'pass', True))



    def play(self,start,end):
        st = copy.deepcopy(self.state)
        oldi,oldj=[int(x)for x in start.split(" ")]
        st[oldi][oldj] = self.player
        if not ',' in end:
            newi,newj = [int(x) for x in end.split(' ')]
            while newi != oldi or newj != oldj:
                st[newi][newj] = self.player
                if oldi < newi:
                    newi -= 1
                elif oldi > newi:
                    newi += 1

                if oldj < newj:
                    newj -= 1
                elif oldj > newj:
                    newj += 1
        else:
            line = end.strip().split(',')
            for points in line:
                newi, newj = [int(x) for x in points.split(' ')]
                while newi != oldi or newj != oldj:
                    st[newi][newj] = self.player
                    if oldi < newi:
                        newi -= 1
                    elif oldi > newi:
                        newi += 1

                    if oldj < newj:
                        newj -= 1
                    elif oldj > newj:
                        newj += 1

        return st


    def return_opponent(self,playa):
        if playa == 'X':
            opponent = 'O'
        else:
            opponent = 'X'
        return opponent

    def neighbours(self):
        neighbour = []
        opponent = self.return_opponent(self.player)
        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                if self.state[i][j] == opponent:
                    for x, y in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
                        x += i
                        y += j
                        if self.inBounds(x, y):
                            if self.state[x][y] == '*':
                                neighbour.append(str(x)+' '+str(y))
        return self.valid_moves(list(set((neighbour))))

    def valid_moves(self,neighbour):
        opponent = self.return_opponent(self.player)
        validmoves = {}
        for point in neighbour:
            x = int(point[0])
            y = int(point[2])
            for drow,dcol in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
                currentx = x + drow
                currenty = y + dcol
                if self.inBounds(currentx,currenty) and self.state[currentx][currenty] == opponent:
                    while self.inBounds(currentx,currenty) and self.state[currentx][currenty] == opponent:
                        currentx += drow
                        currenty += dcol
                    if(self.inBounds(currentx,currenty)) and self.state[currentx][currenty] == self.player:
                        if not validmoves.has_key(str(x)+' '+str(y)):
                            validmoves[str(x)+' '+str(y)] = str(currentx)+' '+str(currenty)
                        else:
                            validmoves[str(x) + ' ' + str(y)] += ','+str(currentx) + ' ' + str(currenty)
        validmoves = OrderedDict(sorted(validmoves.items(), key=lambda t: t[0]))
        return validmoves

    def inBounds(self,x,y):
        return x>=0 and x<=7 and y>=0 and y<=7

    def isTerminal(self):
        '''global Totaldepth
        return Totaldepth == self.depth'''
        return self.terminal

    def utiliy(self):
        global playa
        sumplayer =0
        sumopponent = 0
        for row in range(8):
            for col in range(8):
                if self.state[row][col] == playa:
                    sumplayer += evalMatrix[row][col]
                elif self.state[row][col] == self.return_opponent(playa):
                    sumopponent += evalMatrix[row][col]
        self.value = sumplayer - sumopponent




def importboard(path):
    global playa
    matrix = []
    with open(path,'r') as f:
        contents = f.read().strip().split('\n')
    playa = contents[0]
    depth = int(contents[1])
    for line in contents[2:]:
        row = []
        for i in range(len(line)):
            row.append(line[i])
        matrix.append(row)
    return Node(matrix,contents[0],0,None,float('-inf'),'root',False),depth



def MaxValue(node,alpha,beta):
    global logOutput
    if node.isTerminal():
        node.utiliy()
        logOutput+=str(node.position)+','+str(node.depth)+','+str(node.value)+','+str(alpha)+','+str(beta)+'\n'
        return node.value
    v = float('-inf')
    validmoves = node.neighbours()
    node.generate_child(validmoves)
    for child in node.children:
        logOutput +=str(node.position) + ',' + str(node.depth) + ',' + str(node.value) + ',' + str(alpha) + ',' + str(beta)+'\n'
        v = max(v,MinValue(child,alpha,beta))
        node.value = v
        if v>=beta:
            #node.value = v
            logOutput += str(node.position) + ',' + str(node.depth) + ',' + str(node.value) + ',' + str(alpha) + ',' + str(beta) + '\n'
            return v
        alpha = max(v,alpha)
    #node.value = v
    logOutput += str(node.position) + ',' + str(node.depth) + ',' + str(node.value) + ',' + str(alpha) + ',' + str(beta) + '\n'
    return v

def MinValue(node,alpha,beta):
    global logOutput
    if node.isTerminal():
        node.utiliy()
        logOutput += str(node.position) + ',' + str(node.depth) + ',' + str(node.value) + ',' + str(alpha) + ',' + str(beta) + '\n'
        return node.value
    v = float('inf')
    validmoves = node.neighbours()
    node.generate_child(validmoves)
    for child in node.children:
        logOutput += str(node.position) + ',' + str(node.depth) + ',' + str(node.value) + ',' + str(alpha) + ',' + str(beta) + '\n'
        v = min(v,MaxValue(child,alpha,beta))
        node.value = v
        if v<=alpha:
            #node.value = v
            logOutput += str(node.position) + ',' + str(node.depth) + ',' + str(node.value) + ',' + str(alpha) + ',' + str(beta) + '\n'
            return v
        beta = min(v,beta)
    #node.value = v
    logOutput += str(node.position) + ',' + str(node.depth) + ',' + str(node.value) + ',' + str(alpha) + ',' + str(beta) + '\n'
    return v


def printboard(matrix):
    finalMatrix = ''
    for i in range(8):
        for j in range(8):
            finalMatrix += str(matrix[i][j])
        finalMatrix += '\n'
    return finalMatrix


def main():
    global Totaldepth,logOutput
    root,Totaldepth = importboard('input.txt')
    logOutput+='Node,Depth,Value,Alpha,Beta\n'
    MaxValue(root,float('-inf'),float('inf'))
    for child in root.children:
        if root.value == child.value:
            finalMatrix = printboard(child.state)
            #print finalMatrix
            break

    logOutput = logOutput.rstrip()
    logOutput = re.sub(r'inf','Infinity',logOutput)
    finalMatrix += logOutput
    with open('output.txt','w+') as f:
        f.write(finalMatrix)


if __name__ == '__main__':
    main()