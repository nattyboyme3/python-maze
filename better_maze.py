import colorama
from sys import argv
import random
from PIL import Image, ImageDraw
from anytree import Node, search, RenderTree, AsciiStyle, walker

maze_w = 20
maze_h = 20
debug = False

undefined_wall = 'u'
unevaluated_cell = 'U'
current_cell = 'C'
neighbor_cell = 'N'
cell = ' '
filled_wall = 'E'
open_wall = ','
solved_path = 'O'


def get_rand_cell_coord(s: int):
    r = 0
    while is_even(r):
        r = random.randint(0, s*2)
    return r


def get_contents(m: list, y: int, x: int):
    return m[y][x]


def set_contents(m: list, y: int, x: int, c):
    m[y][x] = c


def set_contents_obj(m, coords, content=None):
    if not content:
        set_contents(m, coords[0], coords[1], coords[2])
    else:
        set_contents(m, coords[0], coords[1], content)


def get_adj_cells(m, y, x):
    return_list = list()
    if is_odd(x) and is_odd(y):
        # North == Y - 2, assuming y > 2
        if y > 2:
            try:
                return_list.append((y-2, x, get_contents(m, y-2, x)))
            except IndexError:
                print("Something went wrong")
        # Top row? Check the border:
        if y == 2:
            try:
                return_list.append((y-1, x, get_contents(m, y-1, x)))
            except IndexError:
                print("Something went wrong")
        # South == Y + 2, assuming y < (len(m)-1)
        if y < (len(m)-2):
            try:
                return_list.append((y+2, x, get_contents(m, y+2, x)))
            except IndexError:
                print("Something went wrong")
        # Bottom row? Check the border:
        if y == (len(m)-2):
            try:
                return_list.append((y+1, x, get_contents(m, y+1, x)))
            except IndexError:
                print("Something went wrong")
        # West == X -2 , assuming x > 2
        if x > 2:
            try:
                return_list.append((y, x-2, get_contents(m, y, x-2)))
            except IndexError:
                print("Something went wrong")
        # East == X + 2, assuming x < (len(m[0]-1)
        if x < (len(m[0])-2):
            try:
                return_list.append((y, x+2, get_contents(m, y, x+2)))
            except IndexError:
                print("Something went wrong")


    return return_list


def get_adj_cells_equal(m, y, x, c):
    cell_list = get_adj_cells(m, y, x)
    return_list = list()
    for i in cell_list:
        if i[2] == c:
            return_list.append(i)
    return return_list


def is_even(x: int):
    return x % 2 == 0


def is_odd(x: int):
    return not is_even(x)


def build_maze(h: int, w: int):
    m = list()
    for i in range(0,h*2+1):
        m.append(list())
        for j in range(0,w*2+1):
            if is_even(j) and is_even(i):
                m[i].append(filled_wall)
            elif is_even(j) or is_even(i):
                m[i].append(undefined_wall)
            else:
                m[i].append(unevaluated_cell)
    return m


def open_interposing_wall(m, cell_1, cell_2):
    if is_even(cell_1[0]) or is_even(cell_1[1]) or is_even(cell_2[0]) or is_even(cell_2[1]):
        raise RuntimeError("Trying to do stuff that's not cells")
    # Cell 2 is North of Cell 1 X's equal, Cell 2's y == Cell 1' Y - 2
    # wall coords = Cell 1 X, Cell 1 Y - 1
    if cell_1[1] == cell_2[1] and cell_1[0]-2 == cell_2[0]:
        set_contents(m, cell_1[0]-1, cell_1[1], open_wall)
        return
    # Cell 2 is South of Cell 1 X's equal, Cell 2's y == Cell 1' Y + 2
    # wall coords = Cell 1 X, Cell 1 Y + 1
    if cell_1[1] == cell_2[1] and cell_1[0]+2 == cell_2[0]:
        set_contents(m, cell_1[0]+1, cell_1[1], open_wall)
        return
    # Cell 2 is West of Cell 1 Y's equal, Cell 2's X == Cell 1' X - 2
    # wall coords = Cell 1 X-1, Cell 1 Y
    if cell_1[0] == cell_2[0] and cell_1[1]-2 == cell_2[1]:
        set_contents(m, cell_1[0], cell_1[1]-1, open_wall)
        return
    # Cell 2 is East of Cell 1 Y's equal, Cell 2's X == Cell 1' X + 2
    # wall coords = Cell 1 X+1, Cell 1 Y
    if cell_1[0] == cell_2[0] and cell_1[1]+2 == cell_2[1]:
        set_contents(m, cell_1[0], cell_1[1]+1, open_wall)
        return
    raise RuntimeError("Somehow these weren't adjacent")


def print_maze(m: list):
    for i in range(0, len(m)):
        for j in range(0, len(m[0])):
            if m[i][j] == undefined_wall:
                print(colorama.Back.WHITE, f'{m[i][j]}', end="")
            if m[i][j] == unevaluated_cell:
                print(colorama.Back.LIGHTWHITE_EX, f'{m[i][j]}', end="")
            if m[i][j] == cell:
                print(colorama.Back.GREEN, f'{m[i][j]}', end="")
            if m[i][j] == filled_wall:
                print(colorama.Back.BLACK, f'{m[i][j]}', end="")
            if m[i][j] == open_wall:
                print(colorama.Back.LIGHTGREEN_EX, f'{m[i][j]}', end="")
            if m[i][j] == current_cell:
                print(colorama.Back.RED, f'{m[i][j]}', end="")
            if m[i][j] == neighbor_cell:
                print(colorama.Back.LIGHTBLUE_EX, f'{m[i][j]}', end="")
            if m[i][j] == solved_path:
                print(colorama.Back.BLUE, f'{m[i][j]}', end="")
        print('\n', end="")


def define_maze(m, h, w):
    y = get_rand_cell_coord(h)
    x = get_rand_cell_coord(w)
    set_contents(m, y, x, cell)
    to_evaluate = list()
    adj_cells = get_adj_cells(m, y, x)
    for i in adj_cells:
        to_evaluate.append(i)
    while len(to_evaluate) > 0:
        expand_maze(m, to_evaluate)


def expand_maze(m, cell_list):
    neighbor = None
    this_cell = random.choice(cell_list)
    set_contents(m, this_cell[0], this_cell[1], cell)
    evaluated_cells = get_adj_cells_equal(m, this_cell[0], this_cell[1], cell)
    if len(evaluated_cells) < 1:
        if debug:
            print("this should be impossible")
            print_maze(m)
        pass
    else:
        neighbor = random.choice(evaluated_cells)
        open_interposing_wall(m, this_cell, neighbor)
    adj_unevaluated_cells = get_adj_cells_equal(m, this_cell[0], this_cell[1], unevaluated_cell)
    for i in adj_unevaluated_cells:
        if i not in cell_list:
            cell_list.append(i)
    cell_list.remove(this_cell)
    if debug:
        set_contents(m, neighbor[0], neighbor[1], neighbor_cell)
        set_contents(m, this_cell[0], this_cell[1], current_cell)
        print_maze(m)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        set_contents(m, this_cell[0], this_cell[1], cell)
        set_contents(m, neighbor[0], neighbor[1], cell)


def finish_maze(m, w):
    for i in range(0, len(m)):
        for j in range(0, len(m[0])):
            if m[i][j] == undefined_wall:
                m[i][j] = filled_wall
    # Entrance
    top_x = get_rand_cell_coord(w)
    set_contents(m, 0, top_x, cell)
    # Exit
    bottom_x = get_rand_cell_coord(w)
    set_contents(m, len(m)-1, bottom_x, cell)


def find_entrance(m):
    entrance_x = None
    for i in range(0, len(m[0])-1):
        if m[0][i] == cell:
            entrance_x = i
    return 0, entrance_x, cell


def find_exit(m):
    bottom = len(m)-1
    exit_x = None
    for i in range(0, len(m[0])-1):
        if m[bottom][i] == cell:
            exit_x = i
    return bottom, exit_x, cell


def coord_name(coord):
    return f"{str(coord[0])},{str(coord[1])}"


def solve_maze(m):
    en = find_entrance(m)
    ex = find_exit(m)
    path = walk_maze(m, en, ex)
    count = 0
    for i in path[0]:
        set_contents_obj(m, i.coord, solved_path)
        count +=1
    if path[1]:
        set_contents_obj(m, path[1].coord, solved_path)
        count +=1
    for j in path[2]:
        set_contents_obj(m, j.coord, solved_path)
        count +=1
    return count


def walk_maze(m, maze_entrance, maze_exit):
    to_map = list()
    root = Node(coord_name(maze_entrance), coord=maze_entrance)
    last = root
    to_map.append(((maze_entrance[0]+1, maze_entrance[1], cell), maze_entrance))
    visited = list()
    while len(to_map) > 0:
        here = random.choice(to_map)
        if debug:
            print(f"visiting {coord_name(here[0])}")
        parent_node = search.find_by_attr(root, coord_name(here[1]))
        last = Node(coord_name(here[0]), parent=parent_node, coord=here[0])
        adj_cells = get_adj_cells_equal(m, here[0][0], here[0][1], cell)
        openings = list()
        for a in adj_cells:
            if cells_connected(m, a, here[0]):
                openings.append(a)
        for i in openings:
            unique = True
            for j in to_map:
                if i[0] == j[0][0] and i[1] == j[0][1]:
                    unique = False
            for q in visited:
                if i[0] == q[0][0] and i[1] == q[0][1]:
                    unique = False
            if unique:
                if debug:
                    print(f"adding connected {coord_name(i)} to visit list")
                to_map.append((i, here[0]))
        visited.append(here)
        to_map.remove(here)
        if debug:
            print(RenderTree(root, style=AsciiStyle()))
        pass
    exit_node = search.find_by_attr(root, coord_name(maze_exit))
    w = walker.Walker()
    return w.walk(root, exit_node)


def cells_connected(m, cell_1, cell_2):
    # Handle the borders -- cells are directly adjacent
    if abs(cell_1[0] - cell_2[0]) == 1 or abs(cell_1[1] - cell_2[1]) == 1:
        return True
    if is_even(cell_1[0]) or is_even(cell_1[1]) or is_even(cell_2[0]) or is_even(cell_2[1]):
        raise RuntimeError("Trying to do stuff that's not cells or borders")
    # Cell 2 is North of Cell 1 -- X's equal, Cell 2's y == Cell 1' Y - 2
    # wall coords = Cell 1 X, Cell 1 Y - 1
    if cell_1[1] == cell_2[1] and cell_1[0]-2 == cell_2[0]:
        return get_contents(m, cell_1[0]-1, cell_1[1]) == open_wall
    # Cell 2 is South of Cell 1 X's equal, Cell 2's y == Cell 1' Y + 2
    # wall coords = Cell 1 X, Cell 1 Y + 1
    if cell_1[1] == cell_2[1] and cell_1[0]+2 == cell_2[0]:
        return get_contents(m, cell_1[0]+1, cell_1[1]) == open_wall
    # Cell 2 is West of Cell 1 Y's equal, Cell 2's X == Cell 1' X - 2
    # wall coords = Cell 1 X-1, Cell 1 Y
    if cell_1[0] == cell_2[0] and cell_1[1]-2 == cell_2[1]:
        return get_contents(m, cell_1[0], cell_1[1]-1) == open_wall
    # Cell 2 is East of Cell 1 Y's equal, Cell 2's X == Cell 1' X + 2
    # wall coords = Cell 1 X+1, Cell 1 Y
    if cell_1[0] == cell_2[0] and cell_1[1]+2 == cell_2[1]:
        return get_contents(m, cell_1[0], cell_1[1]+1) == open_wall
    raise RuntimeError("Somehow these weren't adjacent")


if __name__ == '__main__':
    if len(argv) == 2:
        maze_h = int(argv[0])
        maze_w = int(argv[1])
    best_maze = None
    for i in range(0,200):
        maze = build_maze(maze_h, maze_w)
        try:
            define_maze(maze, maze_h, maze_w)
        except Exception as e:
            print_maze(maze)
            pass
            raise e
        finish_maze(maze, maze_w)
        length = solve_maze(maze)
        if not best_maze or length > best_maze[1]:
            best_maze = (maze, length)
            print(f"\nnew best: {length}")
        else:
            print('.', end='')
    print("\n")
    print_maze(best_maze[0])
    print(f"done: best quality {best_maze[1]}")

    


