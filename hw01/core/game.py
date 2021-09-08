class Game:

    def __init__(self, cannibalLeft, missionaryLeft, boat, cannibalRight, missionaryRight, boat_capacity=2):
        self.cannibalLeft = cannibalLeft
        self.missionaryLeft = missionaryLeft
        self.boat = boat
        self.cannibalRight = cannibalRight
        self.missionaryRight = missionaryRight
        self.parent = None
        self.capacity = boat_capacity
    
    #Function to decide if a node is a goal state or not
    def is_goal(self):
        if self.cannibalLeft == 0 and self.missionaryLeft == 0:
            return True
        else:
            return False
    
    #Function to decide if a new node is valid
    def is_valid(self):
        if self.missionaryLeft >= 0 and self.missionaryRight >= 0 \
                and self.cannibalLeft >= 0 and self.cannibalRight >= 0 \
                and (self.missionaryLeft == 0 or self.missionaryLeft >= self.cannibalLeft) \
                and (self.missionaryRight == 0 or self.missionaryRight >= self.cannibalRight):
            return True
        else:
            return False

    #Function to generate the succesor of a specific node
    @staticmethod
    def generate_successors(state):
        children = []
        moves = []
        #These loops creates the available moves
        #given a certain node or state, having as
        #constraints the boat capacity and the numbers
        #of cannibals and missionaries.
        for missioners in range(state.capacity + 1):
            for cannibals in range(state.capacity + 1):
                if 0 < missioners < cannibals:
                    continue
                if 1 <= missioners + cannibals <= state.capacity:
                    moves.append((missioners, cannibals))
        cannibal = 0
        missioner = 1
        #This loop search inside the available moves to create a
        #new node, if the node is a valid state, then is appended
        #to the child list
        for move in moves:
            if state.boat == "left":
                new_state = Game(state.cannibalLeft - move[cannibal], state.missionaryLeft - move[missioner], 'right',
                                 state.cannibalRight + move[cannibal], state.missionaryRight + move[missioner],
                                 state.capacity)
            else:
                new_state = Game(state.cannibalLeft + move[cannibal], state.missionaryLeft + move[missioner], 'left',
                                 state.cannibalRight - move[cannibal], state.missionaryRight - move[missioner],
                                 state.capacity)

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

        for node in reversed(path):
            print(str(node))

    #Function to make the search, either DFS or BFS
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

    #Overloaded operand equal to compare the objects of the class.
    def __eq__(self, other):
        return self.cannibalLeft == other.cannibalLeft and self.missionaryLeft == other.missionaryLeft \
               and self.boat == other.boat and self.cannibalRight == other.cannibalRight \
               and self.missionaryRight == other.missionaryRight

    def __str__(self):
        name = f'({self.cannibalLeft},{self.missionaryLeft},{self.boat},{self.cannibalRight},{self.missionaryRight})'
        return name
