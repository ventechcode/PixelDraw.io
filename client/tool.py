import pygame
from colors import Colors

class Tool:
    selected = 'brush'
    tools = []

    def __init__(self, name, icon, pos):
        self.name = name
        self.icon = icon
        self.pos = pos
        self.size = (50, 50)
        self.color = Colors.WHITE
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        Tool.tools.append(self)

    def draw(self, win):
        win.blit(self.surface, self.pos)
        win.blit(self.icon, (self.pos[0] + 12, self.pos[1] + 12))

    def hover(self, pos):
        if self.pos[0] < pos[0] < self.pos[0] + self.size[0]:
            if self.pos[1] < pos[1] < self.pos[1] + self.size[1]:
                return True

        return False

    def set_selected(self):
        Tool.selected = self.name