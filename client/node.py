import pygame
from colors import Colors

class Node:
    def __init__(self, size, color=Colors.BLACK):
        self.color = color
        self.size = size
        self.subsurface = pygame.Surface((self.size, self.size))
        self.subsurface.fill(self.color)

    def set_color(self, color):
        self.color = color
        self.subsurface.fill(self.color)

    def draw(self, win, posx, posy):
        win.blit(self.subsurface, (posx, posy))