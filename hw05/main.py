from hw05.core import Sudoku


def main():
    board = "sudoku.csv"
    game = Sudoku(csv_dir=board)
    # game.check_col(8)
    # game.check_row(8)

    game.first_check()
    game.check_col(7)


    
if __name__ == '__main__':
    main()
