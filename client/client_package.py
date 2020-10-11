class ClientPackage:
    def __init__(self):
        self.uid = ''  # uid of player
        self.ready = False  # is ready
        self.guess = ''  # get player guess (word)
        self.grid_data = ((255, 255, 255), 0, 0)  # get grid info (color, row, col)