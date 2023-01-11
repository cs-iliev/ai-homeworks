import math

from random import choice


class TicTacToe():
    def __init__(self):
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]
        self.x_player = 1
        self.o_player = -1

    def display_board(self):
        print('---------------')
        switcher = {-1: 'O', 0: ' ', 1: 'X'}
        for x in self.board:
            for y in x:
                ch = switcher[y]
                print(f'| {ch} |', end='')
            print('\n---------------')

    def clear_board(self):
        for x, row in enumerate(self.board):
            for y, col in enumerate(row):
                self.board[x][y] = 0

    def player_won(self, player):
        winning_states = [[self.board[0][0], self.board[0][1], self.board[0][2]],
                          [self.board[1][0], self.board[1][1], self.board[1][2]],
                          [self.board[2][0], self.board[2][1], self.board[2][2]],
                          [self.board[0][0], self.board[1][0], self.board[2][0]],
                          [self.board[0][1], self.board[1][1], self.board[2][1]],
                          [self.board[0][2], self.board[1][2], self.board[2][2]],
                          [self.board[0][0], self.board[1][1], self.board[2][2]],
                          [self.board[0][2], self.board[1][1], self.board[2][0]]]

        if [player, player, player] in winning_states:
            return True

        return False

    def is_game_won(self):
        return self.player_won(self.o_player) or self.player_won(self.x_player)

    def print_game_results(self):
        if self.player_won(self.x_player):
            print('X has won!')
        elif self.player_won(self.o_player):
            print('O has won!')
        else:
            print('Draw' + '\n')

    def empty_cells(self):
        empty = []
        for x, row in enumerate(self.board):
            for y, col in enumerate(row):
                if self.board[x][y] == 0:
                    empty.append([x, y])

        return empty

    def is_board_filled(self):
        if len(self.empty_cells()) == 0:
            return True
        return False

    def make_move(self, x, y, player):
        self.board[x][y] = player

    def player_move(self, player_symbol):
        e = True
        moves = {1: [0, 0], 2: [0, 1], 3: [0, 2],
                 4: [1, 0], 5: [1, 1], 6: [1, 2],
                 7: [2, 0], 8: [2, 1], 9: [2, 2]}
        while e:
            try:
                a, b = list(map(int, input('Pick a position ').split()))
                move = 3 * (a - 1) + b
                if move < 1 or move > 9:
                    print('Invalid location! ')
                elif not (moves[move] in self.empty_cells()):
                    print('Location filled')
                else:
                    self.make_move(
                        moves[move][0], moves[move][1], player_symbol)
                    self.display_board()
                    e = False
            except(KeyError, ValueError):
                print('Please pick a number!')

    def computer_move(self, computer_symbol):
        if len(self.empty_cells()) == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
            self.make_move(x, y, computer_symbol)
        else:
            result = self.mini_max_alpha_beta_pruning(
                len(self.empty_cells()), -math.inf, math.inf, computer_symbol)
            self.make_move(result[0], result[1], computer_symbol)

        self.display_board()

    def get_score(self):
        if self.player_won(self.x_player):
            return 1
        elif self.player_won(self.o_player):
            return -1
        else:
            return 0

    def mini_max_alpha_beta_pruning(self, depth, alpha, beta, player):
        row = -1
        col = -1
        if depth == 0 or self.is_game_won():
            return [row, col, self.get_score()]
        else:
            for cell in self.empty_cells():
                self.make_move(cell[0], cell[1], player)
                score = self.mini_max_alpha_beta_pruning(
                    depth - 1, alpha, beta, -player)
                if player == self.x_player:
                    # X is always the max player
                    if score[2] > alpha:
                        alpha = score[2]
                        row = cell[0]
                        col = cell[1]
                else:
                    if score[2] < beta:
                        beta = score[2]
                        row = cell[0]
                        col = cell[1]

                self.make_move(cell[0], cell[1], 0)

                if alpha >= beta:
                    break

            if player == self.x_player:
                return [row, col, alpha]

            else:
                return [row, col, beta]

    def play(self):
        while True:
            try:
                order = int(
                    input('Would you like to go first or second? (1/2)? '))
                if not (order == 1 or order == 2):
                    print('Please pick 1 or 2')
                else:
                    break
            except(KeyError, ValueError):
                print('Enter a number')

        while True:
            player_symbol = input('Choose symbol? (X/O)? ')
            if player_symbol.capitalize() == 'X':
                human_player = self.x_player
                break
            elif player_symbol.capitalize() == 'O':
                human_player = self.o_player
                break
            else:
                print('Please pick X or O')

        self.clear_board()
        if order == 1:
            current_player = human_player
        else:
            current_player = -human_player

        while not (self.is_board_filled() or self.is_game_won()):
            if current_player == human_player:
                self.player_move(human_player)
            else:
                self.computer_move(-human_player)
            current_player *= -1

        self.print_game_results()


if __name__ == '__main__':
    game = TicTacToe()
    game.play()
