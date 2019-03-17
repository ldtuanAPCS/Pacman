import copy as cp 
from random import randint

class Ghost(object):
    def __init__(self, initposition):
        self.onFood = False
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

    def doAction(self, maze, action):
        if action == 'up': maze.move(self, self.location[0]-1, self.location[1])
        elif action == 'down': maze.move(self, self.location[0]+1, self.location[1])
        elif action == 'left': maze.move(self, self.location[0], self.location[1]-1)
        else: maze.move(self, self.location[0], self.location[1]+1)
        
    def randomAction(self, maze):
        actionSet = Ghost.actions(self, maze)
        act = actionSet[randint(0, len(self.actions(maze))-1)]
        return self.doAction(maze, act)

        