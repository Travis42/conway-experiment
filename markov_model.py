#!python
"""
A modification of traditional Game of Life such that each cell has randomly
initiated probabilities.

It's possible to do Markov, but the probabilities need to be normalized
 against each other and stored in a temporary array. Then the central cell
  will make it flip along this weights and the chosen cell will turn on in
  the next round. In this model the probabilities of each cell never change

"""
import random
import collections as c
from tradmodel import tradModel


class markovModelNormalized(tradModel):

    def __init__(self):
        self.cell = c.namedtuple('On', 'rand')

    def randomize(grid, width, height):
        for i in range(0, height):
            for j in range(0, width):
                rand_val = random.random()
                if rand_val > 0.8:
                    grid[i][j] = cell(On=1, rand_val=rand_val)
                else:
                    grid[i][j] = cell(On=0, rand_val=rand_val)


    def next_gen(parameter_count):
        global grid_model, next_grid_model

        for i in range(0, height):
            for j in range(0, width):
                cell = 0
                count = count_neighbors(grid_model, i, j)
                rand_val = random.random()

                if grid_model[i][j].On == 0:
                    if count > parameter_count:
                        cell = 1
                elif grid_model[i][j].On == 1:
                    if count <= parameter_count:
                        cell = 0
                next_grid_model[i][j] = cell(On=cell, rand_val=rand_val)

        temp = grid_model
        grid_model = next_grid_model
        next_grid_model = temp


    # TODO: left off here.

    # TODO: use this to regen the grid.  By replicating and offsetting, I can
    # keep the GOL going forever. Just replicate whatever exists, offset it,
    # and pile it back on itself.
    def load_pattern(pattern, x_offset=0, y_offset=0):
        global grid_model

        # init to clear the grid:
        for i in range(0, height):
            for j in range(0, width):
                grid_model[i][j] = 0

        # this is offsetting by y amount, to apply the pattern wherever you like.
        j = y_offset

        for row in pattern:
            # offset by x amount.
            i = x_offset
            for value in row:
                grid_model[i][j] = value
                i = i + 1
            j = j + 1
