import colorama
from sys import argv
import square_maze


if __name__ == '__main__':
    cell = 'c'
    wall = 'w'
    colorama.init()
    height = int(argv[2])
    width = int(argv[1])
    m = square_maze.Maze(width, height, cell=cell, wall=wall)
    m.print()
    m.draw_cells()
    m.show_image()
    print("starting to solve...")
    # m.solve()




