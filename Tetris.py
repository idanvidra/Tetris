import random
import time
import turtle
import numpy as np

from Figures import Figures


class Tetris():
    level = 2
    score = 0
    state = "start"
    '''
    state -> game state - start or gameover
    '''
    field = []
    '''
    field-> game field (numpy array). 0 if pixel is empty, number if it has piece.
    except for active piece
    '''
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None

    def __init__(self, height, width):
        '''
        create new game field of size height x width
        '''
        self.height = height
        self.width = width
        # for i in range(height):
        #     new_line = []
        #     for j in range(width):
        #         new_line.append(0)
        #     self.field.append(new_line)
        self.field = np.zeros((height, width), dtype=int)
        self.score = 0
        self.state = "start"

    def new_figure(self):
        '''
        new figure appears on the screen at coordinate 3,0
        '''
        self.figure = Figures(3, 0)

    def intersect(self):
        '''
        check for intersection.
        used to check if we are allowed to move or rotate the figure.
        we check each cell in the 4x4 matrix of the current figure
        whether it is out of the game bounds and whether it is touching
        some busy game field.
        '''
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def freeze(self):
        '''
        check if we are allowed to move or rotate the figure.
        if it moves down and intersects, then it means we have reached to bottom,
        so we need to freeze the figure on our field.
        '''
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j +
                                                  self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersect():
            self.state = "gameover"

    def break_lines(self):
        '''
        check for full lines. 
        destroying a line goes from the bottom to the top.
        '''
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    # moving methods
    def go_space(self):
        while not self.intersect():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersect():
            self.figure.y -= 1
            self.freeze()

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersect():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersect():
            self.figure.rotation = old_rotation


class Shape():
    def __init__(self) -> None:
        self.x = 5
        self.y = 0
        self.color = random.randint(1, 7)

        # block shape
        square = [[1, 1],
                  [1, 1]]
        horizontal_line = [[1, 1, 1, 1]]
        vertical_line = [[1],
                         [1],
                         [1],
                         [1]]
        left_l = [[1, 0, 0, 0],
                  [1, 1, 1, 1]]
        right_l = [[0, 0, 0, 1],
                   [1, 1, 1, 1]]
        left_s = [[1, 1, 0],
                  [0, 1, 1]]
        right_s = [[0, 1, 1],
                   [1, 1, 0]]
        t = [[0, 1, 0],
             [1, 1, 1]]

        self.shapes = [square, horizontal_line, vertical_line,
                       left_l, right_l, left_s, right_s, t]

        # choose random shape each iteration
        self.shape = random.choice(self.shapes)
        self.height = len(self.shape)
        self.width = len(self.shape[0])

    def move_left(self, grid):
        if self.x > 0:
            if grid[self.y][self.x - 1] == 0:
                self.erase_shape(grid)
                self.x -= 1

    def move_right(self, grid):
        if self.x < 12 - self.width:
            if grid[self.y][self.x + self.width] == 0:
                self.erase_shape(grid)
                self.x += 1

    def draw_shape(self, grid):
        for y in range(self.height):
            for x in range(self.width):
                if(self.shape[y][x] == 1):
                    grid[self.y + y][self.x + x] = self.color

    def erase_shape(self, grid):
        for y in range(self.height):
            for x in range(self.width):
                if(self.shape[y][x] == 1):
                    grid[self.y + y][self.x + x] == 0

    def can_move(self, grid):
        result = True
        for x in range(self.width):
            # check if bottom is a 1
            if(self.shape[self.height-1][x] == 1):
                if(grid[self.y + self.height][self.x + x] != 0):
                    result = False
        return result

    def rotate(self, grid):
        # first erase current shape
        self.erase_shape(grid)
        rotated_shape = []
        for x in range(len(self.shape[0])):
            new_row = []
            for y in range(len(self.shape) - 1, -1, -1):
                new_row.append(self.shape[y][x])
            rotated_shape.append(new_row)

        right_side = self.x + len(rotated_shape[0])
        if right_side < len(grid[0]):
            self.shape = rotated_shape
            # update the height and width
            self.height = len(self.shape)
            self.width = len(self.shape[0])


class Turtle_Tetris():
    '''
    made using: https://github.com/wynand1004/Projects/blob/master/Tetris/tetris.py
    '''

    def __init__(self) -> None:

        self.delay = 0.1
        self.grid = np.ndarray.tolist(np.zeros((24, 12), dtype=int))

        # background
        self.win = turtle.Screen()
        self.win.title("Tetris")
        self.win.bgcolor("NavajoWhite2")
        self.win.setup(width=600, height=800)
        self.win.tracer(0)

        # create the drawing pen
        self.pen = turtle.Turtle()
        self.pen.penup()
        self.pen.speed(0)
        self.pen.shape("square")
        self.pen.setundobuffer(None)

        # game score
        self.score = 0

        # soreboard
        self.scoreboard = turtle.Turtle()
        self.scoreboard.speed(0)
        self.scoreboard.color('white')
        self.scoreboard.hideturtle()  # make turtle invisable - hide the shape
        self.scoreboard.goto(0, 270)  # set scoreboard at the top of the screen
        self.scoreboard.penup()
        self.scoreboard.write("Score: {}".format(
            self.score), align='center', font=('Courier', 24, 'normal'))

        # initial shape
        self.shape = Shape()

        # put the shape in the grid
        self.grid[self.shape.y][self.shape.x] = self.shape.color

        # keyboard control
        self.win.listen()
        self.win.onkeypress(lambda: self.shape.move_left(self.grid), 'Left')
        self.win.onkeypress(lambda: self.shape.move_right(self.grid), 'Right')
        self.win.onkeypress(lambda: self.shape.rotate(self.grid), 'space')

    def draw_grid(self):
        self.pen.clear()
        top = 230
        left = -110

        colors = ["black", "lightblue", "blue",
                  "orange", "yellow", "green", "purple", "red"]

        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                screen_x = left + (x * 20)
                screen_y = top - (y * 20)
                color_number = self.grid[y][x]
                color = colors[color_number]
                self.pen.color(color)
                self.pen.goto(screen_x, screen_y)
                self.pen.stamp()

    def check_grid(self):
        # check if each row is full
        y = 23
        while y > 0:
            is_full = True
            for x in range(0, 12):
                if self.grid[y][x] == 0:
                    is_full = False
                    y -= 1
                    break
            if is_full:
                self.score += 10
                self.draw_score()
                for copy_y in range(y, 0, -1):
                    for copy_x in range(0, 12):
                        self.grid[copy_y][copy_x] = self.grid[copy_y-1][copy_x]

    def draw_score(self):
        self.pen.color("blue")
        self.scoreboard.clear()
        self.scoreboard.write("Score: {}".format(
            self.score), align='center', font=('Courier', 24, 'normal'))

    def main_loop(self):
        while True:
            self.win.update()

            # Move the shape
            # Open Row
            # Check for the bottom
            if self.shape.y == 23 - self.shape.height + 1:
                self.shape = Shape()
                self.check_grid()

            # check for collision with next row
            elif self.shape.can_move(self.grid):
                # erase the current shape
                self.shape.erase_shape(self.grid)

                # move the shape by 1
                self.shape.y += 1

                # draw the shape again
                self.shape.draw_shape(self.grid)

            else:
                self.shape = Shape()
                self.check_grid()

            # draw on screen
            self.draw_grid()
            self.draw_score()

            time.sleep(self.delay)


if __name__ == "__main__":
    # a = Tetris(5, 5)

    T = Turtle_Tetris()
    T.main_loop()
