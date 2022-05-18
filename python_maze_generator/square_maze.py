import colorama
import random
from PIL import Image, ImageDraw
from anytree import Node
from sys import argv


class SquareMaze:
    def __init__(self, width, height, wall='w', cell='c'):
        self.maze = list()
        self.height = height
        self.width = width
        self.max_h = height - 1
        self.max_w = width - 1
        self.image_border = 3
        self.image_multiplier = 30
        self.wall_border = 5
        self.wall = wall
        self.cell = cell
        for i in range(0, height):
            line = []
            for j in range(0, width):
                line.append('u')
            self.maze.append(line)
        self.image = self.set_up_image()
        self.built = False
        self.exit = None
        self.entrance = None
        self.tree_root = None
        start = self.rand_coord(width, height)
        self.set_cell(start)
        self.cell = cell
        walls = list()
        for i in self.get_adj_coord(start):
            walls.append(i)
            self.set(i, wall)
        retries = 0
        while walls:
            r = random.choice(walls)
            if self.adj_equal(r, cell) == 1:
                self.set_cell(r)
                for i in self.get_adj_coord_not(r, self.cell):
                    walls.append(i)
                    self.set(i, wall)
            retries += 1
            walls.remove(r)
        self.finish_walls(wall)
        self.add_entrance()
        self.add_exit()
        print(f'iterated through {retries} walls.')

    @staticmethod
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

    def equals(self, coord: tuple, char: str):
        return self.get(coord) == char

    @staticmethod
    def same(coord1: tuple, coord2: tuple) -> bool:
        return all([coord1[0]==coord2[0], coord1[1] == coord2[1]])

    @staticmethod
    def dup(coord: tuple) -> tuple:
        r = (coord[0], coord[1])
        return r

    def get(self, coord):
        return self.maze[coord[0]][coord[1]]

    def set(self, coord, char):
        self.maze[coord[0]][coord[1]] = char

    def set_cell(self, coord):
        self.set(coord, self.cell)

    def get_adj_coord(self, coord):
        r = list()
        # up
        if coord[1] > 1:
            r.append((coord[0], coord[1]-1))
        # down
        if coord[1] < self.max_h - 1:
            r.append((coord[0], coord[1]+1))
        # left
        if coord[0] > 1:
            r.append((coord[0]-1, coord[1]))
        # right
        if coord[0] < self.max_w - 1:
            r.append((coord[0]+1, coord[1]))
        return r

    def get_adj(self, coord): # gets a list of all the adjacent cells' contents
        r = list()
        a = self.get_adj_coord(coord)
        for i in a:
            r.append(self.get(i))
        return r

    def adj_equal(self, coord, char): # Counts the adjacent cells equal to char
        r = 0
        adj_list = self.get_adj(coord)
        for i in adj_list:
            if i == char:
                r += 1
        return r

    def is_left_cell(self, coord):
        if coord[1] == 0:
            return True
        return self.equals((coord[0], coord[1]-1), self.cell)

    def is_right_cell(self, coord):
        if coord[1] == self.max_h:
            return True
        return self.equals((coord[0], coord[1]+1), self.cell)

    def is_up_cell(self, coord):
        if coord[0] == 0:
            return True
        return self.equals((coord[0]-1, coord[1]), self.cell)

    def is_down_cell(self, coord):
        if coord[0] == self.max_w:
            return True
        return self.equals((coord[0]+1, coord[1]), self.cell)

    def print(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.maze[i][j] == 'u':
                    print(colorama.Fore.WHITE, f'{self.maze[i][j]}', end="")
                if self.maze[i][j] == 'c':
                    print(colorama.Fore.GREEN, f'{self.maze[i][j]}', end="")
                if self.maze[i][j] == 'w':
                    print(colorama.Fore.RED, f'{self.maze[i][j]}', end="")
            print('\n', end="")

    def get_adj_coord_not(self, coord, char):
        r = list()
        for i in self.get_adj_coord(coord):
            if self.get(i) != char:
                r.append(i)
        return r

    def get_adj_coord_equal(self, coord, char):
        r = list()
        for i in self.get_adj_coord(coord):
            if self.get(i) == char:
                r.append(i)
        return r

    def finish_walls(self, wall_char):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.maze[i][j] == 'u':
                    self.maze[i][j] = wall_char

    def draw_cells(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                coord = (j, i)
                if self.equals(coord, self.cell):
                    if self.is_left_cell(coord):
                        offset = 0
                        if coord[1] == 0:
                            offset = self.image_border
                        rect_start = (
                            (self.image_border + (self.image_multiplier * coord[1]) - offset),
                            (self.image_border + (self.image_multiplier * coord[0]) + self.wall_border)
                        )
                        rect_end = (
                            (self.image_border + (self.image_multiplier * coord[1]) +
                             self.image_multiplier - self.wall_border),
                            (self.image_border + (self.image_multiplier * coord[0]) +
                             self.image_multiplier - self.wall_border)
                        )
                        drawing = ImageDraw.Draw(self.image)
                        drawing.rectangle([rect_start, rect_end], fill='white', outline='white')
                        del drawing
                    if self.is_right_cell(coord):
                        offset = 0
                        if coord[1] == self.max_w:
                            offset = self.image_border
                        rect_start = (
                            (self.image_border + (self.image_multiplier * coord[1]) + self.wall_border),
                            (self.image_border + (self.image_multiplier * coord[0]) + self.wall_border)
                        )
                        rect_end = (
                            (self.image_border + (self.image_multiplier * coord[1]) + self.image_multiplier + offset),
                            (self.image_border + (self.image_multiplier * coord[0]) +
                             self.image_multiplier - self.wall_border)
                        )
                        drawing = ImageDraw.Draw(self.image)
                        drawing.rectangle([rect_start, rect_end], fill='white', outline='white')
                        del drawing
                    if self.is_up_cell(coord):
                        offset = 0
                        if coord[0] == 0:
                            offset = self.image_border
                        rect_start = (
                            (self.image_border + (self.image_multiplier * coord[1]) + self.wall_border),
                            (self.image_border + (self.image_multiplier * coord[0]) - offset)
                        )
                        rect_end = (
                            (self.image_border + (self.image_multiplier * coord[1]) +
                             self.image_multiplier - self.wall_border),
                            (self.image_border + (self.image_multiplier * coord[0]) + self.image_multiplier - self.wall_border),
                        )

                        drawing = ImageDraw.Draw(self.image)
                        drawing.rectangle([rect_start, rect_end], fill='white', outline='white')
                        del drawing
                    if self.is_down_cell(coord):
                        offset = 0
                        if coord[0] == self.max_h:
                            offset = self.image_border
                        rect_start = (
                            (self.image_border + (self.image_multiplier * coord[1]) + self.wall_border),
                            (self.image_border + (self.image_multiplier * coord[0]) + self.wall_border),
                        )
                        rect_end = (
                            (self.image_border + (self.image_multiplier * coord[1]) +
                             self.image_multiplier - self.wall_border),
                            (self.image_border + (self.image_multiplier * coord[0]) + self.image_multiplier + offset)
                        )
                        drawing = ImageDraw.Draw(self.image)
                        drawing.rectangle([rect_start, rect_end], fill='white', outline='white')
                        del drawing

    def add_entrance(self):
        while True:
            index = int(random.random()*self.max_w)
            coord = (0, index)
            if self.adj_equal(coord, self.cell) > 0:
                self.set_cell(coord)
                self.entrance = coord
                break

    def add_exit(self):
        while True:
            index = int(random.random()*self.max_h)
            coord = (self.max_h, index)
            if self.adj_equal(coord, self.cell) > 0:
                self.set_cell(coord)
                self.exit = coord
                break

    def set_up_image(self):
        width = (self.width * self.image_multiplier) + (self.image_border * 2)
        height = (self.height * self.image_multiplier) + (self.image_border * 2)
        return Image.new(mode='RGB', size=(width, height))

    def show_image(self):
        self.image.show()

    def solve(self):
        if not all([self.exit, self.entrance]):
            return False
        self.tree_root = Node(name="root", coord=self.dup(self.entrance))
        ends = list()
        ends.append(self.tree_root)
        solved = False
        here = None
        while not solved:
            here = random.choice(ends)

            # Are we solved?
            if self.same(here.coord, self.exit):
                break
            for n in self.get_adj_coord_equal(here.coord, self.cell):
                ends.append(Node(name=str(n), parent=here, coord=n))
            ends.remove(here)
        back_at_start = False
        solution = list()
        while not here.is_root:
            if self.same(here.coord, self.entrance):
                break
            solution.append(here.coord)
            here = here.parent
        print(solution)
        print("finished!")


if __name__ == '__main__':
    cell = 'c'
    wall = 'w'
    colorama.init()
    height = int(argv[2])
    width = int(argv[1])
    m = SquareMaze(width, height, cell=cell, wall=wall)
    m.print()
    m.draw_cells()
    m.show_image()
    print("starting to solve...")
    # m.solve()