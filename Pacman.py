from copy import deepcopy as cp
import numpy as np 
import random

class Pacman(object):
    def __init__(self, initposition):
        self.live = 1
        self.location = initposition

    def actions(self, maze):  #Action allowed in next step
        act = []
        posX = self.location[0]
        posY = self.location[1]

        if (maze.map[posX - 1][posY] != '=') & (maze.map[posX - 1][posY] != '|'):
            act.append("up")

        if (maze.map[posX + 1][posY] != '=') & (maze.map[posX + 1][posY] != '|'):
            act.append("down")

        if (maze.map[posX][posY - 1] != '|') & (maze.map[posX][posY - 1] != '='):
            act.append("left")

        if (maze.map[posX][posY + 1] != '|') & (maze.map[posX][posY + 1] != '='):
            act.append("right")
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
    
    def existGhostNearby(self, ghosts):
        for ghost in ghosts:
            distance = self.mahattanDistance(ghost)
            if distance < 3: return True
        return False 
    
    def runAway(self, maze, ghosts, actions):
        availableActions = Pacman.actions(self, maze)
        for ghost in ghosts:
            direction = self.getDirection(ghost) #The direction will not be chosen by pacman
            for d in direction:
                for a in availableActions:
                    if d == a: availableActions.remove(d)
        if (availableActions): Pacman.doAction(self, maze,np.random.choice(availableActions))
        else: Pacman.doAction(self, maze, Pacman.actions(self, maze))

    def gameOver(self, maze):
        return (self.live == 0) | (maze.remainingFood == 0)

    def IDS(self, maze, ghosts, nearestFood, actions, doAction, depthLimit):
        if Pacman.existGhostNearby(self, ghosts): return 'run'
        for food in nearestFood:
            if self.location == food.location: return []
        if depthLimit == 0: return 'cutoff'
        
        CutOff = False
        for act in Pacman.actions(self,maze):
            cpmaze = cp(maze)
            cpself = cp(self)
            doAction(cpself, cpmaze, act)
            res = Pacman.IDS(cpself,cpmaze, ghosts, nearestFood, actions, doAction, depthLimit - 1)

            if res is 'cutoff': CutOff = True 
            elif res is not 'fail': return act
        if CutOff: return 'cutoff'
        else: return 'fail'

    def pacmanMove(self, maze, ghosts, maxDepth = 4):
        nearestFood = Pacman.getNearestFood(self, maze)
        for food in nearestFood:
            if self.location == food.location: return []
        
        for depth in range(maxDepth):
            res = Pacman.IDS(self, maze, ghosts, nearestFood, Pacman.actions, Pacman.doAction, depth)
            if res != 'cutoff' and res != 'fail' and res != 'run': return Pacman.doAction(self, maze, res)
                
        if res == 'run': Pacman.runAway(self, maze, ghosts, Pacman.actions)
        else: Pacman.doAction(self, maze, Pacman.actions(self, maze))