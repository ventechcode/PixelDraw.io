from node import Node

class ColorPalette:
    def __init__(self):
        self.color_palette = [(255, 255, 255), (191, 191, 191), (238, 34, 14),
                              (254, 115, 23), (254, 229, 53), (0, 204, 49),
                              (25, 174, 252), (44, 17, 206), (162, 0, 181),
                              (210, 123, 167), (158, 84, 50), (0, 0, 0),
                              (77, 77, 77), (115, 22, 14), (192, 61, 9),
                              (231, 162, 37), (0, 86, 30), (16, 85, 154),
                              (23, 6, 99), (86, 0, 103), (165, 86, 114),
                              (99, 52, 23)]
        self.selected_color = (0, 0, 0)
        self.color_cells = []
        for color in self.color_palette:
            self.color_cells.append(Node(25, color))
        self.positions = []
        for i in range(0, len(self.color_palette) // 2):
            self.positions.append((440 + i * 25, 90 + (64 * 12) + 25))
        for i in range(0, len(self.color_palette) // 2):
            self.positions.append((440 + i * 25, 90 + (64 * 12) + 50))

    def draw_palette(self, win):
        for i in range(0, len(self.color_cells)):
            win.blit(self.color_cells[i].subsurface, self.positions[i])