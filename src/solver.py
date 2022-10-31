import copy
import board
import metrics
import utility


class Solver:

    def __init__(self, input_board):

        self.board = copy.deepcopy(input_board)

        if not self.solvable():
            raise ValueError('Not solvable')

        self.goal_state = self.set_goal_state()

        self.queue = utility.CustomQueue()
        self.pq = utility.CustomPriorityQueue()
        self.explored = utility.CustomStack()

        self.metrics = metrics.Metrics()

    def set_goal_state(self):

        goal_state = [['-' for x in range(self.board.n)]
                      for y in range(self.board.n)]

        i = 0
        j = 0
        count = 1

        while i < self.board.n:
            if count == self.board.n ** 2:
                count = 0
            goal_state[i][j] = count
            count += 1
            j += 1
            if j == self.board.n:
                j = 0
                i += 1

        return goal_state

    def goal_test(self, state):
        if state.state == self.goal_state:
            return True
        else:
            return False

    def expand_nodes(self, starting_board):

        node_order = ['up', 'down', 'left', 'right']

        for node in node_order:

            future_board = board.Board(
                utility.flatten_list(starting_board.state))

            future_board.path_history = copy.copy(
                starting_board.path_history)

            if future_board.move(node):
                future_board.path_history.append(node)

                if future_board not in self.queue and future_board not in self.explored:
                    future_board.score = future_board.manhattan_score(
                        self.goal_state)
                    self.pq.queue.put((future_board.score, future_board))

    def search(self):

        self.metrics.start_timer()

        self.board.score = self.board.manhattan_score(
            self.goal_state)

        self.pq.queue.put((self.board.score, self.board))

        while self.pq.queue:
            lowest_scored = self.pq.queue.get()
            lowest_scored_state = lowest_scored[1]

            self.explored.set.add(lowest_scored_state)

            if self.goal_test(lowest_scored_state):
                self.metrics.path_to_goal = lowest_scored_state.path_history
                self.metrics.stop_timer()
                return self.metrics

            self.expand_nodes(lowest_scored_state)

        raise RuntimeError('Something very wrong occured')

    def solvable(self):
        width = self.board.n

        temp_grid = copy.deepcopy(self.board)

        zero_location = temp_grid.locate_tile(0, temp_grid.state)

        input_list = utility.flatten_list(temp_grid.state)
        input_list = [number for number in input_list if number != 0]

        inversion_count = 0
        list_length = len(input_list)

        for index, value in enumerate(input_list):
            for value_to_compare in input_list[index + 1: list_length]:
                if value > value_to_compare:
                    inversion_count += 1

        if utility.is_even(width):
            zero_odd = not utility.is_even(zero_location[0])

        return (not utility.is_even(width) and utility.is_even(inversion_count)
                or
                (utility.is_even(width) and (zero_odd == utility.is_even(inversion_count))))
