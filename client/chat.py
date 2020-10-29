import pygame


class Chat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 285
        self.height = 767
        self.messages = []
        self.message = ''
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
            font_size = 15  # font size for default messages
            msg_color = (0, 0, 0)  # black for default messages
            if message.startswith('SUCCESS'):
                message = message[7:]
                msg_color = (86, 206, 128)
                font_size = 16
            if message.startswith('INFO'):
                message = message[4:]
                msg_color = (57, 117, 206)
                font_size = 16
            if message.startswith('ERROR'):
                message = message[5:]
                msg_color = (206, 79, 10)
                font_size = 16
            if message.startswith('WARNING'):
                message = message[7:]
                msg_color = (204, 204, 0)
                font_size = 16
            if message.startswith('INVISIBLE'):
                message = message[9:]
                msg_color = (162, 173, 142)

            font = pygame.font.Font('client/assets/fonts/Helvetica.ttf', font_size)

            if i % 2 == 0:
                self.message_surface.fill((255, 255, 255))
                win.blit(self.message_surface, (self.x + 2, self.y + 2 + i * self.message_surface.get_height()))
                text = font.render(message, True, msg_color)
                win.blit(text, (self.x + 8, self.y + 11 + i * self.message_surface.get_height()))
            else:
                self.message_surface.fill((238, 238, 238))
                win.blit(self.message_surface, (self.x + 2, self.y + 2 + i * self.message_surface.get_height()))
                text = font.render(message, True, msg_color)
                win.blit(text, (self.x + 8, self.y + 11 + i * self.message_surface.get_height()))

        try:
            typing_font = pygame.font.Font('client/assets/fonts/Helvetica.ttf', 18)
            msg = typing_font.render(self.message, True, (0, 0, 0))
            win.blit(msg, (self.x + 12, self.y + self.height - 52 // 2 - msg.get_height() // 2 + 2))
        except pygame.error:
            pass

    def input_hover(self, pos):
        if self.input_rect.collidepoint(pos[0], pos[1]):
            return True
        return False

    def update(self, messages, client):
        self.messages = []
        for msg in messages:
            if msg.startswith('INVISIBLE') and not client.guessed and not client.drawing:  # filter invisible messages
                pass
            else:
                self.messages.append(msg)