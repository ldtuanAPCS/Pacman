import time, os
import Pacman as P
import Ghost as G
import Food as F
import Map as M

def eachRun(ghosts, p, maze, stop):
    numFood = maze.remainingFood
    if maze.level == 4:
        for ghost in ghosts: ghost.ghostMove(maze, p)
    if maze.level == 3: stop = p.pacmanMove(maze, ghosts, stop, min(3, maze.width + maze.height - 6))
    else: stop = p.pacmanMove(maze, ghosts, stop, min(10, maze.width + maze.height - 6))
    if not stop: maze.score -= 1
    if numFood > maze.remainingFood: maze.score += 10
    return ghosts, p, maze, stop

def beginGame(maze, p, ghosts, start1, filename):
    step, stop = 1, None
    #stop status: True if pacman decide to stop the game, False means pacman win the game
    f = open(filename+'.out','w+')
    os.system('clear')
    print("\nStep 0\tFood left: ", maze.remainingFood, "\tScore:  ", maze.score)
    f.write("\nStep 0\tFood left: " +str(maze.remainingFood) + "\tScore:  " + str(maze.score) +'\n')
    maze.printMaze(f)
    time.sleep(2)
    start2 = time.time()
    while not p.gameOver(maze):
        ghosts, p, maze, stop = eachRun(ghosts, p, maze, stop)
        time.sleep(0.3)
        if not stop:
            os.system('clear')
            print("\nStep ",step ,"\tFood left: ", maze.remainingFood, "\tScore:  ", maze.score)
            f.write("\nStep " + str(step) + "\tFood left: " + str(maze.remainingFood) + "\tScore:  " + str(maze.score) +'\n')
            maze.printMaze(f)
            step += 1 
    if stop: 
        print("Pacman decide to stop the game. Total score is: ", maze.score)
        f.write("Pacman decide to stop the game. Total score is: " + str(maze.score) + '\n')
    else: 
        print('Congratulations! You ate all the food. Your final score is: ',maze.score)
        f.write('Congratulations! You ate all the food. Your final score is: ' + str(maze.score) + '\n')
    end = time.time()
    print('Calculated time from the very beginning: ',end - start1 - step*0.3 - 2)
    f.write('Calculated time from the very beginning: ' + str(end - start1 - step*0.3 - 2) + '\n')
    print('Calculated time from the first run     : ',end - start2 - step*0.3)
    f.write('Calculated time from the first run     : ' + str(end - start2 - step*0.3))
    f.close()
    time.sleep(2)

if __name__ == "__main__":
    start1 = time.time()
    filename = 'map/level4'
    maze = M.Map(filename+'.txt')
    p = P.Pacman(maze.pacmanSpawn)
    ghosts = [G.Ghost(maze.ghostSpawn)]
    beginGame(maze, p, ghosts, start1, filename)
