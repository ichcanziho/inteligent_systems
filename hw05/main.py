from hw05.core import Sudoku


def main():
    board = "sudoku.csv"
    game = Sudoku(csv_dir=board)
    game.fill_cells()



if __name__ == '__main__':
    main()
