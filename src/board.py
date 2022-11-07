import math
import copy


class Board:

    def __init__(self, input_state):
        self.state = copy.deepcopy(self.__list_to_grid(input_state))
        self.n = len(self.state[0])

    def print(self):
        """Print nxn board"""

        for row in self.state:
            for col in row:
                print(col, end=' ')
            print('\n')

    def __list_to_grid(self, tile_list):
        """Take a list of length n^2, return a nxn 2D list"""

        n = int(math.sqrt(len(tile_list)))

        # initialise empty grid
        input_grid = [['-' for x in range(n)] for y in range(n)]

        # populate grid with tiles
        i = 0
        j = 0
        for tile in tile_list:
            input_grid[i][j] = tile
            j += 1
            if j == n:
                j = 0
                i += 1

        return input_grid
