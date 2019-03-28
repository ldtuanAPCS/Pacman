import Pacman as P
import Ghost as G
from Food import Food as F
from copy import deepcopy as cp

initialVisit = []

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

    def __str__(self):
        value = ''
        for i in range(self.height):
            for j in range(self.width): value += self.map[i][j]
            value += '\n'
        return value
    
    def removeFood(self, x, y):
        for f in self.food:
            if (f.location[0] == x and f.location[1] == y): self.food.remove(f)

    def move(self, target, x, y):
        posX = target.location[0]
        posY = target.location[1]
        if isinstance(target, P.Pacman):
            if self.map[x][y] is '.':
                self.remainingFood -= 1
                self.removeFood(x ,y)
                self.updateNewVisit()
            self.map[x][y] = 'P'
            self.map[posX][posY] = ' '
            target.location = x, y            
            self.visited[x][y] = True
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
            #self.visited[posX][posY] = False
            #self.visited[x][y] = True