from collections import deque
import copy
import heapq as hq
from node import Node
from metrics import Metrics


class Solver:

    def __init__(self, init_board, zero_pos):
        self.n = init_board.n
        self.zero_pos = self.n ** 2 - 1 if zero_pos == -1 else zero_pos
        self.init_state = init_board.state
        self.goal_state = self.set_goal_state(self.zero_pos)
        self.actions = deque()
        self.metrics = Metrics()

        for i, v in enumerate(self.init_state):
            for j, k in enumerate(v):
                if k == 0:
                    self.start_pos = (i, j)
                    break

        self.start_node = Node(self.init_state, None, None, self.start_pos)

    def swap(self, curr_state, pos, direction):
        temp = curr_state[pos[0]][pos[1]]
        curr_state[pos[0]][pos[1]] = curr_state[pos[0] +
                                                direction[0]][pos[1] + direction[1]]
        curr_state[pos[0] + direction[0]][pos[1]+direction[1]] = temp
        return curr_state

    def move(self, curr_state, pos, visited, direction):
        if pos[0] + direction[0] >= len(curr_state) or pos[0] + direction[0] < 0 or pos[1] + direction[1] >= len(curr_state[0]) or pos[1] + direction[1] < 0:
            return None, pos
        if str(self.swap(curr_state, pos, direction)) in visited:
            curr_state = self.swap(curr_state, pos, direction)
            return None, pos

        next_state = copy.deepcopy(curr_state)
        curr_state = self.swap(curr_state, pos, direction)
        return next_state, (pos[0]+direction[0], pos[1]+direction[1])

    def is_solvable(self):
        flattened_list = [i for sublist in self.init_state for i in sublist]
        inv_count = 0
        for i in range(len(flattened_list) - 1):
            for j in range(i+1, len(flattened_list)):
                if flattened_list[i] and flattened_list[j] and flattened_list[i] > flattened_list[j]:
                    inv_count += 1

        if len(self.init_state[0]) % 2:
            return inv_count % 2 == 0
        else:
            x = len(self.init_state) - self.start_pos[0]
            return inv_count % 2 == 0 if x % 2 else inv_count % 2

    def solve(self):
        self.metrics.start_timer()

        if not self.is_solvable():
            raise ValueError('Not solvable')

        move_directions = {
            (0, 1): 'left',
            (1, 0): 'up',
            (-1, 0): 'down',
            (0, -1): 'right'
        }

        visited = set()
        pq = []
        hq.heappush(pq, self.start_node)

        while pq:
            curr_node = hq.heappop(pq)
            if curr_node.state == self.goal_state:
                self.metrics.stop_timer()
                break
            if str(curr_node.state) in visited:
                continue
            visited.add(str(curr_node.state))

            for direction in move_directions.keys():
                next_state, next_pos = self.move(
                    curr_node.state, curr_node.pos, visited, direction)
                if next_state:
                    hq.heappush(pq, Node(next_state, curr_node,
                                move_directions[direction], next_pos))

        while curr_node:
            if curr_node.action:
                self.actions.appendleft(curr_node.action)
            curr_node = curr_node.parent

        self.metrics.path_to_goal = list(self.actions)
        return self.metrics

    def set_goal_state(self, zero_pos):

        goal_state = [['-' for x in range(self.n)]
                      for y in range(self.n)]

        i = 0
        j = 0
        count = 1
        zero_placed = False

        while i < self.n:

            if not zero_placed:
                board_entry = count
            else:
                board_entry = count - 1
            if self.n * i + j == zero_pos:
                board_entry = 0
                zero_placed = True

            goal_state[i][j] = board_entry
            count += 1
            j += 1
            if j == self.n:
                j = 0
                i += 1

        return goal_state
