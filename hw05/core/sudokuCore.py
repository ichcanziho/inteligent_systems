import csv


class Sudoku:
    def __init__(self, csv_dir):
        self.board = list()
        self.board_priority = list()
        with open(csv_dir, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            for row in reader:
                self.board.append([int(val) for val in row])
                self.board_priority.append([9 for i in range(len(row))])

        self.show_board()
        print("----------------------------")
        self.update_board_priority()
        print("----------------------------")
        self.show_board_priority()
        self.number_density = {i: 9 for i in range(1, 10, 1)}
        self.update_number_density()
        print(self.number_density)

    @staticmethod
    def sboard(bo):
        for i in range(len(bo)):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - -")

            for j in range(len(bo[0])):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")

                if j == 8:
                    print(bo[i][j])
                else:
                    print(str(bo[i][j]) + " ", end="")

    def show_board(self):
        bo = self.board
        self.sboard(bo)

    def show_board_priority(self):
        bo = self.board_priority
        self.sboard(bo)

    def get_cell_priority(self, x, y):
        y, x = x, y
        value = self.board[x][y]
        # get the row vector
        row = [self.board[x][i] for i in range(9)]

        # get the column vector
        column = [self.board[i][y] for i in range(9)]

        x_quad = int(x / 3)
        y_quad = int(x / 3)
        # get the quadrant vector
        quadrant = list()
        for i in range(3):
            nx = i + (x_quad * 3)
            for j in range(3):
                ny = j + (y_quad * 3)
                quadrant.append(self.board[nx][ny])

        alls = set(range(10))
        frees = set(row) | set(column) | set(quadrant)
        frees = alls - frees

        return len(frees)

    def update_board_priority(self):
        for i in range(len(self.board_priority)):
            for j in range(len(self.board_priority[0])):
                if self.board[i][j] == 0:
                    self.board_priority[i][j] = self.get_cell_priority(i, j)

    def update_number_density(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] in self.number_density:
                    self.number_density[self.board[i][j]] -= 1

