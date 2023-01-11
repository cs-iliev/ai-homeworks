# n-puzzle

N puzzle solver developed for the Intelligent Systems course

USEAGE
--------

In the command line:
$ python n_puzzle.py [board-size] [zero-pos-in-solution] [input-list]

where [board-size] is a perfect square
where [zero-pos-in-solution] is between 0 and N - 1 where N is the board size or -1 for default
where [input-list] contains all numbers from 0 to n^2 - 1

eg.
$ python n_puzzle.py 9 -1 3,5,0,1,8,6,4,2,7

represents the puzzle
3 5 0
1 8 6
4 2 7
where 0 is the blank space

RETURNS
----------

cost_of_path
path_to_goal
running_time

or

'Not solvable'
