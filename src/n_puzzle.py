import sys
from utility import *
from board import Board
from solver import Solver

if len(sys.argv) != 4:
    sys.stderr.write(
        'Error: must be 4 command line argument of the form: \npython n_puzzle.py <board-size> <zero-position-in-solution> <board>\n')
    sys.exit()

if not is_square(int(sys.argv[1])):
    sys.stderr.write('Error: <board-size> argument must be a perfect square\n')
    sys.exit()

zero_pos = int(sys.argv[2])

if int(zero_pos < -1 or zero_pos >= int(sys.argv[1]) ** 2):
    sys.stderr.write(
        'Error: <zero-position-in-solution> argument must between 0 and N - 1 where N is the board size or -1 for default\n')
    sys.exit()

input_list = sys.argv[3].split(',')
input_list = list(map(int, input_list))

if len(input_list) != int(sys.argv[1]):
    sys.stderr.write("Error: input grid must match <board-size>\n")
    sys.exit()

ordered_list = sorted(input_list)
for index, number in enumerate(ordered_list):
    if number != index:
        sys.stderr.write(
            "Error: input list must contain all numbers from 0 to n^2 - 1\n")

initial_board = Board(input_list)

try:
    solver = Solver(initial_board, zero_pos)
except Exception as e:
    print(e)
    sys.exit()

ans = solver.solve()

print(list(ans))

print(solver.metrics.search_time)
