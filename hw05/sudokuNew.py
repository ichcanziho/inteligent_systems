
import csv
from queue import PriorityQueue
import numpy as np
from copy import deepcopy
import time
        
def getBoardPriority(grid): 
    board_priority = [[0 for j in range(9)] for i in range(9)]
    for ys in range(9):
        for xs in range(9):
            value = grid[ys][xs]
            if value == 0:
                priority, _ = get_cell_priority(grid,ys, xs)
                board_priority[ys][xs] = priority
            else:
                board_priority[ys][xs] = 0
    return board_priority

def get_cell_priority(board, y, x):

            # get the row vector
            row = [board[y][i] for i in range(9)]
    
            # get the column vector
            column = [board[i][x] for i in range(9)]
    
            x_quad = int(x / 3)
            y_quad = int(y / 3)
    
            # get the quadrant vector
            quadrant = list()
            for i in range(3):
                nx = i + (x_quad * 3)
                for j in range(3):
                    ny = j + (y_quad * 3)
                    quadrant.append(board[ny][nx])
    
            alls = set(range(10))
            frees = set(row) | set(column) | set(quadrant)
            frees = alls - frees
    
            return len(frees), frees
        
class Solver(object):
   
    def __init__(self, initial_board):
        self.start = initial_board
        self.visited_set = set()
        self.queue = PriorityQueue()
    

    def solve(self):
        puzzle_state = self.start
   
        puzzle_state.fill_zeroes()

        dist = puzzle_state.get_dist_to_goal()
        self.queue.put((dist, puzzle_state))
        
        while not puzzle_state.is_complete() and self.queue.qsize():
            puzzle_state = self.queue.get()[1]
            puzzle_hash = str(puzzle_state)
            self.visited_set.add(puzzle_hash)
                
            for c in puzzle_state.create_children():
                if str(c) not in self.visited_set:
                    dist = c.get_dist_to_goal()
                    for e in self.queue.queue:
                        if dist == e[0]: 
                            dist = dist + 1
                    self.queue.put((dist, c))

        return puzzle_state
        
class BoardState(object):
    """
    Describes a single instance of the game board. Underlying data structure
    is a 2D array.
    """
    
    def __init__(self, csv_dir):
        self.board = []
        with open(csv_dir, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            for row in reader:
                self.board.append([int(val) for val in row])

    def get_dist_to_goal(self):
        """
        The goal of this function is to establish a quantitative measure of 
        distance from the (solved) end-state. Currently uses a naive count of
        the number of filled-in cells on the board.
        """
        bool_map = [map(bool, row) for row in self.board]
        return sum([sum(r) for r in bool_map])
        
    def is_complete(self):
        return self.get_dist_to_goal() == 0 

    def get_scored_next_steps(self):
        scored_steps = PriorityQueue() 
        for ys in range(9):
            for xs in range(9):
                value = self.board[ys][xs]
                if value == 0:
                    priority, values = get_cell_priority(self.board, ys, xs)
                    scored_steps.put((priority, ys, xs, values))
                    
        return scored_steps            
                    
    def fill_zeroes(self):
        for ys in range(9):
            for xs in range(9):
                value = self.board[ys][xs]
                if value == 0:
                    priority, _ = get_cell_priority(self.board,ys, xs)
                    if priority == 1:
                        self.board[ys][xs] = list(_)[0]
                        
        arr = np.array(getBoardPriority(self.board))
        n_ones = np.count_nonzero(arr == 1)
        if n_ones == 0:
            #print(np.matrix(arr))
            return 
        else:
            self.fill_zeroes()     
           
    def create_children(self):

        next_steps = self.get_scored_next_steps()
        if next_steps.qsize():
            pc, row, col, choices = self.get_scored_next_steps().get()
            children = []
            for val in choices:
                child = deepcopy(self)
                child.board[row][col] = val
                child.fill_zeroes()
                children.append(child)
            return children
        else:
            return []
    
    def pretty_print(self):
        int2str = lambda s: str(s).replace('0', ' ')
        rows = [','.join(map(int2str, row)) for row in self.board]
        print ('\n'.join(rows))
    
    def __str__(self):
        """
        Return a unique sting identifier for this board
        """
        return ''.join([''.join(map(str, row)) for row in self.board])
    
    def __lt__(self, other):
        sum1 = sum(sum(self.board,[]))
        sum2 = sum(sum(other.board,[]))
        if sum1 < sum2:
            return self
        else:
            return other
        
if __name__ == "__main__":
    board = "sudoku.csv"

    start = BoardState(board)
    print ("\nYour puzzle:")
    start.pretty_print()
    print ("\nSolving...\n")
    solver = Solver(start)
    start = time.time()
    fin = solver.solve()
    print("Total time:", time.time()-start)
    
    #solver.validate_solution(fin)
    print ("Complete! See solution below:\n")
    fin.pretty_print()
       