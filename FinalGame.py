from copy import deepcopy as cp
import Pacman as P
import Ghost as G
import Food as F
import Map as M

def getFood(state):
    food = []
    for x, i in enumerate(state):
        for y, j in enumerate(state[x]):
            if j is '.': food.append(F.Food(x,y))
    return food



if __name__ == "__main__":
    state = [['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '='],
             ['|', ' ', ' ', ' ', ' ', 'G', ' ', ' ', ' ', ' ', '|'],
             ['|', ' ', '=', '=', '=', ' ', '=', '=', '=', ' ', '|'],
             ['|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|'],
             ['|', ' ', '=', '=', '=', ' ', '=', '=', '=', ' ', '|'],
             ['|', '.', '.', '.', '.', '.', '.', '.', '.', 'P', '|'],
             ['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=']]

    maze = M.Map(state)
    p = P.Pacman(maze.pacmanSpawn)
    ghost = [G.Ghost(maze.ghostSpawn)]
    score = 100
    print(score)
