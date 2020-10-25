from copy import deepcopy

class Grid:
    def __init__(self):
        self.size = 64
        self.grid = []
        self.new_empty_grid()

    def update(self, grid_data):
        self.grid[grid_data[1]][grid_data[0]] = grid_data[2]

    def completely_update(self, grid):
        self.grid = deepcopy(grid)

    def new_empty_grid(self):
        self.grid = []
        for i in range(self.size):
            self.grid.append([])
            for j in range(self.size):
                self.grid[i].append((255, 255, 255))

    def get_grid(self):
        return self.grid