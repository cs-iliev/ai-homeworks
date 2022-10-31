import math
import copy


class Board:

    def __init__(self, input_state):
        self.state = copy.deepcopy(self.__list_to_grid(input_state))
        self.path_history = []
        self.n = len(self.state[0])
        self.score = 0

    def move(self, direction):
        """Slide tile in one of the 4 directions"""

        zero_coords = self.locate_tile(0, self.state)

        if direction == 'up':
            y, x = 1, 0
        elif direction == 'down':
            y, x = -1, 0
        elif direction == 'left':
            y, x = 0, 1
        elif direction == 'right':
            y, x = 0, -1
        else:
            raise ValueError(
                'Invalid direction: must be \'up\', \'down\', \'left\' or \'right\'')

        # move not possible
        if zero_coords[0] + y not in range(0, self.n):
            return False
        if zero_coords[1] + x not in range(0, self.n):
            return False

        # move tiles
        tile_to_move = self.state[zero_coords[0] + y][zero_coords[1] + x]
        self.state[zero_coords[0]][zero_coords[1]] = tile_to_move
        self.state[zero_coords[0] + y][zero_coords[1] + x] = 0

        return True

    def locate_tile(self, tile, board_state):
        """Return coordinates of a given tile as a tuple"""

        for(y, row) in enumerate(board_state):
            for(x, value) in enumerate(row):
                if value == tile:
                    return (y, x)

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

    def manhattan_score(self, goal_state):
        sum = 0
        for (y, row) in enumerate(self.state):
            for (x, tile) in enumerate(row):
                if tile == 0:
                    continue
                sum += self.manhattan_distance(tile, (y, x), goal_state)

        return sum

    def manhattan_distance(self, tile, tile_position, goal_state):
        goal_position = self.locate_tile(tile, goal_state)

        distance = (abs(goal_position[0] - tile_position[0])
                    + abs(goal_position[1] - tile_position[1]))

        return distance

    def __gt__(self, other):
        return self.score > other.score

    def __eq__(self, other):
        return self.score == other.score

    def __hash__(self):
        return hash(self.score)
