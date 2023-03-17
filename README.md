# Robot-Navigation
DFS and BFS Algorithm Implementation
The program read a world description from standard input with a form like:


4
3
@*__
__#*
__*#

Inputs all have the format:
1. The first line is the number of columns
2. The second line is the number of rows
3. The remaining lines are a description of the Sample World with the representation: @ is the starting
location of the robot, # is a blocked cell, * is a sample location, is a blank cell.
Assume that all inputs are correctly formatted and solvable.
In addition to the world description input, the program  accept one command-line argument:
algorithm: one of dfs (depth-first search with cycle detection) or ucs (uniform cost search).
Not every world can be solved in a reasonable amount of time with every algorithm.

Actions
The robot can perform one of five actions from any given state: moving in one of the four cardinal directions
or sampling its current location. It cannot move into a blocked cell or move off the board, and it can only
perform a sample action if it is on a cell that was marked to sample. It cannot sample the same cell twice.

The program only output the list of actions followed by two algorithm statistics:
Action list: A sequence of movements (U, D, L, R) and sample actions (S)
Statistics: The number of nodes that the algorithm generated and expanded, on separate lines
Example output for small2 world (the nodes generated/expanded may not match exactly):
R
U
U
R
R
D
D
S
24 nodes generated
10 nodes expanded
