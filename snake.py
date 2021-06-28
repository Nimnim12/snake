from enum import Enum
from math import floor
import random

import pygame


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
        tail = [[headrow, headcol], [headrow, headcol + 1], [headrow, headcol + 2], [headrow, headcol + 3]]
        self.snake = Snake(tail)
        self.height = height
        self.width = width
        self.board = [[0 for row in range(height)] for col in range(width)]
        self.board[headrow][headcol] = 1
        for point in tail:
            self.board[point[0]][point[1]] = 1
        self.generate_apple()

    def move_snake(self, dir):
        row = self.snake.tail[0][0] + dir.value[0]
        col = self.snake.tail[0][1] + dir.value[1]
        if not self.check_colisions(row, col):
            self.snake.tail.insert(0, [row, col])
            if self.board[row][col] == 2:
                if self.generate_apple():
                    print("You WON !!!")
            else:
                deletedpoint = self.snake.tail.pop()
                self.board[deletedpoint[0]][deletedpoint[1]] = 0
            self.board[row][col] = 1
            return False
        return True

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
        #End game condition
        if len(emptyspots) == 0:
            return True
        chosenspot = random.choice(emptyspots)
        applerow = chosenspot[0]
        applecol = chosenspot[1]
        self.board[applerow][applecol] = 2
        return False


class Gui:
    BACKGROUND_COLOR = (0, 0, 0)
    SNAKE_COLOR = (255, 255, 255)
    APPLE_COLOR = (255, 0, 0)

    def __init__(self, width, height, board):
        # Create first window
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake")
        self.size = (width, height)
        self.screen = screen
        self.board = board

    def paint_board(self):
        for row in range(len(self.board.board)):
            for col in range(len(self.board.board[0])):
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
        pygame.draw.rect(self.screen, color, rect)


def main():
    # size of the board (how log can snake be)
    board = Board(40, 40)
    # size of screen in pixels
    gui = Gui(1200, 800, board)
    # game loop termination condition
    running = True
    # lose condition tracker
    lose = False
    # game clock
    clock = pygame.time.Clock()
    # event added to event queue every %time miliseconds
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
            if event.type == AUTOMOVEEVENT:
                lose = gui.board.move_snake(lastknowndirection)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    lose = gui.board.move_snake(Directions.up)
                    lastknowndirection = Directions.up
                elif event.key == pygame.K_DOWN:
                    lose = gui.board.move_snake(Directions.down)
                    lastknowndirection = Directions.down
                elif event.key == pygame.K_LEFT:
                    lose = gui.board.move_snake(Directions.left)
                    lastknowndirection = Directions.left
                elif event.key == pygame.K_RIGHT:
                    lose = gui.board.move_snake(Directions.right)
                    lastknowndirection = Directions.right

        if (lose):
            board = Board(40, 40)
            gui = Gui(1200, 800, board)
            lose = False
            lastknowndirection = Directions.left
        pygame.display.update()
        # game will run in 60 FPS
        clock.tick(60)


if __name__ == '__main__':
    main()
