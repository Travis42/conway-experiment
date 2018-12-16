#!python
"""
A modification of traditional Game of Life such that each cell has randomly
initiated probabilities.

It's possible to do Markov, but the probabilities need to be normalized
 against each other and stored in a temporary array. Then the central cell
  will make it flip along this weights and the chosen cell will turn on in
  the next round. In this model the probabilities of each cell never change,
  and the cell that is 'alive' or 'dead' must be initialized up front.  In
  other words, there are only ever n agents in the simulation at one time,
  moving from cell to cell.

"""
import random
import sys

from settings import height, width
from tradmodel import tradModel


class markovModelNormalized(tradModel):

    def __init__(self, grid_model, next_grid_model):
        self.grid_model = grid_model
        self.next_grid_model = next_grid_model

    def randomize(self, grid, width, height):
        for i in range(0, height):
            for j in range(0, width):
                rand_val = random.random()
                if rand_val > 0.9:
                    grid[i][j] = {'On': 1, 'rand_val': rand_val}
                else:
                    grid[i][j] = {'On': 0, 'rand_val': rand_val}
        self.grid_model = grid

    #TODO: color each cell in a gradient based on its probability, so that I
    # can see where high probabilty 'basins' lie.
    #TODO: fix cell merge, if desired.

    def next_gen(self):
        alive_cells = []
        for i in range(0, height):
            for j in range(0, width):
                if self.grid_model[i][j]['On'] == 1 and (i, j) not in \
                        alive_cells:
                    # ex. {(x, y): 0.50}
                    probabilities = self.count_neighbor_probabilities((i, j))
                    # scrubbing options that are off the grid:
                    probabilities = {k:v for k, v in probabilities.items()
                                     if (k[0] >= 0 and k[0] <= width) and
                                     (k[1] >= 0 and k[1] <= height)}
                    cell_probabilities_totaled = sum(v for v in
                                                     probabilities.values())
                    coords_w_normalized_weights = {k: v /
                                                   cell_probabilities_totaled
                                                   for k, v in probabilities.items()}
                    coordinates = list(coords_w_normalized_weights.keys())
                    weights = list(coords_w_normalized_weights.values())
                    next_cell_x, next_cell_y = random.choices(coordinates,
                                                              weights)[0]

                    self.grid_model[i][j]['On'] = 0
                    self.next_grid_model[next_cell_x][next_cell_y]['On'] = 1
                    alive_cells.append((next_cell_x, next_cell_y))
        temp = self.grid_model
        self.grid_model = self.next_grid_model
        self.next_grid_model = temp

    def count_neighbor_probabilities(self, cell_coord):
        row, col = cell_coord
        cell_prob_dict = {}
        neighbor_cells = [
            (row - 1, col - 0),
            (row - 1, col - 1),
            (row - 1, col + 1),
            (row - 0, col - 1),
            (row - 0, col + 1),
            (row + 1, col + 0),
            (row + 1, col - 1),
            (row + 1, col + 1)
        ]
        for i in neighbor_cells:
            try:
                cell_prob_dict[i] = self.grid_model[i[0]][i[1]]['rand_val']
            except IndexError:  # hit edge of the grid
                continue
        return cell_prob_dict

    def load_pattern(self, pattern, x_offset=0, y_offset=0):
        global grid_model

        # init to clear the grid:
        for i in range(0, height):
            for j in range(0, width):
                rand_val = random.random()
                grid_model[i][j] = self.cell(On=0, rand_val=rand_val)

        # this is offsetting by y amount, to apply the pattern wherever you
        # like.
        j = y_offset

        for row in pattern:
            # offset by x amount.
            i = x_offset
            for value in row:
                rand_val = random.random()
                grid_model[i][j] = self.cell(On=value, rand_val=rand_val)
                i = i + 1
            j = j + 1
