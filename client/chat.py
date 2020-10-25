import pygame


class Chat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 285
        self.height = 767
        self.messages = []
        self.message = ''
        self.font = pygame.font.Font('client/assets/fonts/Helvetica.ttf', 15)
        self.chat_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.input_rect = pygame.Rect(self.x + 2, self.y + self.height - 52 + 1, 282, 50)
        self.message_surface = pygame.Surface((282, 31))
        self.hint_text = 'Type your guess here...'
        self.input_active = False

    def draw(self, win):
        pygame.draw.rect(win, (128, 128, 128), self.chat_rect, 2)  # chat border
        surface = pygame.Surface((self.width - 3, self.height - 52 - 2))  # chat surface
        surface.fill((255, 255, 255))
        win.blit(surface, (self.x + 2, self.y + 2))
        pygame.draw.line(win, (128, 128, 128), (self.x + 2, self.y + self.height - 52), (self.x + self.width - 2, self.y + self.height - 52), 1)  # separator
        if not self.input_active:
            pygame.draw.rect(win, (255, 255, 255), self.input_rect)  # inactive input field
        else:
            pygame.draw.rect(win, (200, 200, 200), self.input_rect)  # active input field

        if not self.input_active and not len(self.message) > 0:
            hint_font = pygame.font.Font('client/assets/fonts/Helvetica.ttf', 20)
            text = hint_font.render(self.hint_text, True, (153, 153, 166))
            win.blit(text, (self.x + 12, self.y + self.height - 52 // 2 - text.get_height() // 2 + 2))

        if len(self.messages) * self.message_surface.get_height() > self.height - 52:  # remove top message if chat is full
            self.messages = self.messages[1:]

        for i, message in enumerate(self.messages):  # draw chat messages
            if i % 2 == 0:
                self.message_surface.fill((255, 255, 255))
                win.blit(self.message_surface, (self.x + 2, self.y + 2 + i * self.message_surface.get_height()))
                text = self.font.render(message, True, (0, 0, 0))
                win.blit(text, (self.x + 8, self.y + 11 + i * self.message_surface.get_height()))
            else:
                self.message_surface.fill((238, 238, 238))
                win.blit(self.message_surface, (self.x + 2, self.y + 2 + i * self.message_surface.get_height()))
                text = self.font.render(message, True, (0, 0, 0))
                win.blit(text, (self.x + 8, self.y + 11 + i * self.message_surface.get_height()))
        try:
            msg_font = pygame.font.Font('client/assets/fonts/Helvetica.ttf', 18)
            msg = msg_font.render(self.message, True, (0, 0, 0))
            win.blit(msg, (self.x + 12, self.y + self.height - 52 // 2 - msg.get_height() // 2 + 2))
        except pygame.error:
            pass

    def input_hover(self, pos):
        if self.input_rect.collidepoint(pos[0], pos[1]):
            return True
        return False

    def update(self, messages):
        self.messages = []
        for msg in messages:
            self.messages.append(msg)