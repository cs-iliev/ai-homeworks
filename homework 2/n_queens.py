import random
import time
import sys


class NQueens:

    def __init__(self, n):
        self.n = n
        self.board = []
        self.row_conflicts = []
        self.right_diag_conflicts = []
        self.left_diag_conflicts = []

    def change_conflicts(self, col, row, val):
        """val indicates the number of conflicts to add or subtract from the given row/diag"""

        self.row_conflicts[row] += val
        self.right_diag_conflicts[col + row] += val
        self.left_diag_conflicts[col + (self.n - row - 1)] += val

    def min_conflict_pos(self, col):
        """for a given col get a row with least ammount of conflicts"""
        min_conflicts = self.n
        min_conflict_rows = []
        for row in range(self.n):

            conflicts = self.row_conflicts[row] + self.right_diag_conflicts[col +
                                                                            row] + self.left_diag_conflicts[col + (self.n - row - 1)]
            if conflicts == 0:
                return row

            # update min value
            if conflicts < min_conflicts:
                min_conflict_rows = [row]
                min_conflicts = conflicts

            # if conflict count is equal to current min just appent to list
            elif conflicts == min_conflicts:
                min_conflict_rows.append(row)

        # select random row with minumum conflicts
        choice = random.choice(min_conflict_rows)
        return choice

    def create_board(self):
        """Setup board with a random starting state"""

        self.board = []

        self.right_diag_conflicts = [0] * ((2 * self.n) - 1)
        self.left_diag_conflicts = [0] * ((2 * self.n) - 1)
        self.row_conflicts = [0] * self.n

        row_set = set(range(0, self.n))

        for col in range(0, self.n):
            # place queen on a random free row
            self.board.append(row_set.pop())
            # update conflict lists
            self.change_conflicts(col, self.board[col], 1)

    def find_max_conflict_col(self):
        conflicts = 0
        max_conflicts = 0
        max_conflict_cols = []

        for col in range(0, self.n):
            row = self.board[col]
            conflicts = self.row_conflicts[row] + self.right_diag_conflicts[col +
                                                                            row] + self.left_diag_conflicts[col+(self.n-row-1)]
            # update max
            if (conflicts > max_conflicts):
                max_conflict_cols = [col]
                max_conflicts = conflicts

            # else append to current list of maximums
            elif conflicts == max_conflicts:
                max_conflict_cols.append(col)

        # select random col with max conflicts
        choice = random.choice(max_conflict_cols)
        return choice, max_conflicts

    def solve(self):
        self.create_board()
        iteration = 0
        # define max iteration before termination
        max_iteration = 8 * self.n

        while (iteration < max_iteration):
            # calculate column with max conflicts and how many conflicts it contains
            col, num_conflicts = self.find_max_conflict_col()

            if (num_conflicts > 3):
                # search for row with min conflicts
                newLocation = self.min_conflict_pos(col)

                # if better location is a new location, switch it
                if (newLocation != self.board[col]):
                    # reduce number of conflicts where queen is leaving
                    self.change_conflicts(col, self.board[col], -1)
                    self.board[col] = newLocation
                    # increment conflicts where queen is entering
                    self.change_conflicts(col, newLocation, 1)
            # number of conflicts equal to 3 means the queen is alone on the given row/col/diag
            elif num_conflicts == 3:
                # solution found
                return True
            iteration += 1
        # if no solution is found by this point return false
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Expected 2 arguments")
        sys.exit()

    dimension = int(sys.argv[1])

    if dimension <= 3 or dimension > 10000000:
        print("Cannot build board of size: " + str(dimension))
        sys.exit()

    sol = NQueens(dimension)
    start_time = time.time()
    solved = False

    # keep calling function until a solution is found
    while (not solved):
        solved = sol.solve()

    end_time = time.time()

    print("Board configuration found for size " + str(dimension))

    total_time = "{0:.5f} ms".format(
        (end_time - start_time) * 1000)

    print(sol.board)
    print("Time taken: " + total_time + " ms\n")
