import random

from settings import height, width


class tradModel(object):

    def __init__(self, grid_model, next_grid_model):
        self.grid_model = grid_model
        self.next_grid_model = next_grid_model

    def randomize(self, grid, width, height):
        for i in range(0, height):
            for j in range(0, width):
                grid[i][j] = random.randint(0, 1)

    def next_gen(self):
        for i in range(0, height):
            for j in range(0, width):
                cell = 0
                count = self.count_neighbors(self.grid_model, i, j)

                if self.grid_model[i][j] == 0:
                    if count == 3:
                        cell = 1
                elif self.grid_model[i][j] == 1:
                    if count == 2 or count == 3:
                        cell = 1
                self.next_grid_model[i][j] = cell

        temp = self.grid_model
        self.grid_model = self.next_grid_model
        self.next_grid_model = temp
        return self.grid_model, self.next_grid_model

    def count_neighbors(self, grid, row, col):
        count = 0
        if row - 1 >= 0:
            count = count + grid[row - 1][col]
        if (row - 1 >= 0) and (col - 1 >= 0):
            count = count + grid[row - 1][col - 1]
        if (row - 1 >= 0) and (col + 1 < width):
            count = count + grid[row - 1][col + 1]
        if col - 1 >= 0:
            count = count + grid[row][col - 1]
        if col + 1 < width:
            count = count + grid[row][col + 1]
        if row + 1 < height:
            count = count + grid[row + 1][col]
        if (row + 1 < height) and (col - 1 >= 0):
            count = count + grid[row + 1][col - 1]
        if (row + 1 < height) and (col + 1 < width):
            count = count + grid[row + 1][col + 1]
        return count

    def load_pattern(self, pattern, x_offset=0, y_offset=0):
        # init to clear the grid:
        for i in range(0, height):
            for j in range(0, width):
                self.grid_model[i][j] = 0

        # this is offsetting by y amount, to apply the pattern wherever you
        # like.
        j = y_offset

        for row in pattern:
            # offset by x amount.
            i = x_offset
            for value in row:
                self.grid_model[i][j] = value
                i = i + 1
            j = j + 1

