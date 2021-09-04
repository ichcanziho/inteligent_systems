from hw01.core import Game


def main():
    state = Game(3, 3, 'left', 0, 0, 2)
    solution = Game.search_solution(initial_state=state, method="BFS")
    print("Using BFS")
    Game.print_solution(solution)
    solution = Game.search_solution(initial_state=state, method="DFS")
    print("Using DFS")
    Game.print_solution(solution)


if __name__ == "__main__":
    main()
