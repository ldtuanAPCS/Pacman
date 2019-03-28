from queue import PriorityQueue
from copy import deepcopy as cp
import numpy as np

class Pacman(object):
    def __init__(self, initposition):
        self.live = 1
        self.location = initposition
        self.onGhost = False

    def actions(self, maze, nearestFood):  #Action allowed in next step
        act = []
        q = PriorityQueue()
        posX = self.location[0]
        posY = self.location[1]

        if (maze.map[posX - 1][posY] != '=') and (maze.map[posX - 1][posY] != '|') and (maze.map[posX - 1][posY] != 'G') and (maze.visited[posX - 1][posY] == False):
            mini = 999999999
            cpSelf = cp(self)
            t = list(cpSelf.location)
            t[0] -= 1
            cpSelf.location = tuple(t)
            for food in nearestFood: mini = min(mini, cpSelf.mahattanDistance(food))
            q.put([mini, 'up'])

        if (maze.map[posX + 1][posY] != '=') and (maze.map[posX + 1][posY] != '|') and (maze.map[posX + 1][posY] != 'G') and (maze.visited[posX + 1][posY] == False):
            mini = 999999999
            cpSelf = cp(self)
            t = list(cpSelf.location)
            t[0] += 1
            cpSelf.location = tuple(t)
            for food in nearestFood: mini = min(mini, cpSelf.mahattanDistance(food))
            q.put([mini, 'down'])

        if (maze.map[posX][posY - 1] != '=') and (maze.map[posX][posY - 1] != '|') and (maze.map[posX][posY - 1] != 'G') and (maze.visited[posX][posY - 1] == False):
            mini = 999999999
            cpSelf = cp(self)
            t = list(cpSelf.location)
            t[1] -= 1
            cpSelf.location = tuple(t)
            for food in nearestFood: mini = min(mini, cpSelf.mahattanDistance(food))
            q.put([mini, 'left'])

        if (maze.map[posX][posY + 1] != '=') and (maze.map[posX][posY + 1] != '|') and (maze.map[posX][posY + 1] != 'G') and (maze.visited[posX][posY + 1] == False):
            mini = 999999999
            cpSelf = cp(self)
            t = list(cpSelf.location)
            t[1] += 1
            cpSelf.location = tuple(t)
            for food in nearestFood: mini = min(mini, cpSelf.mahattanDistance(food))
            q.put([mini, 'right'])
        while not q.empty(): act.append(q.get()[1])
        return act

    def doAction(self, maze, act):
        if act == 'up': maze.move(self, self.location[0]-1, self.location[1])
        elif act == 'down': maze.move(self, self.location[0]+1, self.location[1])
        elif act == 'left': maze.move(self, self.location[0], self.location[1]-1)
        else: maze.move(self, self.location[0], self.location[1]+1)

    def mahattanDistance(self, obj):
        dX = obj.location[1] - self.location[1]
        dY = obj.location[0] - self.location[0]
        return np.abs(dX) + np.abs(dY)

    def getNearestFood(self, maze):
        food = maze.food
        chosenFood = []
        mini = 9999999999  # +INF
        for f in food:
            x = self.mahattanDistance(f)
            if maze.level != 3:
                if x < mini :
                    chosenFood = [f]
                    mini = x
                elif x == mini:
                    chosenFood.append(f)
            else:
                if x < mini and x <= 3:
                    chosenFood = [f]
                    mini = x
                elif x == mini:
                    chosenFood.append(f)
        return chosenFood
    
    def getDirection(self, obj): #suitable direction
        direction = []
        dX = self.location[0] - obj.location[0]
        dY = self.location[1] - obj.location[1]
        if dX > 0: direction.append('up')
        if dX < 0: direction.append('down')
        if dY > 0: direction.append('left')
        if dY < 0: direction.append('right')
        return direction

    def gameOver(self, maze):
        return (self.live == 0) | (maze.remainingFood == 0)

    def IDS(self, maze, ghosts, nearestFood, depthLimit):
        for food in nearestFood:
            if self.location == food.location: return []
        if depthLimit == 0: 
            return 'cutoff'
        
        CutOff = False
        for act in Pacman.actions(self, maze, nearestFood):
            cpmaze = cp(maze)
            cpself = cp(self)
            Pacman.doAction(cpself, cpmaze, act)
            res = Pacman.IDS(cpself, cpmaze, ghosts, nearestFood, depthLimit - 1)
            if res is 'cutoff': CutOff = True 
            elif res is not 'fail': return act
        if CutOff: return 'cutoff'
        else: return 'fail'

    def pacmanMove(self, maze, ghosts, stop, maxDepth):
        nearestFood = Pacman.getNearestFood(self, maze)
        for food in nearestFood:
            if self.location == food.location: return []
        for depth in range(1, maxDepth+1):
            res = Pacman.IDS(self, maze, ghosts, nearestFood, depth)
            if res != 'cutoff' and res != 'fail' and res != 'run':
                Pacman.doAction(self, maze, res)
                return stop
        if res == 'cutoff' or res == 'fail': 
            stop = True
            self.live = 0
            #end the game 
        return stop