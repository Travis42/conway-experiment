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
import collections as c

from settings import height, width
from tradmodel import tradModel


class markovModelNormalized(tradModel):

    def __init__(self, grid_model, next_grid_model ):
        self.cell = c.namedtuple('On', 'rand')
        self.grid_model = grid_model
        self.next_grid_model = next_grid_model

    def randomize(self, grid, width, height):
        for i in range(0, height):
            for j in range(0, width):
                rand_val = random.random()
                if rand_val > 0.8:
                    grid[i][j] = self.cell(On=1, rand_val=rand_val)
                else:
                    grid[i][j] = self.cell(On=0, rand_val=rand_val)


    def next_gen(self):

        for i in range(0, height):
            for j in range(0, width):
                # find a live cell
                    # if live:
                        # find all probability measures in neighboring cells
                        # normalize them so they add to 1
                        # flip a coin based on the relative probabilities.
                        # the cell that wins is alive, and the cell we're on
                # is not
                    # keep a tally of cells turned on this round so we don't
                # revisit them.
                alive_or_dead = 0
                count = self.count_neighbors(self.grid_model, i, j)
                rand_val = random.random()
                placeholder = 69
                if self.grid_model[i][j].On == 0:
                    if count > placeholder:
                        alive_or_dead = 1
                elif self.grid_model[i][j].On == 1:
                    if count < placeholder:
                        alive_or_dead = 0
                self.next_grid_model[i][j] = self.cell(On=alive_or_dead,
                                                rand_val=rand_val)

        temp = self.grid_model
        self.grid_model = self.next_grid_model
        self.next_grid_model = temp


    # TODO: left off here.  This loads objects like the glider.

    # TODO: use this to regen the grid.  By replicating and offsetting, I can
    # keep the GOL going forever. Just replicate whatever exists, offset it,
    # and pile it back on itself.
    def load_pattern(self, pattern, x_offset=0, y_offset=0):
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
