# Adversarial-Search
Minimax algorithm using alpha-beta pruning on Reversi game

The rules of the Reversi game can be found at http://en.wikipedia.org/wiki/Reversi and
interactive examples can be found at http://www.samsoft.org.uk/reversi/.

The program takes the input from the file input.txt, and print out its output to the file
output.txt. Each input of the program contains a game position (including the board
state and the player to move) and a search cut-off depth D.

Evaluation function: positional weights
In this evaluation function, each cell i of the board has a certain strategic value Wi.

Ties between the legal moves are broken by handling the moves in positional order that is, first favor cells in upper rows, and in the
same row favoring cells in the left side. The map of the cell values is given below:

evalMatrix = [[99,-8,8,6,6,8,-8,99],[-8,-24,-4,-3,-3,-4,-24,-8],[8,-4,7,4,4,7,-4,8],[6,-3,4,0,0,4,-3,6],[6,-3,4,0,0,4,-3,6],[8,-4,7,4,4,7,-4,8],[-8,-24,-4,-3,-3,-4,-24,-8],[99,-8,8,6,6,8,-8,99]]

File Formats

Input format:
<player to move>
<search cut-off depth>
<current board status>
where the board status is denoted by * as blank cell, X as black piece, and O as white piece.

Output format:
<next state>
<traverse log>
where the traverse log requires 5 columns. Each column is separated by “,”. The five
columns are node, depth, minimax value, alpha, beta.

Example Test Case
As an example, the following input instance asks to compute a depth-2 alpha-beta search
from the starting game position:
X
2
********
********
********
***OX***
***XO***
********
********
********
and the corresponding output should be:
********
********
***X****
***XX***
***XO***
********
********
********
Node,Depth,Value,Alpha,Beta
root,0,-Infinity,-Infinity,Infinity
d3,1,Infinity,-Infinity,Infinity
c3,2,-3,-Infinity,Infinity
d3,1,-3,-Infinity,-3
e3,2,0,-Infinity,-3
d3,1,-3,-Infinity,-3
c5,2,0.0,-Infinity,-3
d3,1,-3,-Infinity,-3
root,0,-3,-3,Infinity
c4,1,Infinity,-3,Infinity
c3,2,-3,-3,Infinity
c4,1,-3,-3,-3
root,0,-3,-3,Infinity
f5,1,Infinity,-3,Infinity
f4,2,0,-3,Infinity
f5,1,0,-3,0
d6,2,0,-3,0
f5,1,0,-3,0
f6,2,-3,-3,0
f5,1,-3,-3,-3
root,0,-3,-3,Infinity
e6,1,Infinity,-3,Infinity
f4,2,0,-3,Infinity
e6,1,0,-3,0
d6,2,0,-3,0
e6,1,0,-3,0
f6,2,-3,-3,0
e6,1,-3,-3,-3
root,0,-3,-3,Infinity
