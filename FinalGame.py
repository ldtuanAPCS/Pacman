import time
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

def eachRun(num, ghosts, p, maze, score, dead, level, prevMove):
    numFood = maze.remainingFood
    if level == 4:
        for ghost in ghosts: ghost.ghostMove(maze, p.location)
    if level < 3: p.pacmanMove(level, maze, ghosts)
    else: p.pacmanMove(level, maze, ghosts, 1)

    for ghost in ghosts:
        if p.location == ghost.location: 
            dead = True
            p.live -= 1
    if score >= 1: score -= 1
    if numFood > maze.remainingFood: score += 10
    num += 1
    return num, ghosts, p, maze, score, dead

def beginGame(maze, p, level, score, ghosts):
    run, dead = 1, False
    print(ghosts)
    while not p.gameOver(maze):
        print("\nFood left: ", maze.remainingFood, "\t Score:  ", score)
        print(maze)
        #print('Actions available: ', p.actions(maze))
        run, ghosts, p, maze, score, dead = eachRun(run, ghosts, p, maze, score, dead, level, "")
        #time.sleep(0.3)
    print("\nFood left: ", maze.remainingFood, "\t Score:  ", score)
    print(maze)
    if dead: print("You died! Game over")
    else: print('Congratulations! You ate all the food. Your final score is: ',score)

if __name__ == "__main__":
    '''state = [['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '='],
             ['|', 'G', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],   
             ['|', ' ', ' ', ' ', ' ', 'G', ' ', ' ', ' ', ' ', '|'],
             ['|', ' ', ' ', ' ', ' ', '.', ' ', ' ', ' ', ' ', '|'],
             ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
             ['|', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'P', '|'],
             ['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=']]

    state = [['=', '=', '=', '=', '='],
             ['|', 'P', ' ', ' ', '|'],
             ['|', ' ', '.', 'G', '|'],
             ['=', '=', '=', '=', '=']]
           '''  
    state = [['=', '=', '=', '=', '='],
             ['|', 'P', '.', 'G', '|'],
             ['=', '=', '=', '=', '=']]
             
    maze = M.Map(state)
    p = P.Pacman(maze.pacmanSpawn)
    ghosts = [G.Ghost(maze.ghostSpawn)]
    score = 100
    level = 1
    print("You are given ",score,'points')
    beginGame(maze, p, level, score, ghosts)