import sys
from board import Board
from solver import Solver
from utility import is_square

if len(sys.argv) != 4:
    sys.stderr.write(
        'Error: must be 4 command line argument of the form: \npython n_puzzle.py <board-size> <zero-location-in-solution> <board>\n')
    sys.exit()

if not is_square(int(sys.argv[1])):
    sys.stderr.write('Error: <board-size> argument must be a perfect square\n')
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
    solver = Solver(initial_board)
except Exception as e:
    print(e)
    sys.exit()

solution_metrics = solver.search()

print('Path to goal: ' + str(solution_metrics.path_to_goal))
print('Cost of path: ' + str(solution_metrics.cost_of_path()))
print('Time: ' + str(solution_metrics.search_time))