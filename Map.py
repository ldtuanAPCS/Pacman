import Pacman as P
import Ghost as G
#import Food as F
from Food import Food as F
from copy import deepcopy as cp
'''
class Food(object):
    def __init__(self, x, y):
        self.location = x, y
    
    def location(self):
        return self.location

    def __repr__(self):
        st = "Food location: ", self.location[0], ", ", self.location[1] 
        return str(st)
'''
class Map(object):
    def __init__(self, startState):
        self.map = cp(startState)
        self.food = self.setFood(startState)
        self.ghostSpawn = self.findGhost(startState)
        self.pacmanSpawn = self.findPacman(startState)
        self.height = len(startState)
        self.length = len(startState[0])
        self.remainingFood = self.calculateRemainingFood(startState)
        return

    def __getitem__(self, item):
        x = item[0]
        y = item[1]
        return self.map[x][y]

    #1 ghsot only
    def findGhost(self, state):
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 'G': return i,j
        print('No ghost appeared')
        return None

    def findPacman(self, state):
#        PacmanPos = None
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 'P': return i, j

    def setFood(self, state):
        arr = []
        for x, i in enumerate(state):
            for y, j in enumerate(state[x]):
                if j is '.': arr.append(F(x,y))
        return arr

    def getFood(self):
        return self.food

    def __str__(self):
        value = ''
        for i in range(len(self.map)):
            for j in range(len(self.map[i])): value += self.map[i][j]
            value += '\n'
        return value

    def calculateRemainingFood(self, state):
        cnt = 0
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == '.': cnt += 1
        return cnt
    
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
                self.map[x][y]  = 'P'
                self.map[posX][posY] = ' '
                target.location = x, y
        else:  #GHOST
            if self.map[x][y] is '.':
                self.map[x][y] = 'G'
                if target.onFood:
                    self.map[posX][posY] = '.'
                    target.onFood = False
                else: self.map[posX][posY] = ' '
                target.onFood = False
                target.location = x, y
            else:
                self.map[x][y] = 'G'
                if target.onFood:
                    self.map[posX][posY] = '.'
                    target.onFood = False
                else: self.map[posX][posY] = ' '
                target.location = x, y