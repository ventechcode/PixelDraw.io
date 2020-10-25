import uuid
import pygame
from colors import Colors


class Client:

    @staticmethod
    def parse_player(player):
        client = Client(player.name)
        client.uid = player.uid
        client.ready = player.ready
        client.points = player.points
        client.rank = player.rank
        client.drawing = player.drawing
        return client

    def __init__(self, name):
        self.name = name
        self.uid = uuid.uuid4()
        self.ready = False
        self.points = 0
        self.rank = 1
        self.drawing = False

    def draw_lobby_widget(self, win, x, y, yourself):
        if self.ready:
            color = (29, 191, 56)
        else:
            color = (232, 9, 32)
        font = pygame.font.Font('client/assets/fonts/pixelfont.ttf', 22)
        text_surface = font.render(self.name, True, color)
        win.blit(text_surface, (x, y))
        if yourself:
            font = pygame.font.SysFont('arial', 19)
            you_surface = font.render('You', True, Colors.WHITE)
            win.blit(you_surface, (x + text_surface.get_width() + 8, y))

    def draw_game_widget(self, win, x, y, color, yourself):
        rect = pygame.Rect(x, y, 316 - 30, 55, )
        pygame.draw.rect(win, color, rect)

        rank_font = pygame.font.SysFont('arial', 18, True)
        rank_surface = rank_font.render('#' + str(self.rank), True, Colors.BLACK)
        win.blit(rank_surface, (x + 8, y + rect.height // 2 - rank_surface.get_height() // 2))

        name_font = pygame.font.SysFont('arial', 14, True)
        if yourself:
            name_surface = name_font.render(self.name + ' (You)', True, (0, 83, 254))
        else:
            name_surface = name_font.render(self.name, True, Colors.BLACK)
        win.blit(name_surface, (x + rect.width // 2 - name_surface.get_width() // 2, y + 10))

        points_font = pygame.font.SysFont('arial', 14, False)
        points_surface = points_font.render('Points: ' + str(self.points), True, Colors.BLACK)
        win.blit(points_surface, (x + rect.width // 2 - points_surface.get_width() // 2, y + 28))
