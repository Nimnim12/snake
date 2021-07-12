from enum import Enum
from math import floor
from tkinter import messagebox
import random

import pygame


class Maze:
    ARENA_HEIGHT = 10
    ARENA_WIDTH = 10
    ARENA_SIZE = ARENA_WIDTH * ARENA_HEIGHT

    class Node:
        def __init__(self):
            self.visited = False
            self.canGoRight = False
            self.canGoDown = False

    def __init__(self):
        self.nodes = [self.Node() for i in range(floor(self.ARENA_SIZE / 4))]
        self.tourToNumber = [None] * self.ARENA_SIZE

    def getPathNumber(self, x, y):
        return self.tourToNumber[floor(x + self.ARENA_WIDTH * y)]

    def markVisited(self, x, y):
        self.nodes[floor(x + y * self.ARENA_WIDTH / 2)].visited = True

    def markCanGoRight(self, x, y):
        self.nodes[floor(x + y * self.ARENA_WIDTH / 2)].canGoRight = True

    def markCanGoDown(self, x, y):
        self.nodes[floor(x + y * self.ARENA_WIDTH / 2)].canGoDown = True

    def canGoRight(self, x, y):
        return self.nodes[floor(x + y * self.ARENA_WIDTH / 2)].canGoRight

    def canGoDown(self, x, y):
        return self.nodes[floor(x + y * self.ARENA_WIDTH / 2)].canGoDown

    def canGoLeft(self, x, y):
        if x == 0:
            return False
        return self.nodes[floor((x - 1) + y * self.ARENA_WIDTH / 2)].canGoRight

    def canGoUp(self, x, y):
        if (y == 0):
            return False
        return self.nodes[floor(x + (y - 1) * self.ARENA_WIDTH / 2)].canGoDown

    def isVisited(self, x, y):
        return self.nodes[floor(x + y * self.ARENA_WIDTH / 2)].visited

    def calc_dist(self, a, b):
        if (a > b):
            dist = a - b - 1
        else:
            dist = a - b - 1 + self.ARENA_SIZE
        return dist

    def generate(self):
        self.generate_r(-1, -1, 0, 0)
        self.generateTourNumber()

    def generate_r(self, fromx, fromy, x, y):
        if (x < 0 or y < 0 or x >= self.ARENA_WIDTH / 2 or y >= self.ARENA_HEIGHT / 2):
            return
        if (self.isVisited(x, y)):
            return
        self.markVisited(x, y)

        if (fromx != -1):
            if (fromx < x):
                self.markCanGoRight(fromx, fromy)
            elif (fromx > x):
                self.markCanGoRight(x, y)
            elif (fromy < y):
                self.markCanGoDown(fromx, fromy)
            elif (fromy > y):
                self.markCanGoDown(x, y)

        for i in range(2):
            r = random.randint(0, 3)
            if r == 0:
                self.generate_r(x, y, x - 1, y)
            elif r == 1:
                self.generate_r(x, y, x + 1, y)
            elif r == 2:
                self.generate_r(x, y, x, y - 1)
            elif r == 3:
                self.generate_r(x, y, x, y + 1)

        self.generate_r(x, y, x - 1, y)
        self.generate_r(x, y, x + 1, y)
        self.generate_r(x, y, x, y + 1)
        self.generate_r(x, y, x, y - 1)

    def findNextDir(self, x, y, dir):
        if (dir == Directions.right):
            if (self.canGoUp(x, y)):
                return Directions.up
            if (self.canGoRight(x, y)):
                return Directions.right
            if (self.canGoDown(x, y)):
                return Directions.down
            return Directions.left
        elif (dir == Directions.down):
            if (self.canGoRight(x, y)):
                return Directions.right
            if (self.canGoDown(x, y)):
                return Directions.down
            if (self.canGoLeft(x, y)):
                return Directions.left
            return Directions.up
        elif (dir == Directions.left):
            if (self.canGoDown(x, y)):
                return Directions.down
            if (self.canGoLeft(x, y)):
                return Directions.left
            if (self.canGoUp(x, y)):
                return Directions.up
            return Directions.right
        elif (dir == Directions.up):
            if (self.canGoLeft(x, y)):
                return Directions.left
            if (self.canGoUp(x, y)):
                return Directions.up
            if (self.canGoRight(x, y)):
                return Directions.right
            return Directions.down
        return Directions.none

    def setTourNumber(self, x, y, number):
        if (not self.getPathNumber(x, y) == None):
            return
        self.tourToNumber[x + self.ARENA_WIDTH * y] = number

    def debug_print_maze_path(self):
        for y in range(self.ARENA_HEIGHT):
            a = ""
            for x in range(self.ARENA_WIDTH):
                if self.getPathNumber(x, y) > 10:
                    a = a + " " + str(self.getPathNumber(x, y))
                else:
                    a = a + " " + str(self.getPathNumber(x, y)) + " "
            print(a + "\n")

    def generateTourNumber(self):
        start_x = 0
        start_y = 0
        x = start_x
        y = start_y
        start_dir = Directions.up if self.canGoDown(x, y) else Directions.left
        dir = start_dir
        number = 0
        while (number != self.ARENA_SIZE):
            nextDir = self.findNextDir(x, y, dir)
            if dir == Directions.right:
                self.setTourNumber(x * 2, y * 2, number)
                number = number + 1
                if (nextDir == dir or nextDir == Directions.down or nextDir == Directions.left):
                    self.setTourNumber(x * 2 + 1, y * 2, number)
                    number = number + 1
                if (nextDir == Directions.down or nextDir == Directions.left):
                    self.setTourNumber(x * 2 + 1, y * 2 + 1, number)
                    number = number + 1
                if (nextDir == Directions.left):
                    self.setTourNumber(x * 2, y * 2 + 1, number)
                    number = number + 1
            elif dir == Directions.down:
                self.setTourNumber(x * 2 + 1, y * 2, number)
                number = number + 1
                if nextDir == dir or nextDir == Directions.left or nextDir == Directions.up:
                    self.setTourNumber(x * 2 + 1, y * 2 + 1, number)
                    number = number + 1
                if nextDir == Directions.left or nextDir == Directions.up:
                    self.setTourNumber(x * 2, y * 2 + 1, number)
                    number = number + 1
                if (nextDir == Directions.up):
                    self.setTourNumber(x * 2, y * 2, number)
                    number = number + 1
            elif dir == Directions.left:
                self.setTourNumber(x * 2 + 1, y * 2 + 1, number)
                number = number + 1
                if (nextDir == dir or nextDir == Directions.up or nextDir == Directions.right):
                    self.setTourNumber(x * 2, y * 2 + 1, number)
                    number = number + 1
                if (nextDir == Directions.up or nextDir == Directions.right):
                    self.setTourNumber(x * 2, y * 2, number)
                    number = number + 1
                if (nextDir == Directions.right):
                    self.setTourNumber(x * 2 + 1, y * 2, number)
                    number = number + 1
            elif dir == Directions.up:
                self.setTourNumber(x * 2, y * 2 + 1, number)
                number = number + 1
                if (nextDir == dir or nextDir == Directions.right or nextDir == Directions.down):
                    self.setTourNumber(x * 2, y * 2, number)
                    number = number + 1
                if (nextDir == Directions.right or nextDir == Directions.down):
                    self.setTourNumber(x * 2 + 1, y * 2, number)
                    number = number + 1
                if (nextDir == Directions.down):
                    self.setTourNumber(x * 2 + 1, y * 2 + 1, number)
                    number = number + 1
            dir = nextDir

            if nextDir == Directions.right:
                x += 1
            elif nextDir == Directions.left:
                x -= 1
            if nextDir == Directions.down:
                y += 1
            if nextDir == Directions.up:
                y -= 1


class Directions(Enum):
    up = [-1, 0]
    down = [1, 0]
    left = [0, -1]
    right = [0, 1]
    none = [0, 0]


class Snake:
    def __init__(self, tail):
        # head is first element of tail
        self.tail = tail


class Board:
    def __init__(self, height, width):
        headrow = floor(height / 2)
        headcol = floor(width / 2)
        tail = [[headrow, headcol]]
        self.snake = Snake(tail)
        self.height = height
        self.width = width
        self.board = [[0 for row in range(height)] for col in range(width)]
        self.board[headrow][headcol] = 1
        for point in tail:
            self.board[point[0]][point[1]] = 1
        self.apple = self.generate_apple()

    def move_snake(self, dir):
        row = self.snake.tail[0][0] + dir.value[0]
        col = self.snake.tail[0][1] + dir.value[1]
        if not self.check_colisions(row, col):
            self.snake.tail.insert(0, [row, col])
            if self.board[row][col] == 2:
                if self.generate_apple()[0] == -1:
                    print("You WON !!!")
                    return 1
            else:
                deletedpoint = self.snake.tail.pop()
                self.board[deletedpoint[0]][deletedpoint[1]] = 0
            self.board[row][col] = 1
            return 0
        return -1

    def check_colisions(self, row, col):
        if row > self.height or row < 0:
            return True
        if col > self.width or row < 0:
            return True
        if [row, col] in self.snake.tail:
            return True
        return False

    def find_empty(self):
        emptyspots = []
        for row, sublist in enumerate(self.board):
            for col, value in enumerate(sublist):
                if value == 0:
                    emptyspots.append([row, col])
        return emptyspots

    def generate_apple(self):
        emptyspots = self.find_empty()
        # End game condition
        if len(emptyspots) == 0:
            return -1, -1
        chosenspot = random.choice(emptyspots)
        applerow = chosenspot[0]
        applecol = chosenspot[1]
        self.board[applerow][applecol] = 2
        return applerow, applecol


class Gui:
    BACKGROUND_COLOR = (0, 0, 0)
    SNAKE_COLOR = (255, 255, 255)
    APPLE_COLOR = (255, 0, 0)

    def __init__(self, width, height, board, maze):
        # Create first window
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake")
        self.size = (width, height)
        self.screen = screen
        self.board = board
        self.maze = maze

    def paint_board(self):
        for row in range(self.board.height):
            for col in range(self.board.width):
                if row + self.maze.ARENA_WIDTH * col < self.maze.ARENA_SIZE:
                    self.paint_number(row, col, self.maze.getPathNumber(row, col))
                if (self.board.board[row][col] == 1):
                    self.paint_rectangle(row, col, self.SNAKE_COLOR)
                elif (self.board.board[row][col] == 2):
                    self.paint_rectangle(row, col, self.APPLE_COLOR)

    def paint_rectangle(self, row, col, color):
        width, height = self.size
        rectcol = floor(width / self.board.width * col)
        rectrow = floor(height / self.board.height * row)
        rectwidth = floor(width / self.board.width) - 2
        rectheight = floor(height / self.board.height) - 2
        rect = pygame.Rect(rectcol, rectrow, rectwidth, rectheight)
        pygame.draw.rect(self.screen, color, rect, 1)

    def paint_number(self, row, col, number):
        width, height = self.size
        font = pygame.font.SysFont("ComicSans", height // self.board.height - 4)
        number = font.render(str(number), 1, (255, 255, 255))
        self.screen.blit(number, ((col * (width // self.board.width)) + (width // 4 // self.board.width),
                                  (row * (height // self.board.height)) + (height // 4 // self.board.height)))


class AI():
    def get_next_dir(self, board, maze):
        headrow, headcol = board.snake.tail[0]
        path_number = maze.getPathNumber(headrow, headcol)
        dir_to_zero = Directions.none
        if headrow + 1 + maze.ARENA_WIDTH * headcol < maze.ARENA_SIZE:
            next_path_number = maze.getPathNumber(headrow + 1, headcol)
            if next_path_number == 0:
                dir_to_zero = Directions.down
            if next_path_number - 1 == path_number:
                return Directions.down
        if headrow - 1 + maze.ARENA_WIDTH * headcol < maze.ARENA_SIZE:
            next_path_number = maze.getPathNumber(headrow - 1, headcol)
            if next_path_number == 0:
                dir_to_zero = Directions.up
            if next_path_number - 1 == path_number:
                return Directions.up
        if headrow + maze.ARENA_WIDTH * (headcol + 1) < maze.ARENA_SIZE:
            next_path_number = maze.getPathNumber(headrow, headcol + 1)
            if next_path_number == 0:
                dir_to_zero = Directions.right
            if next_path_number - 1 == path_number:
                return Directions.right
        if headrow + maze.ARENA_WIDTH * (headcol - 1) < maze.ARENA_SIZE:
            next_path_number = maze.getPathNumber(headrow, headcol - 1)
            if next_path_number == 0:
                dir_to_zero = Directions.left
            if next_path_number - 1 == path_number:
                return Directions.left
        if path_number == 99:
            return dir_to_zero
        return Directions.none

    def get_next_dir_upgraded(self, board, maze):
        headrow, headcol = board.snake.tail[0]
        lastrow, lastcol = board.snake.tail[len(board.snake.tail) - 1]
        applerow, applecol = board.apple
        head_path_number = maze.getPathNumber(headrow, headcol)
        apple_path_number = maze.getPathNumber(applerow, applecol)
        last_path_number = maze.getPathNumber(lastrow, lastcol)
        current_dist_to_apple = maze.calc_dist(apple_path_number, head_path_number)
        steps_skipped = 0
        if len(board.snake.tail) < maze.ARENA_SIZE / 2:
            if headrow + 1 + maze.ARENA_WIDTH * headcol < maze.ARENA_SIZE:
                next_path_number = maze.getPathNumber(headrow + 1, headcol)
                if (apple_path_number < last_path_number and apple_path_number < next_path_number) or (apple_path_number > last_path_number and apple_path_number > next_path_number):
                    next_dist_to_apple = maze.calc_dist(apple_path_number, next_path_number)
                    if steps_skipped < current_dist_to_apple - next_dist_to_apple:
                        steps_skipped = current_dist_to_apple - next_dist_to_apple
                        dir = Directions.down
                elif next_path_number == apple_path_number:
                    return Directions.down
            if headrow - 1 + maze.ARENA_WIDTH * headcol < maze.ARENA_SIZE:
                next_path_number = maze.getPathNumber(headrow - 1, headcol)
                if (apple_path_number < last_path_number and apple_path_number < next_path_number) or (apple_path_number > last_path_number and apple_path_number > next_path_number):
                    next_dist_to_apple = maze.calc_dist(apple_path_number, next_path_number)
                    if steps_skipped < current_dist_to_apple - next_dist_to_apple:
                        steps_skipped = current_dist_to_apple - next_dist_to_apple
                        dir = Directions.up
                elif next_path_number == apple_path_number:
                    return Directions.up
            if headrow + maze.ARENA_WIDTH * (headcol + 1) < maze.ARENA_SIZE:
                next_path_number = maze.getPathNumber(headrow, headcol + 1)
                if (apple_path_number < last_path_number and apple_path_number < next_path_number) or (apple_path_number > last_path_number and apple_path_number > next_path_number):
                    next_dist_to_apple = maze.calc_dist(apple_path_number, next_path_number)
                    if steps_skipped < current_dist_to_apple - next_dist_to_apple:
                        steps_skipped = current_dist_to_apple - next_dist_to_apple
                        dir = Directions.right
                elif next_path_number == apple_path_number:
                    return Directions.right
            if headrow + maze.ARENA_WIDTH * (headcol - 1) < maze.ARENA_SIZE:
                next_path_number = maze.getPathNumber(headrow, headcol - 1)
                if (apple_path_number < last_path_number and apple_path_number < next_path_number) or (apple_path_number > last_path_number and apple_path_number > next_path_number):
                    next_dist_to_apple = maze.calc_dist(apple_path_number, next_path_number)
                    if steps_skipped < current_dist_to_apple - next_dist_to_apple:
                        steps_skipped = current_dist_to_apple - next_dist_to_apple
                        dir = Directions.down
                elif next_path_number == apple_path_number:
                    return Directions.down
        else:
            dir = self.get_next_dir()
        return dir


def win_game():
    messagebox.showinfo("Ok", "You won!")
    pygame.quit()


def main():
    maze = Maze()
    maze.generate()
    ai = AI()
    # size of the board (how log can snake be)
    board = Board(maze.ARENA_HEIGHT, maze.ARENA_WIDTH)
    # size of screen in pixels
    gui = Gui(1200, 800, board, maze)
    # game loop termination condition
    running = True
    # lose condition tracker
    lose = False
    # game clock
    clock = pygame.time.Clock()
    # event added to event queue every %time miliseconds
    # this even is used to automove snake
    AUTOMOVEEVENT = pygame.USEREVENT
    time = 250
    pygame.time.set_timer(AUTOMOVEEVENT, time)
    # direction where snake will move on its own
    lastknowndirection = Directions.left
    while (running):
        gui.screen.fill(Gui.BACKGROUND_COLOR)
        gui.paint_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == AUTOMOVEEVENT:
            #   lose = gui.board.move_snake(lastknowndirection)
            # if event.type == pygame.KEYDOWN:
            #   if event.key == pygame.K_UP:
            #      lose = gui.board.move_snake(Directions.up)
            #     lastknowndirection = Directions.up
            # elif event.key == pygame.K_DOWN:
            #   lose = gui.board.move_snake(Directions.down)
            #  lastknowndirection = Directions.down
            # elif event.key == pygame.K_LEFT:
            #   lose = gui.board.move_snake(Directions.left)
            #  lastknowndirection = Directions.left
            # elif event.key == pygame.K_RIGHT:
            #   lose = gui.board.move_snake(Directions.right)
            #  lastknowndirection = Directions.right
            dir = ai.get_next_dir_upgraded(board, maze)
            lose = gui.board.move_snake(dir)
            lastknowndirection = dir

        if lose == -1:
            board = Board(40, 40)
            gui = Gui(1200, 800, board, maze)
            lose = False
            lastknowndirection = Directions.left
        elif lose == 1:
            win_game()
        pygame.display.update()
        # game will run in 60 FPS
        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    main()
