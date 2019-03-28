import time, os
import Pacman as P
import Ghost as G
import Food as F
import Map as M

def eachRun(ghosts, p, maze, stop):
    numFood = maze.remainingFood
    if maze.level == 4:
        for ghost in ghosts: ghost.ghostMove(maze, p.location)
    if maze.level == 3: stop = p.pacmanMove(maze, ghosts, stop, min(3, maze.width + maze.height - 6))
    else: stop = p.pacmanMove(maze, ghosts, stop, min(10, maze.width + maze.height - 6))
    if not stop: maze.score -= 1
    if numFood > maze.remainingFood: maze.score += 10
    return ghosts, p, maze, stop

def beginGame(maze, p, ghosts):
    step, stop = 1, None
    #stop status: True if pacman decide to stop the game, False means pacman win the game
    os.system('clear')
    print("\nStep 0\tFood left: ", maze.remainingFood, "\tScore:  ", maze.score)
    print(maze)
    while not p.gameOver(maze):
        #print('Actions available: ', p.actions(maze))
        ghosts, p, maze, stop = eachRun(ghosts, p, maze, stop)
        time.sleep(1)
        os.system('clear')
        print("\nStep ",step ,"\tFood left: ", maze.remainingFood, "\tScore:  ", maze.score)
        print(maze)
        step += 1 
    if stop: print("Pacman decide to stop the game. Total score is: ", maze.score)
    else: print('Congratulations! You ate all the food. Your final score is: ',maze.score)

if __name__ == "__main__":
    #maze = M.Map('level/LV4_10x10.txt')
    maze = M.Map('level/level2.txt')
    p = P.Pacman(maze.pacmanSpawn)
    ghosts = [G.Ghost(maze.ghostSpawn)]
    beginGame(maze, p, ghosts)