import sys


class Node():
    def __init__(self, state: tuple[int, int], parent: Node | None, action: int) -> None:
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self) -> None:
        self.frontier: list[Node] = []

    def add(self, node: Node) -> None:
        self.frontier.append(node)

    def contains_state(self, state: tuple[int, int]) -> bool:
        return any(node.state == state for node in self.frontier)

    def empty(self) -> bool:
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty Frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty Frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class Maze():
    def __init__(self, filename) -> None:
        # Read file and set height and width of the maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one starting point")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls: list[list[bool]] = []
        for i in range(self.height):
            row: list[bool] = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        
        self.solution: tuple[list[int], list[tuple[int, int]]] | None = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("â–ˆ", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()
    
    def neighbour(self, state: tuple[int, int]):
        row, col = state
        candidate: list[tuple[str, tuple[int, int]]] = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
        
        result: list[tuple[str, tuple[int, int]]] = []
        for action, (r, c) in candidate:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result
    
    def solve(self):
        """Finds a solution to maze, if one exists"""
        
        # Keep track of number of states explored
        self.num_explored = 0
        
        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)
        
        # Initialize an empty explored set
        self.explored: set[Node] = set()
        
        # Keep looping until solution found
        while True:
            
            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")
            
            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1
            
            # If node is the goal then we have a solution
            if node.state == self.goal:
                actions: list[int] = []
                cells: list[tuple[int, int]] = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                    
        