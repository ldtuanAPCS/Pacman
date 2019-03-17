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

def eachRun(num, ghosts, p, maze, score, dead, level):
    numFood = maze.remainingFood
    if level == 4:
        for ghost in ghosts: state = ghost.ghost_move(maze, p.location)
    if level < 3: state = p.pacmanMove(maze, ghosts)
    else: p.pacmanMove(maze, ghosts, 1)

    for ghost in ghosts:
        if p.location == ghost.location: 
            dead = True
            p.live -= 1
    if score >= 1: score -= 1
    if numFood > maze.remainingFood: score += 10
    num += 1
    return num, ghosts, p, maze, score, dead

def beginGame(maze, p, level):
    score, run, dead, ghosts = 0, 1, False, []
    while not p.gameOver(maze):
        print("Food left: \t", maze.remainingFood, "\t Score:  ", score)
        print(maze)
        print('\nActions available: ', p.actions(maze))
        run, ghosts, p, maze, score, dead = eachRun(run, ghosts, p, maze, score, dead, level)
    if dead: print("You died! Game over")
    else: print('Congratulations! You ate all the food. Your final score is: ',score)

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
    level = 1
    print("You are given ",score,'points')
    beginGame(maze, p, level)