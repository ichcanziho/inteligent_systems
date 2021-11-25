# -*- coding: utf-8 -*-
"""In-class activity (11-Oct-2021) - Template.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pxSCkXRn_QF5ejCyoSDs-BWSScXxpdmR
"""

# Libraries
# =======================
import random
import math


# Neigbor generator
# =======================
# Receives a board and generates a neighbor. The neighbor is generated by swapping
# two randomly chosen numbers on the board.
def neighbor(board):
    # REPLACE with the actual code to generate the neighbor
    newBoard = board.copy()
    index_a = random.randint(0, 8)
    index_b = random.randint(0, 8)
    newBoard[index_a], newBoard[index_b] = newBoard[index_b], newBoard[index_a]
    return newBoard


# Objective (cost) function (version 1)
# =======================
# Receives a board and returns a numeric value to estimate its cost. This function
# will sum the number of rows, columns and diagonals that do not sum up 15. In 
# this way, the solution has a cost of zero, and the worst possible solution has
# a cost of eight.
def f1(board):
    # REPLACE with the actual code to calculate the cost according to version 1 of
    # the cost function
    cost = 8
    one = sum(int(i) for i in board[0:3])
    sec = sum(int(i) for i in board[3:6])
    thi = sum(int(i) for i in board[6:9])
    fou = board[0] + board[3] + board[6]
    fif = board[1] + board[4] + board[7]
    six = board[2] + board[5] + board[8]
    sev = board[0] + board[4] + board[8]
    oct = board[2] + board[4] + board[6]
    l = [one, sec, thi, fou, fif, six, sev, oct]
    for el in l:
        if el == 15: cost -= 1
    return cost


# Objective (cost) function (version 2)
# =======================
# Receives a board and returns a numeric value to estimate its cost. This function
# will sum the difference between 15 and the sum of each row, column and diagonal.
def f2(board):
    # REPLACE with the actual code to calculate the cost according to version 2 of
    # the cost function
    cost = 0
    one = sum(int(i) for i in board[0:3])
    sec = sum(int(i) for i in board[3:6])
    thi = sum(int(i) for i in board[6:9])
    fou = board[0] + board[3] + board[6]
    fif = board[1] + board[4] + board[7]
    six = board[2] + board[5] + board[8]
    sev = board[0] + board[4] + board[8]
    oct = board[2] + board[4] + board[6]
    l = [one, sec, thi, fou, fif, six, sev, oct]
    for el in l:
        cost += abs(15 - el)
    return cost


# Local search
# =======================
# Implements local search for a minimization problem (the rationale is to
# minimize the errors on the board).
def localSearch(f, iterations):
    # Creates a random board (a permutation of the nine numbers on the board)
    x = list(range(1, 10))
    random.shuffle(x)
    # Iterates to optimize the best solution found
    for i in range(iterations):
        # Generates a neigbor of x
        y = neighbor(x)
        # If the cost of y is smaller than the cost of x, we replace x with y
        if (f(y) < f(x)):
            x = y
    # Returns the best solution found
    return x


# Simulated annealing
# =======================
# Implements simulated annealing for a minimization problem (the rationale is to
# minimize the errors on the board).
def simulatedAnnealing(f, iterations, t):
    # Creates a random board (a permutation of the nine numbers on the board)
    x = list(range(1, 10))
    random.shuffle(x)
    best = x
    # Iterates to optimize the best solution found
    for i in range(iterations):
        # Generates a neigbor of x
        y = neighbor(x)
        # If the cost of y is smaller than the cost of x, we replace x with y
        if (f(y) < f(x)):
            x = y
            if (f(x) < f(best)):
                best = x
        else:
            delta = f(x) - f(y)
            if (random.random() < math.exp(delta / t)):
                x = y
        t = t * 0.98
    # Returns the best solution found
    return best


# Parameters for the tests
# =======================
# Do not change these parameters (trials and iterations)
trials = 100
iterations = 1000
# Set the seed to your preferred value
random.seed(12345)

# Evaluates the performance of local search when version 1 of the cost function
# is used
# =======================
# Estimates the success rate of local search when version 1 of the cost function
# is used
success = 0
for i in range(iterations):
    best = localSearch(f1, iterations)
    if f1(best) == 0:
        success = success + 1
success = success / iterations
print("Success rate of local search with version 1 of the cost function: " + str(success))

# Evaluates the performance of local search when version 2 of the cost function
# is used
# =======================
# Estimates the success rate of local search when version 2 of the cost function
# is used
success = 0
for i in range(iterations):
    best = localSearch(f2, iterations)
    if (f2(best) == 0):
        success = success + 1
success = success / iterations
print("Success rate of local search with version 2 of the cost function: " + str(success))

# Evaluates the performance of simulated annealing when version 2 of the cost
# function is used
# =======================
# Estimates the success rate of simulated annealing when version 2 of the cost 
# function is used
success = 0
for i in range(iterations):
    best = simulatedAnnealing(f2, iterations, 1000)
    if (f2(best) == 0):
        success = success + 1
success = success / iterations
print("Success rate of simulated annealing with version 2 of the cost function: " + str(success))
