import pygame
from colors import Colors
from node import Node

class Grid:
    def __init__(self, x_cells, y_cells, cell_size, x_off, y_off, color=Colors.WHITE):
        self.xCells = x_cells
        self.yCells = y_cells
        self.cellSize = cell_size
        self.xOff = x_off
        self.yOff = y_off
        self.color = color
        self.grid = []
        self.showLines = False

        for i in range(self.xCells):
            self.grid.append([])
            for j in range(self.yCells):
                self.grid[i].append(Node(self.cellSize, self.color))

    def set_color(self, posx, posy, color):
        self.grid[posy][posx].set_color(color)

    def draw(self, win):
        for i in range(self.xCells):
            for j in range(self.yCells):
                self.grid[i][j].draw(win, self.cellSize * i + self.xOff, self.cellSize * j + self.yOff)

    def draw_lines(self, win):
        for i in range(self.xCells):
            for j in range(self.yCells + 1):
                pygame.draw.line(win, Colors.GREY, (self.xOff, self.cellSize * j + self.yOff), (self.cellSize * (i - 1) + self.xOff + 23, self.cellSize * j + self.yOff))
                pygame.draw.line(win, Colors.GREY, (self.cellSize * i + self.xOff, self.yOff), (self.cellSize * i + self.xOff, self.cellSize * j + self.yOff))

    def clear(self):
        self.grid = []
        for i in range(self.xCells):
            self.grid.append([])
            for j in range(self.yCells):
                self.grid[i].append(Node(self.cellSize, self.color))