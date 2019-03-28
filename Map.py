import Pacman as P
import Ghost as G
from Food import Food as F
from copy import deepcopy as cp
import turtle

#Set up screen & pen
wn=turtle.Screen()
wn.bgcolor("black")
wn.title("Pacman")
wn.setup(700,700)
wn.tracer(0)
s = turtle.Screen()
s.register_shape('ghost.gif')
s.register_shape('fruit.gif')
s.register_shape('pacman.gif')

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)

initialVisit = []
pen=Pen()

class Map(object):
    def __init__(self, path):
        f = open(path, 'r')
        a,x,y = f.readline().split()
        self.level = int(a)
        self.height = int(x)
        self.width = int(y)
        self.food = []
        self.map = []
        self.score = 0
        self.ghostSpawn = None
        self.pacmanSpawn = None
        self.remainingFood = 0
        self.visited = [[True for i in range(self.width)] for j in range(self.height)]
        x = 0
        for i in f:
            i = i[:-1]
            y = 0
            tmp = []
            for j in i:
                if j == ' ': self.visited[x][y] = False
                elif j == 'G': self.ghostSpawn = x,y   
                elif j == 'P': self.pacmanSpawn = x,y
                elif j == '.':
                    self.food.append(F(x,y))
                    self.visited[x][y] = False
                    self.remainingFood += 1
                tmp.append(j)
                y += 1
            self.map.append(tmp)
            x+=1
        f.close()
        global initialVisit
        initialVisit = cp(self.visited)

    def updateNewVisit(self):
        self.visited = [[True for i in range(self.width)] for j in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j] == ' ' or self.map[i][j] == '.': self.visited[i][j] = False

    def __getitem__(self, item):
        x = item[0]
        y = item[1]
        return self.map[x][y]

    def printMaze(self, f):
        for i in range(self.height):
            for j in range(self.width):
                char = self.map[i][j]
                f.write(char)
                screen_y=288-(i*21)
                screen_x=-288+(j*21)
                pen.goto(screen_x,screen_y)
                if(char=='|' or char=='='):
                    pen.shape("square")
                    pen.color("white")
                elif(char=='P'):
                    pen.shape('pacman.gif')
                    pen.stamp()
                elif(char=='G'):
                    pen.shape("ghost.gif")
                    pen.stamp()
                elif(char=='.'):
                    pen.shape("fruit.gif")
                    pen.stamp()
                else:
                    pen.shape('square')
                    pen.color('black')
                pen.stamp()
            f.write('\n')
        wn.update()

    def removeFood(self, x, y):
        for f in self.food:
            if (f.location[0] == x and f.location[1] == y): self.food.remove(f)

    def move(self, target, x, y):
        posX = target.location[0]
        posY = target.location[1]
        if isinstance(target, P.Pacman):
            flag = False
            if self.map[x][y] is '.':
                flag =True
                self.remainingFood -= 1
                self.removeFood(x ,y)
            self.map[x][y] = 'P'
            if target.onGhost:
                self.map[posX][posY] = 'G'
                target.onGhost = False
            else: self.map[posX][posY] = ' '
            target.location = x, y            
            if flag: self.updateNewVisit()
            else: self.visited[x][y] = True
        else:  #GHOST
            if self.map[x][y] is '.':
                if target.onFood: self.map[posX][posY] = '.'
                else: self.map[posX][posY] = ' '
                target.onFood = True
            else:
                if target.onFood:
                    self.map[posX][posY] = '.'
                    target.onFood = False
                else: self.map[posX][posY] = ' '
            self.map[x][y] = 'G'    
            target.location = x, y