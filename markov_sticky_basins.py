#!python

#!python
"""
A modification of traditional Game of Life such that each cell has randomly
initiated probabilities.

This is the Markov Model, but if there are two or more neighbors, the cell
stays on, doesn't move.  This should have the effect of aggregating agents
into piles where probability is highest, leading to an end state around
'attractor basins' of a sort.

"""
import random

from markov_model import markovModelNormalized

class markovModelStickyBasins(markovModelNormalized):

    def __init__(self, grid_model, next_grid_model):
        self.grid_model = grid_model
        self.next_grid_model = next_grid_model
        self.alive_count = 0

    def outcome_logic(self, i, j, coordinates, weights):
        if self.alive_count >= 3:
            self.next_grid_model[i][j]['On'] = 1
            return -1, -1
        else:
            next_cell_x, next_cell_y = random.choices(coordinates, weights)[0]
            self.grid_model[i][j]['On'] = 0
            self.next_grid_model[next_cell_x][next_cell_y]['On'] = 1
            return next_cell_x, next_cell_y

    def count_neighbor_probabilities(self, cell_coord):
        row, col = cell_coord
        cell_prob_dict = {}
        neighbor_cells = [(row - 1, col - 0), (row - 1, col - 1),
            (row - 1, col + 1), (row - 0, col - 1), (row - 0, col + 1),
            (row + 1, col + 0), (row + 1, col - 1), (row + 1, col + 1)]
        # adds probability if cell is on the grid and unoccupied
        self.alive_count = 0
        for x, y in neighbor_cells:
            # sticky model is different here:
            try:
                if not self.next_grid_model[x][y]['On']:
                    cell_prob_dict[(x, y)] = self.grid_model[x][y]['rand_val']
                else:
                    self.alive_count += 1
            except IndexError:  # hit edge of the grid
                continue
        return cell_prob_dict
