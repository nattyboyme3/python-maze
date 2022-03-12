import colorama
from sys import argv
import random
import square_maze


def rand_coord(width, height):
    starting_height = int(random.random()*height)
    starting_width = int(random.random()*width)
    if starting_height == 0:
        starting_height += 1
    if starting_width == 0:
        starting_width += 1
    if starting_height == height-1:
        starting_height -= 1
    if starting_width == width-1:
        starting_width -= 1
    return [starting_width, starting_height]


if __name__ == '__main__':
    cell = 'c'
    wall = 'w'
    colorama.init()
    height = int(argv[2])
    width = int(argv[1])
    m = square_maze.Maze(width, height)
    start = rand_coord(width, height)
    m.set_cell(start, cell)

    walls = list()

    for i in m.get_adj_coord(start):
        walls.append(i)
        m.set(i, wall)
    retries = 0

    while walls:
        r = walls[int(random.random()*len(walls))-1]
        if m.adj_equal(r, cell) == 1:
            m.set_cell(r, cell)
            for i in m.get_adj_coord_not(r, cell):
                walls.append(i)
                m.set(i, wall)
        retries += 1
        walls.remove(r)
    m.finish_walls(wall)
    m.add_entrance(cell)
    m.add_exit(cell)

    m.print()
    print(f'iterated through {retries} walls.')
    m.draw_cells(cell)
    m.show_image()




