import pygame
from colors import Colors

class TopBar:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.word = ''
        self.round = 1
        self.max_rounds = 3
        self.time = 90
        self.is_drawing = False

    def draw(self, win):
        bar = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, Colors.WHITE, bar)

        # draw timer
        timer_font = pygame.font.Font('client/assets/fonts/pixelfont.ttf', 44)
        timer_surface = timer_font.render(str(self.time), False, Colors.BLACK)
        if self.time <= 10:
            timer_surface = timer_font.render(str(self.time), False, (232, 9, 32))
        win.blit(timer_surface, (bar.x + 20, bar.y + bar.height // 2 - timer_surface.get_height() // 2 - 1))

        # draw word & underscores
        if self.is_drawing:
            text = self.word
        else:
            text = self.underscore_word()

        text_surface = timer_font.render(text, True, Colors.BLACK)
        win.blit(text_surface, (self.x + self.width // 2 - text_surface.get_width() // 2, self.y + self.height // 2 - text_surface.get_height() // 2))

    def underscore_word(self):
        temp = ''
        for char in self.word:
            if char == ' ':
                temp += '  '
            else:
                temp += '_ '
        return temp