import math
import sys

from collections import deque
from box import Box


class Board:
    def __init__(self, m, n):
        self.player_score = 0
        self.computer_score = 0
        self.m = m
        self.n = n
        self.boxes = self.generate_boxes(m, n)
        self.available_moves = self.generate_available_moves(m, n)
        self.connected_dots = set()

        self.alpha = math.inf
        self.beta = -math.inf

    def generate_boxes(self, m, n):

        boxes = [[Box(0, 0) for j in range(n)] for i in range(m)]

        for i in range(m):
            for j in range(n):
                boxes[i][j] = (Box(i, j))
        return boxes

    def generate_available_moves(self, m, n):

        lines = deque()

        for i in range(0, m + 1):
            for j in range(0, n):
                lines.append(((j, i), (j + 1, i)))
                if i < m:
                    lines.append(((j, i), (j, i + 1)))
            if i < m:
                lines.append(((n, i), (n, i + 1)))

        return lines

    def draw(self):
        print(f'Human: {self.player_score}')
        print(f'Computer: {self.computer_score}')

        pad = ' '
        axis_x = "\n   "
        for i in range(self.m + 1):
            axis_x = axis_x + f'{i:{pad}{4}}'
        print(axis_x)

        box_value = ' '
        for i in range(self.m + 1):
            horizontal = f'{i:{pad}{3}}'
            vertical = "     "
            for j in range(self.n + 1):
                if ((j - 1, i), (j, i)) in self.connected_dots:
                    horizontal = horizontal + "---*"
                else:
                    horizontal = horizontal + "   *"

                # Check for the box value of a given square based on the top left coordinate
                if j < self.n:
                    if self.boxes[j][i - 1].TopLeft == (j, i - 1):
                        box_value = self.boxes[j][i - 1].value
                else:
                    box_value = " "

                if ((j, i - 1), (j, i)) in self.connected_dots:
                    vertical = vertical + f'| {box_value} '
                else:
                    vertical = vertical + f'  {box_value} '
            print(vertical)
            print(horizontal)
        print("")

    def move(self, coords, player):
        if player is True:
            player = 1
        elif player is False:
            player = 0
        if coords in self.available_moves:
            self.available_moves.remove(coords)
            self.connected_dots.add(coords)
            self.check_boxes(coords, player)
            return 0
        else:
            return -1

    def check_boxes(self, coords, player):

        for i in range(self.m):
            for j in range(self.n):
                box = self.boxes[i][j]
                if coords in box.lines:
                    box.connect_dot(coords)
                if box.complete is True and box.owner is None:
                    box.owner = player
                    self.prevComplete = True
                    # Assign points to whomever completed the box
                    if player == 0:
                        self.playerScore += 1
                        box.value = 'H'
                    elif player == 1:
                        self.aiScore += 1
                        box.value = 'C'
