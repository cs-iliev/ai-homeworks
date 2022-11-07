class Node:

    def __init__(self, curr_state, parent, action, pos):
        self.state = curr_state
        self.parent = parent
        self.action = action
        self.pos = pos
        self.path_cost = parent.path_cost + 1 if parent != None else 0
        self.manhattan_distance = self.get_manhattan_distance()

    def __lt__(self, other):
        return self.path_cost + self.manhattan_distance < other.path_cost + other.manhattan_distance

    def get_manhattan_distance(self):
        distance = 0

        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                if self.state[i][j] != 0:
                    x, y = divmod(self.state[i][j] - 1, len(self.state[0]))
                    distance += abs(x - i) + abs(y - j)

        return distance
