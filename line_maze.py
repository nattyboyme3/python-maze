import colorama
from sys import argv
import random
from PIL import Image, ImageDraw
from anytree import Node, search, RenderTree, AsciiStyle, walker

debug = False


class LineMaze:
    def __init__(self, h, w):
        self.maze_w = w
        self.maze_h = h
        self.undefined_wall = 'u'
        self.unevaluated_cell = 'U'
        self.current_cell = 'C'
        self.neighbor_cell = 'N'
        self.cell = ' '
        self.filled_wall = 'E'
        self.open_wall = ','
        self.solved_path = 'O'
        self.m = None
        try:
            self.build()
            self.define_maze(self.maze_h, self.maze_w)
            self.finish(self.maze_w)
        except Exception as e:
            self.print()
            pass
            raise e
        # Image Stuff
        self.image = None
        self.cell_size = 20
        self.wall_size = 3
        self.set_up_image()

    @staticmethod
    def coord_name(coord):
        return f"{str(coord[0])},{str(coord[1])}"

    @staticmethod
    def get_rand_cell_coord(s: int):
        r = 0
        while LineMaze.is_even(r):
            r = random.randint(0, s*2)
        return r

    @staticmethod
    def is_even(x: int):
        return x % 2 == 0

    @staticmethod
    def is_odd(x: int):
        return not LineMaze.is_even(x)

    def get_contents(self, y: int, x: int):
        return self.m[y][x]

    def set_contents(self, y: int, x: int, c):
        self.m[y][x] = c

    def set_contents_obj(self, coords, content=None):
        if not content:
            self.set_contents(coords[0], coords[1], coords[2])
        else:
            self.set_contents(coords[0], coords[1], content)

    def get_adj_cells(self, y, x):
        return_list = list()
        if LineMaze.is_odd(x) and LineMaze.is_odd(y):
            # North == Y - 2, assuming y > 2
            if y > 2:
                try:
                    return_list.append((y-2, x, self.get_contents(y-2, x)))
                except IndexError:
                    print("Something went wrong")
            # Top row? Check the border:
            if y == 2:
                try:
                    return_list.append((y-1, x, self.get_contents(y-1, x)))
                except IndexError:
                    print("Something went wrong")
            # South == Y + 2, assuming y < (len(m)-1)
            if y < (len(self.m)-2):
                try:
                    return_list.append((y+2, x, self.get_contents(y+2, x)))
                except IndexError:
                    print("Something went wrong")
            # Bottom row? Check the border:
            if y == (len(self.m)-2):
                try:
                    return_list.append((y+1, x, self.get_contents(y+1, x)))
                except IndexError:
                    print("Something went wrong")
            # West == X -2 , assuming x > 2
            if x > 2:
                try:
                    return_list.append((y, x-2, self.get_contents(y, x-2)))
                except IndexError:
                    print("Something went wrong")
            # East == X + 2, assuming x < (len(m[0]-1)
            if x < (len(self.m[0])-2):
                try:
                    return_list.append((y, x+2, self.get_contents(y, x+2)))
                except IndexError:
                    print("Something went wrong")
        return return_list

    def get_adj_cells_equal(self, y, x, c):
        cell_list = self.get_adj_cells(y, x)
        return_list = list()
        for i in cell_list:
            if i[2] == c:
                return_list.append(i)
        return return_list

    def build(self):
        self.m = list()
        for i in range(0, self.maze_h*2+1):
            self.m.append(list())
            for j in range(0, self.maze_w*2+1):
                if LineMaze.is_even(j) and LineMaze.is_even(i):
                    self.m[i].append(self.filled_wall)
                elif LineMaze.is_even(j) or LineMaze.is_even(i):
                    self.m[i].append(self.undefined_wall)
                else:
                    self.m[i].append(self.unevaluated_cell)

    def open_interposing_wall(self, cell_1, cell_2):
        if LineMaze.is_even(cell_1[0]) or LineMaze.is_even(cell_1[1]) \
                or LineMaze.is_even(cell_2[0]) or LineMaze.is_even(cell_2[1]):
            raise RuntimeError("Trying to do stuff that's not cells")
        # Cell 2 is North of Cell 1 X's equal, Cell 2's y == Cell 1' Y - 2
        # wall coords = Cell 1 X, Cell 1 Y - 1
        if cell_1[1] == cell_2[1] and cell_1[0]-2 == cell_2[0]:
            self.set_contents(cell_1[0]-1, cell_1[1], self.open_wall)
            return
        # Cell 2 is South of Cell 1 X's equal, Cell 2's y == Cell 1' Y + 2
        # wall coords = Cell 1 X, Cell 1 Y + 1
        if cell_1[1] == cell_2[1] and cell_1[0]+2 == cell_2[0]:
            self.set_contents(cell_1[0]+1, cell_1[1], self.open_wall)
            return
        # Cell 2 is West of Cell 1 Y's equal, Cell 2's X == Cell 1' X - 2
        # wall coords = Cell 1 X-1, Cell 1 Y
        if cell_1[0] == cell_2[0] and cell_1[1]-2 == cell_2[1]:
            self.set_contents(cell_1[0], cell_1[1]-1, self.open_wall)
            return
        # Cell 2 is East of Cell 1 Y's equal, Cell 2's X == Cell 1' X + 2
        # wall coords = Cell 1 X+1, Cell 1 Y
        if cell_1[0] == cell_2[0] and cell_1[1]+2 == cell_2[1]:
            self.set_contents(cell_1[0], cell_1[1]+1, self.open_wall)
            return
        raise RuntimeError("Somehow these weren't adjacent")

    def print(self):
        for i in range(0, len(self.m)):
            for j in range(0, len(self.m[0])):
                if self.m[i][j] == self.undefined_wall:
                    print(colorama.Back.WHITE, f'{self.m[i][j]}', end="")
                if self.m[i][j] == self.unevaluated_cell:
                    print(colorama.Back.LIGHTWHITE_EX, f'{self.m[i][j]}', end="")
                if self.m[i][j] == self.cell:
                    print(colorama.Back.GREEN, f'{self.m[i][j]}', end="")
                if self.m[i][j] == self.filled_wall:
                    print(colorama.Back.BLACK, f'{self.m[i][j]}', end="")
                if self.m[i][j] == self.open_wall:
                    print(colorama.Back.LIGHTGREEN_EX, f'{self.m[i][j]}', end="")
                if self.m[i][j] == self.current_cell:
                    print(colorama.Back.RED, f'{self.m[i][j]}', end="")
                if self.m[i][j] == self.neighbor_cell:
                    print(colorama.Back.LIGHTBLUE_EX, f'{self.m[i][j]}', end="")
                if self.m[i][j] == self.solved_path:
                    print(colorama.Back.BLUE, f'{self.m[i][j]}', end="")
            print('\n', end="")

    def define_maze(self, h, w):
        y = LineMaze.get_rand_cell_coord(h)
        x = LineMaze.get_rand_cell_coord(w)
        self.set_contents(y, x, self.cell)
        to_evaluate = list()
        adj_cells = self.get_adj_cells(y, x)
        for i in adj_cells:
            to_evaluate.append(i)
        while len(to_evaluate) > 0:
            self.expand(to_evaluate)

    def expand(self, cell_list):
        neighbor = None
        this_cell = random.choice(cell_list)
        self.set_contents(this_cell[0], this_cell[1], self.cell)
        evaluated_cells = self.get_adj_cells_equal(this_cell[0], this_cell[1], self.cell)
        if len(evaluated_cells) < 1:
            if debug:
                print("this should be impossible")
                self.print()
            pass
        else:
            neighbor = random.choice(evaluated_cells)
            self.open_interposing_wall(this_cell, neighbor)
        adj_unevaluated_cells = self.get_adj_cells_equal(this_cell[0], this_cell[1], self.unevaluated_cell)
        for i in adj_unevaluated_cells:
            if i not in cell_list:
                cell_list.append(i)
        cell_list.remove(this_cell)
        if debug:
            self.set_contents(neighbor[0], neighbor[1], self.neighbor_cell)
            self.set_contents(this_cell[0], this_cell[1], self.current_cell)
            self.print()
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            self.set_contents(this_cell[0], this_cell[1], self.cell)
            self.set_contents(neighbor[0], neighbor[1], self.cell)

    def finish(self, w):
        for i in range(0, len(self.m)):
            for j in range(0, len(self.m[0])):
                if self.m[i][j] == self.undefined_wall:
                    self.m[i][j] = self.filled_wall
        # Entrance
        top_x = self.get_rand_cell_coord(w)
        self.set_contents(0, top_x, self.cell)
        # Exit
        bottom_x = self.get_rand_cell_coord(w)
        self.set_contents(len(self.m)-1, bottom_x, self.cell)

    def find_entrance(self):
        entrance_x = None
        for i in range(0, len(self.m[0])-1):
            if self.m[0][i] == self.cell:
                entrance_x = i
        return 0, entrance_x, self.cell

    def find_exit(self):
        bottom = len(self.m)-1
        exit_x = None
        for i in range(0, len(self.m[0])-1):
            if self.m[bottom][i] == self.cell:
                exit_x = i
        return bottom, exit_x, self.cell

    def solve(self):
        en = self.find_entrance()
        ex = self.find_exit()
        path = self.walk(en, ex)
        count = 0
        for i in path[0]:
            self.set_contents_obj(i.coord, self.solved_path)
            count += 1
        if path[1]:
            self.set_contents_obj(path[1].coord, self.solved_path)
            count += 1
        for j in path[2]:
            self.set_contents_obj(j.coord, self.solved_path)
            count += 1
        return count

    def walk(self, maze_entrance, maze_exit):
        to_map = list()
        root = Node(LineMaze.coord_name(maze_entrance), coord=maze_entrance)
        last = root
        to_map.append(((maze_entrance[0]+1, maze_entrance[1], self.cell), maze_entrance))
        visited = list()
        while len(to_map) > 0:
            here = random.choice(to_map)
            if debug:
                print(f"visiting {LineMaze.coord_name(here[0])}")
            parent_node = search.find_by_attr(root, LineMaze.coord_name(here[1]))
            last = Node(LineMaze.coord_name(here[0]), parent=parent_node, coord=here[0])
            adj_cells = self.get_adj_cells_equal(here[0][0], here[0][1], self.cell)
            openings = list()
            for a in adj_cells:
                if self.cells_connected(a, here[0]):
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
                        print(f"adding connected {LineMaze.coord_name(i)} to visit list")
                    to_map.append((i, here[0]))
            visited.append(here)
            to_map.remove(here)
            if debug:
                print(RenderTree(root, style=AsciiStyle()))
            pass
        exit_node = search.find_by_attr(root, LineMaze.coord_name(maze_exit))
        w = walker.Walker()
        return w.walk(root, exit_node)

    def cells_connected(self, cell_1, cell_2):
        # Handle the borders -- cells are directly adjacent
        if abs(cell_1[0] - cell_2[0]) == 1 or abs(cell_1[1] - cell_2[1]) == 1:
            return True
        if LineMaze.is_even(cell_1[0]) or LineMaze.is_even(cell_1[1]) or \
                LineMaze.is_even(cell_2[0]) or LineMaze.is_even(cell_2[1]):
            raise RuntimeError("Trying to do stuff that's not cells or borders")
        # Cell 2 is North of Cell 1 -- X's equal, Cell 2's y == Cell 1' Y - 2
        # wall coords = Cell 1 X, Cell 1 Y - 1
        if cell_1[1] == cell_2[1] and cell_1[0]-2 == cell_2[0]:
            return self.get_contents(cell_1[0]-1, cell_1[1]) == self.open_wall
        # Cell 2 is South of Cell 1 X's equal, Cell 2's y == Cell 1' Y + 2
        # wall coords = Cell 1 X, Cell 1 Y + 1
        if cell_1[1] == cell_2[1] and cell_1[0]+2 == cell_2[0]:
            return self.get_contents(cell_1[0]+1, cell_1[1]) == self.open_wall
        # Cell 2 is West of Cell 1 Y's equal, Cell 2's X == Cell 1' X - 2
        # wall coords = Cell 1 X-1, Cell 1 Y
        if cell_1[0] == cell_2[0] and cell_1[1]-2 == cell_2[1]:
            return self.get_contents(cell_1[0], cell_1[1]-1) == self.open_wall
        # Cell 2 is East of Cell 1 Y's equal, Cell 2's X == Cell 1' X + 2
        # wall coords = Cell 1 X+1, Cell 1 Y
        if cell_1[0] == cell_2[0] and cell_1[1]+2 == cell_2[1]:
            return self.get_contents(cell_1[0], cell_1[1]+1) == self.open_wall
        raise RuntimeError("Somehow these weren't adjacent")

    def set_up_image(self):
        height = (self.maze_h * (self.cell_size + self.wall_size)) + self.wall_size + 1
        width = (self.maze_w * (self.cell_size + self.wall_size)) + self.wall_size + 1
        self.image = Image.new(mode='RGB', size=(width, height))

    def show_image(self):
        self.image.show()

    def draw(self, solved=False):
        y_index = 0
        for i in range(0, len(self.m)):
            x_index = 0
            for j in range(0, len(self.m[0])):
                cell_contents = self.get_contents(i, j)
                write = False
                is_point = None
                is_vert = None
                is_horiz = None
                color = 'white'
                x_end = None
                y_end = None
                # Always XY
                start = (x_index, y_index)
                is_wall = LineMaze.is_even(i) or LineMaze.is_even(j)
                if is_wall:
                    if cell_contents == self.open_wall or cell_contents == self.cell or \
                            cell_contents == self.solved_path:
                        write = True
                    is_point = LineMaze.is_even(i) and LineMaze.is_even(j)
                    is_vert = LineMaze.is_odd(i)
                    is_horiz = LineMaze.is_odd(j)
                    if is_point:
                        x_end = x_index + self.wall_size
                        y_end = y_index + self.wall_size
                    elif is_vert:
                        x_end = x_index + self.wall_size
                        y_end = y_index + self.cell_size
                    elif is_horiz:
                        x_end = x_index + self.cell_size
                        y_end = y_index + self.wall_size
                    else:
                        print("This should not be possible")
                        pass
                else:
                    write = True
                    x_end = x_index + self.cell_size
                    y_end = y_index + self.cell_size
                end = (x_end, y_end)
                if write:
                    if cell_contents == self.solved_path and solved:
                        color = 'red'
                    drawing = ImageDraw.Draw(self.image)
                    drawing.rectangle([start, end], fill=color, outline=color)
                    del drawing
                # Update indices
                x_index = x_end
            y_index = y_end


if __name__ == '__main__':
    # Defaults:
    maze_h = 50
    maze_w = 50
    attempts = 15
    # Args
    if len(argv) > 1:
        maze_h = int(argv[1])
        maze_w = int(argv[1])
    if len(argv) > 2:
        maze_w = int(argv[2])
    if len(argv) > 3:
        attempts = int(argv[3])
    # Generate SquareMaze
    best_maze = None
    for maze in range(0, attempts):
        m = LineMaze(maze_h, maze_w)
        length = m.solve()
        if not best_maze or length > best_maze[1]:
            best_maze = (m, length)
            print(f"\nnew best: {length}")
        else:
            print('.', end='')
    print("\n")
    # best_maze[0].print()
    best_maze[0].draw(solved=True)
    best_maze[0].show_image()
    best_maze[0].set_up_image()
    best_maze[0].draw(solved=False)
    best_maze[0].show_image()
    print(f"done: best quality {best_maze[1]}")
