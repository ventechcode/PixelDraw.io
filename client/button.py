import pygame

class Button:
    def __init__(self, color, x, y, width, height, text=None, icon=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.icon = icon

    def draw(self, win, text_color, font, font_size, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x, self.y, self.width, self.height), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text:
            font = pygame.font.Font('client/assets/fonts/' + font + '.ttf', font_size)
            text = font.render(self.text, True, text_color)
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        if self.icon:
            win.blit(self.icon, (self.x + (self.width / 2 - self.icon.get_width() / 2), (self.y + (self.height / 2 - self.icon.get_height() / 2))))

    def hover(self, pos) -> bool:
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False