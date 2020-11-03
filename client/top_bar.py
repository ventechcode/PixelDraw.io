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

    def draw(self, win, client):
        bar = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, Colors.WHITE, bar)

        # draw timer
        font = pygame.font.Font('client/assets/fonts/Helvetica-Bold.ttf', 44)
        timer_surface = font.render(str(self.time), True, Colors.BLACK)
        if self.time <= 10:
            timer_surface = font.render(str(self.time), True, (232, 9, 32))
        win.blit(timer_surface, (bar.x + 30, bar.y + bar.height // 2 - timer_surface.get_height() // 2 + 4))

        # draw word & underscores
        if client.drawing or client.guessed:
            text = self.word
            font = pygame.font.Font('client/assets/fonts/Helvetica.ttf', 36)
            text_surface = font.render(text, True, Colors.BLACK)
            win.blit(text_surface, (self.x + self.width // 2 - text_surface.get_width() // 2, self.y + self.height // 2 - text_surface.get_height() // 2 + 4))
        else:
            text = self.underscore_word()
            font = pygame.font.Font('client/assets/fonts/Helvetica-Bold.ttf', 48)
            text_surface = font.render(text, True, Colors.BLACK)
            win.blit(text_surface, (self.x + self.width // 2 - text_surface.get_width() // 2, self.y + self.height // 2 - text_surface.get_height() // 2 - 3))

        # draw round count
        round_font = pygame.font.Font('client/assets/fonts/Helvetica.ttf', 28)
        round_surface = round_font.render(f'Round {self.round}/{self.max_rounds}', True, Colors.BLACK)
        win.blit(round_surface, (self.x + 60 + timer_surface.get_width(), self.y + self.height // 2 - round_surface.get_height() // 2 + 4))

    def underscore_word(self):
        temp = ''
        for char in self.word:
            if char == ' ':
                temp += '  '
            else:
                temp += '_ '
        return temp