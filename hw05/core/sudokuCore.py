import csv


class Sudoku:
    def __init__(self, csv_dir):
        self.current_level = 1
        self.board = list()
        self.board_priority = list()
        with open(csv_dir, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            for row in reader:
                self.board.append([int(val) for val in row])
                self.board_priority.append([0 for i in range(len(row))])

        self.number_density = {i:i for i in range(1,10,1)}
        self.show_board()
        self.update_board_priority()
        print("@@@@@")
        print("prioridad ")
        self.show_board_priority()
        print(("///////////"))


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

    def get_cell_priority(self, y, x):

        # get the row vector
        row = [self.board[y][i] for i in range(9)]

        # get the column vector
        column = [self.board[i][x] for i in range(9)]

        x_quad = int(x / 3)
        y_quad = int(y / 3)

        # get the quadrant vector
        quadrant = list()
        for i in range(3):
            nx = i + (x_quad * 3)
            for j in range(3):
                ny = j + (y_quad * 3)
                quadrant.append(self.board[ny][nx])

        alls = set(range(10))
        frees = set(row) | set(column) | set(quadrant)
        frees = alls - frees

        return len(frees), frees

    def update_board_priority(self):
        for ys in range(9):
            for xs in range(9):
                value = self.board[ys][xs]
                if value == 0:
                    priority, _ = self.get_cell_priority(ys, xs)
                    self.board_priority[ys][xs] = priority
                else:
                    self.board_priority[ys][xs] = 0

    def update_number_density(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] in self.number_density:
                    self.number_density[self.board[i][j]] -= 1

    def get_order_queue(self):
        order = []
        for ys in range(9):
            for xs in range(9):
                if self.board_priority[ys][xs] != 0:
                    if self.board_priority[ys][xs] <= self.current_level:
                         order.append([self.board_priority[ys][xs], [ys, xs]])
        order.sort(reverse=False)
        self.order_queue = order

    def fill_cells(self):

        for i in range(7):

            self.get_order_queue()
            print(len(self.order_queue), self.order_queue)
            for _, coord in self.order_queue:
                ys, xs = coord
                print(ys, xs, _, self.get_cell_priority(ys, xs))
                priority, values = self.get_cell_priority(ys, xs)
                if priority == 1:
                    value = list(values)[0]
                    self.board[ys][xs] = value
                else:
                    ...
            if len(self.order_queue) == 0:
                print("neceito más")
                self.current_level += 1
            self.update_board_priority()
            print("-------quesitos------")

        self.show_board_priority()
        print("---------")
        self.show_board()

