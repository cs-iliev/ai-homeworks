import math

from copy import deepcopy
from board import Board


class DotsAndBoxes:
    def __init__(self, x, y, depth):
        self.depth = depth
        self.board = Board(x, y)

    def game(self):
        while len(self.board.openVectors) > 0:
            print("Coordinate format == x,y,x2,y2")
            print("Hit 0 and enter to quit")

            self.board.draw()

            success = self.player_move()
            if success is False:
                break

            print("\nPlease wait while your opponent moves...\n")
            self.computer_move()
        self.display_winner()

    def player_move(self):
        while True:
            try:
                integers = input(
                    "Enter the coordinates of the dots you wish to connect:")
                if integers is 0:
                    return False

                coordinates = ((integers[0], integers[1]),
                               (integers[2], integers[3]))

                success = self.board.move(coordinates, 0)

                if success == 0:
                    break
                elif success == -1:
                    print("Invalid coordinates specified!")
            except SyntaxError:
                print("Invalid input, please try again...")
        return True

    def computer_move(self):

        # Create a copy of the current board state for tree calculation
        state = deepcopy(self.board)
        available_moves = deepcopy(self.board.available_moves)

        # Retrieve coordinates from minimax algorithm
        coordinates = self.minimax(state, available_moves, self.depth, True)

        self.board.move(coordinates[1], 1)

    def minimax(self, state, openVectors, depth, max_min):
        '''
        This function contains the core logic regarding the minimax algorithm.
        Parameters:
            state - represents the current board state
            openVectors - represents the available successors from the current state
            ply - represents the total depth of the game tree
            max - a value of True represents the AI, False represents the adversary
        Individual successor states are created in the main loop, before recursively
        calling the minimax algorithm to explore subsequent descendants of the tree.
        '''
        # The value of bestMove defaults to -inf for a Max layer, and +inf for a Min Layer
        if max_min is True:
            bestMove = (-1000000, None)
        else:
            bestMove = (1000000, None)

        # If the ply depth limit is reached or available successors are exhausted,
        # we evaluate and return the value of the current state
        if depth == 0 or len(openVectors) == 0:
            h = self.evaluationFunction(state)
            return (h, None)

        # Get successors
        for i in range(0, len(openVectors)):
            # Retrieve coordinates of current successor state
            move = openVectors.pop()

            # Create a deep copy of the state to be explored
            stateCopy = deepcopy(state)
            openVectorsCopy = deepcopy(openVectors)
            stateCopy.move(move, max_min)

            # Add the coordinates back onto the openVector list, this ensures subsequent
            # child states at the current depth can fully explore the remainder of the tree
            openVectors.appendleft(move)

            # Alpha-Beta Pruning
            # We check the requisite value (beta on a max node, alpha on a min) before
            # exploring the nodes children. If a violation is detected, this path returns.
            h = self.evaluationFunction(stateCopy)
            if max_min is True:
                if h >= stateCopy.beta:
                    return (h, move)
                else:
                    stateCopy.alpha = max(stateCopy.alpha, h)
            else:
                if h <= stateCopy.alpha:
                    return (h, move)
                else:
                    stateCopy.beta = min(stateCopy.beta, h)

            # Make a recursive call to the minimax function with the child state
            # The goal state is back propagated up the tree upon the end of recursion,
            # IE, when ply limit is reached or the open moves are exhausted
            nextMove = self.minimax(
                stateCopy, openVectorsCopy, depth - 1, not max_min)

            # Check the score returned from the child state against the 'bestScore'
            if max_min is True:
                # At a max level, we seek scores higher than the current max
                if nextMove[0] > bestMove[0]:
                    bestMove = (nextMove[0], move)
            else:
                # At a min level, we seek scores lower than the current max
                if nextMove[0] < bestMove[0]:
                    bestMove = (nextMove[0], move)
        return bestMove

    def evaluationFunction(self, state):
        '''
        This an evaluation function which calculates the heuristic value of a given leaf state.
        In this case, h == point total for the AI - point total for the player
        '''
        h = state.computer_score - state.player_score
        return h

    def display_winner(self):
        '''
        This function is called upon the completion, or exit, from the game. A summary containing the scores
        and the winner of the game is printed to the command line.
        '''
        self.board.draw()
        if self.board.player_score > self.board.computer_score:
            print("You won!")
        elif self.board.player_score < self.board.computer_score:
            print("The AI won!")
        else:
            print("The game was a draw")
        print("Player Score: %s" % self.board.player_score)
        print("AI Score: %s" % self.board.computer_score)
        print("\nExiting game...")


integers = input(
    "Please enter the length, width, and (ai)depth of the board (x,y,z): ")
m = integers[0]
n = integers[1]
ply = integers[2]
game = DotsAndBoxes(m, n, ply)
game.playGame()
