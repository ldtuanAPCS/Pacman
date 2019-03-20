from queue import PriorityQueue
from copy import deepcopy as cp
import numpy as np 
import random

class Pacman(object):
    def __init__(self, initposition):
        self.live = 1
        self.location = initposition

    def actions(self, maze, nearestFood, prevMove = ""):  #Action allowed in next step
        print('Pacman is in position:  ', self.location)
        print("Print again the map: ")
        for food in nearestFood: print(food.location)
        print(maze)
        act = []
        q = PriorityQueue()
        posX = self.location[0]
        posY = self.location[1]

        if (maze.map[posX - 1][posY] != '=') and (maze.map[posX - 1][posY] != '|') and (maze.map[posX - 1][posY] != 'G') and (prevMove != "down"):
            mini = 999999999
            cpSelf = cp(self)
            t = list(cpSelf.location)
            t[0] -= 1
            cpSelf.location = tuple(t)
            for food in nearestFood: mini = min(mini, cpSelf.mahattanDistance(food))
            q.put([mini, 'up'])

        if (maze.map[posX + 1][posY] != '=') and (maze.map[posX + 1][posY] != '|') and (maze.map[posX + 1][posY] != 'G') and (prevMove != "up"):
            mini = 999999999
            cpSelf = cp(self)
            t = list(cpSelf.location)
            t[0] += 1
            cpSelf.location = tuple(t)
            for food in nearestFood: mini = min(mini, cpSelf.mahattanDistance(food))
            q.put([mini, 'down'])

        if (maze.map[posX][posY - 1] != '=') and (maze.map[posX][posY - 1] != '|') and (maze.map[posX][posY - 1] != 'G') and (prevMove != "right"):
            mini = 999999999
            cpSelf = cp(self)
            t = list(cpSelf.location)
            t[1] -= 1
            cpSelf.location = tuple(t)
            for food in nearestFood: mini = min(mini, cpSelf.mahattanDistance(food))
            q.put([mini, 'left'])

        if (maze.map[posX][posY + 1] != '=') and (maze.map[posX][posY + 1] != '|') and (maze.map[posX][posY + 1] != 'G') and (prevMove != "left"):
            mini = 999999999
            cpSelf = cp(self)
            t = list(cpSelf.location)
            t[1] += 1
            cpSelf.location = tuple(t)
            for food in nearestFood: mini = min(mini, cpSelf.mahattanDistance(food))
            q.put([mini, 'right'])
        print('food distance: ',q.queue)
        while not q.empty(): act.append(q.get()[1])
        return act

    def runAway(self, maze, ghosts, nearestFood):
        availableActions = Pacman.actions(self, maze, nearestFood, "")
        for ghost in ghosts:
            direction = self.getDirection(ghost) #The direction will not be chosen by pacman
            for d in direction:
                for a in availableActions:
                    if d == a: availableActions.remove(d)
        if (availableActions): Pacman.doAction(self, maze,np.random.choice(availableActions))
        else: Pacman.doAction(self, maze, Pacman.actions(self, maze, nearestFood, ""))   #suppose to be end game here_need more work

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
        food = maze.getFood()
        chosenFood = []
        mini = 9999999999  # +INF
        for f in food:
            x = self.mahattanDistance(f)
            if x < mini:
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
    
    def existGhostNearby(self, level, ghosts):
        if level < 4: return False
        for ghost in ghosts:
            distance = self.mahattanDistance(ghost)
            if distance < 2:
                print('distance:  ', distance)
                return True
        return False 

    def gameOver(self, maze):
        return (self.live == 0) | (maze.remainingFood == 0)

    def IDS(self, level, maze, ghosts, nearestFood, depthLimit, prevMove):
        if Pacman.existGhostNearby(self, level, ghosts): return 'run'
        for food in nearestFood:
            if self.location == food.location: return []
        if depthLimit == 0: 
            print('depth limit =0 --> return back')
            return 'cutoff'
        
        CutOff = False
        z = Pacman.actions(self, maze, nearestFood, prevMove)
        for act in z:
            cpmaze = cp(maze)
            cpself = cp(self)
            print('In IDS, depth ', depthLimit,' have actions: ',z)            
            if act == 'left': print('go left')
            if act == 'right': print('go right')
            if act == 'up': print('go up')
            if act == 'down': print('go down')
            Pacman.doAction(cpself, cpmaze, act)
            res = Pacman.IDS(cpself, level, cpmaze, ghosts, nearestFood, depthLimit - 1, act)
            print('result in depth limit: ',depthLimit,' action: ', act,' is: ',res)
            if res is 'cutoff': CutOff = True 
            elif res is not 'fail': return act
        print('return back')
        if CutOff: return 'cutoff'
        else: return 'fail'

    def pacmanMove(self, level, maze, ghosts, maxDepth = 4):
        nearestFood = Pacman.getNearestFood(self, maze)
        for food in nearestFood:
            if self.location == food.location: return []
        
        #for depth in range(maxDepth):
        #print('depth: ',depth)
        res = Pacman.IDS(self, level, maze, ghosts, nearestFood, 10, "")
        print('RESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS:  ',res)
        if res != 'cutoff' and res != 'fail' and res != 'run': return Pacman.doAction(self, maze, res)
                
        if res == 'run': Pacman.runAway(self, maze, ghosts, nearestFood)