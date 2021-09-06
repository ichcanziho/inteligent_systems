class Game:
    def __init__(self, cannibalLeft, missionaryLeft, boat, cannibalRight, missionaryRight, boat_capacity=2):
        self.cannibalLeft = cannibalLeft
        self.missionaryLeft = missionaryLeft
        self.boat = boat
        self.cannibalRight = cannibalRight
        self.missionaryRight = missionaryRight
        self.parent = None
        self.capacity = boat_capacity

    def is_goal(self):
        if self.cannibalLeft == 0 and self.missionaryLeft == 0:
            return True
        else:
            return False

    def is_valid(self):
        if self.missionaryLeft >= 0 and self.missionaryRight >= 0 \
                and self.cannibalLeft >= 0 and self.cannibalRight >= 0 \
                and (self.missionaryLeft == 0 or self.missionaryLeft >= self.cannibalLeft) \
                and (self.missionaryRight == 0 or self.missionaryRight >= self.cannibalRight):
            return True
        else:
            return False

    @staticmethod
    def generate_successors(state):
        children = []
        moves = []
        for missioners in range(state.capacity + 1):
            for cannibals in range(state.capacity + 1):
                if 0 < missioners < cannibals:
                    continue
                if 1 <= missioners + cannibals <= state.capacity:
                    moves.append((missioners, cannibals))
        cannibal = 0
        missioner = 1
        for move in moves:
            if state.boat == "left":
                new_state = Game(state.cannibalLeft - move[cannibal], state.missionaryLeft - move[missioner], 'right',
                                 state.cannibalRight + move[cannibal], state.missionaryRight + move[missioner])
            else:
                new_state = Game(state.cannibalLeft + move[cannibal], state.missionaryLeft + move[missioner], 'left',
                                 state.cannibalRight - move[cannibal], state.missionaryRight - move[missioner])

            if new_state.is_valid():
                new_state.parent = state
                children.append(new_state)

        return children

    @staticmethod
    def print_solution(solution):
        path = [solution]
        parent = solution.parent
        while parent:
            path.append(parent)
            parent = parent.parent

        for t in range(len(path)):
            state = path[len(path) - t - 1]
            print(str(state))

    @staticmethod
    def search_solution(initial_state, method):

        if initial_state.is_goal():
            return initial_state
        frontier = list()
        explored = list()
        frontier.append(initial_state)
        while frontier:
            state = frontier.pop(0)
            if state.is_goal():
                return state
            explored.append(state)
            children = Game.generate_successors(state)
            for child in children:
                if (child not in explored) and (child not in frontier):
                    if method == "DFS":
                        frontier.insert(0, child)
                    elif method == "BFS":
                        frontier.append(child)

        return None

    def __eq__(self, other):
        return self.cannibalLeft == other.cannibalLeft and self.missionaryLeft == other.missionaryLeft \
               and self.boat == other.boat and self.cannibalRight == other.cannibalRight \
               and self.missionaryRight == other.missionaryRight

    def __str__(self):
        name = f'({self.cannibalLeft},{self.missionaryLeft},{self.boat},{self.cannibalRight},{self.missionaryRight})'
        return name