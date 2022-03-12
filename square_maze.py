import colorama
import random
from PIL import Image, ImageDraw

class Maze:
    def __init__(self, width, height):
        self.maze = list()
        self.height = height
        self.width = width
        self.max_h = height - 1
        self.max_w = width - 1
        self.image_border = 3
        self.image_multiplier = 20
        self.wall_border = 4
        self.draw_at_end = True
        for i in range(0, height):
            line = []
            for j in range(0, width):
                line.append('u')
            self.maze.append(line)
        self.image = self.set_up_image()

    def equals(self, coord, char):
        return self.get(coord) == char

    def get(self, coord):
        return self.maze[coord[0]][coord[1]]

    def set(self, coord, char):
        self.maze[coord[0]][coord[1]] = char

    def set_cell(self, coord, char):
        self.set(coord, char)
        if not self.draw_at_end:
            v_rect_start = (
                (self.image_border + (self.image_multiplier * coord[1]) + self.wall_border),
                (self.image_border + (self.image_multiplier * coord[0]))
            )
            v_rect_end = (
                (self.image_border + (self.image_multiplier * coord[1]) + self.image_multiplier - self.wall_border),
                (self.image_border + (self.image_multiplier * coord[0]) + self.image_multiplier)
            )
            h_rect_start = (
                (self.image_border + (self.image_multiplier * coord[1])),
                (self.image_border + (self.image_multiplier * coord[0]) + self.wall_border)
            )
            h_rect_end = (
                (self.image_border + (self.image_multiplier * coord[1]) + self.image_multiplier),
                (self.image_border + (self.image_multiplier * coord[0]) + self.image_multiplier - self.wall_border)
            )
            drawing = ImageDraw.Draw(self.image)
            drawing.rectangle([v_rect_start, v_rect_end], fill='white', outline='white')
            drawing.rectangle([h_rect_start, h_rect_end], fill='white', outline='white')
            del drawing

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

    def get_adj(self, coord):
        r = list()
        a = self.get_adj_coord(coord)
        for i in a:
            r.append(self.get(i))
        return r

    def adj_equal(self, coord, char):
        r = 0
        adj_list = self.get_adj(coord)
        for i in adj_list:
            if i == char:
                r += 1
        return r

    def is_left_cell(self, coord, cell_char):
        if coord[1] == 0:
            return True
        return self.equals((coord[0], coord[1]-1), cell_char)

    def is_right_cell(self, coord, cell_char):
        if coord[1] == self.max_h:
            return True
        return self.equals((coord[0], coord[1]+1), cell_char)

    def is_up_cell(self, coord, cell_char):
        if coord[0] == 0:
            return True
        return self.equals((coord[0]-1, coord[1]), cell_char)

    def is_down_cell(self, coord, cell_char):
        if coord[0] == self.max_w:
            return True
        return self.equals((coord[0]+1, coord[1]), cell_char)

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

    def finish_walls(self, wall_char):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.maze[i][j] == 'u':
                    self.maze[i][j] = wall_char

    def draw_cells(self, cell_char):
        for i in range(0, self.height):
            for j in range(0, self.width):
                coord = (j, i)
                if self.equals(coord, cell_char):
                    if self.is_left_cell(coord, cell_char):
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
                    if self.is_right_cell(coord, cell_char):
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
                    if self.is_up_cell(coord, cell_char):
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
                    if self.is_down_cell(coord, cell_char):
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

    def add_entrance(self, cell_c):
        while True:
            index = int(random.random()*self.max_w)
            coord = (0, index)
            if self.adj_equal(coord, cell_c) > 0:
                self.set_cell(coord, cell_c)
                break

    def add_exit(self, cell_c):
        while True:
            index = int(random.random()*self.max_h)
            coord = (self.max_h, index)
            if self.adj_equal(coord, cell_c) > 0:
                self.set_cell(coord, cell_c)
                break

    def set_up_image(self):
        width = (self.width * self.image_multiplier) + (self.image_border * 2)
        height = (self.height * self.image_multiplier) + (self.image_border * 2)
        return Image.new(mode='RGB', size=(width, height))

    def show_image(self):
        self.image.show()