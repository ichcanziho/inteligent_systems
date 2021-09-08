from hw01.core import Game


def main():
    #Configuration of the game, it can be modified to a greater number
    #of cannibals or missionaries, set the boat capacity and the start
    #position of the boat.
    state = Game(cannibalLeft=3, missionaryLeft=3, boat="left",
                 cannibalRight=0, missionaryRight=0, boat_capacity=2)
    solution = Game.search_solution(initial_state=state, method="BFS")
    print("Using BFS")
    Game.print_solution(solution)
    solution = Game.search_solution(initial_state=state, method="DFS")
    print("Using DFS")
    Game.print_solution(solution)


if __name__ == "__main__":
    main()
