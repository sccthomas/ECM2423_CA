import sys
import time

sys.setrecursionlimit(100000000)


class Node:
    def __init__(self, location):
        self.location = location
        self.neighbours = []  # will contain references to neighbouring nodes
        self.visited = False

    def setVisited(self):
        self.visited = True

    def getLocation(self):
        return self.location

    def getVisited(self):
        return self.visited

    def addToNeighbourhood(self, node):
        self.neighbours.append(node)

    def getNeighbours(self):
        return self.neighbours


class Maze:
    def __init__(self, maze):
        self.maze = maze
        self.mazeToArray()
        self.width = len(self.maze[0])
        self.height = len(self.maze)
        self.Nodes = {}
        self.createNodes()
        self.findNeighbourhood()
        self.start, self.end = self.findStartEnd()

    def mazeToArray(self) -> [[str]]:
        maze_array = []
        maze_file = open("mazes/" + self.maze, "r")
        rows = maze_file.readlines()
        for row in rows:
            if len(row) > 1:
                row_final = []
                for item in list(row):
                    if item != ' ':
                        row_final.append(item)
                row_final.remove('\n')
                maze_array.append(row_final)
        self.maze = maze_array

    def printMaze(self, path: [[int]]):
        for i in range(0, len(self.maze)):
            for j in range(0, len(self.maze[i])):
                if self.maze[i][j] != '#':
                    self.maze[i][j] = ' '
        for coord in path:
            x = coord[0]
            y = coord[1]
            self.maze[x][y] = 'X'
        for row in self.maze:
            print((', '.join(map(str, row))).replace(',', ""))

    def findStartEnd(self) -> tuple[[int], [int]]:
        start = self.maze[0]
        end = self.maze[len(self.maze) - 1]
        start_coords = [0, start.index('-')]
        end_coords = [len(self.maze) - 1, end.index('-')]
        start_coords = self.Nodes.get(tuple(start_coords))
        end_coords = self.Nodes.get(tuple(end_coords))
        return start_coords, end_coords

    def createNodes(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.maze[i][j] == '-':
                    node = Node([i, j])
                    self.Nodes.update({(i, j): node})

    def findNeighbour(self, x: int, y: int) -> [int]:
        if 0 <= x <= self.height-1 and 0 <= y <= self.width-1:
            new_move = self.maze[x][y]
            if new_move == '-':
                return [x, y]
        else:
            return None

    def findNeighbourhood(self):
        for node in self.Nodes.values():
            coordinates = node.getLocation()
            x = coordinates[0]
            y = coordinates[1]

            position_up = self.findNeighbour(x - 1, y)
            if position_up is not None:
                node.addToNeighbourhood(self.Nodes.get((x - 1, y)))

            position_right = self.findNeighbour(x, y + 1)
            if position_right is not None:
                node.addToNeighbourhood(self.Nodes.get((x, y + 1)))

            position_down = self.findNeighbour(x + 1, y)
            if position_down is not None:
                node.addToNeighbourhood(self.Nodes.get((x + 1, y)))

            position_left = self.findNeighbour(x, y - 1)
            if position_left is not None:
                node.addToNeighbourhood(self.Nodes.get((x, y - 1)))

    def getAmountVisited(self):
        amount = 0
        for node in self.Nodes.values():
            if node.getVisited():
                amount += 1
        return amount

    def depthFirstSearch(self, node: [int], end: [int]):
        node.setVisited()
        coords = node.getLocation()
        if coords == end.getLocation():
            return [node.getLocation()]
        neighbours = node.getNeighbours()
        for i in range(0, len(neighbours)):
            if not neighbours[i].getVisited():
                path = self.depthFirstSearch(neighbours[i], end)
                if path != 0:
                    path += [neighbours[i].getLocation()]
                    return path
        return 0

    def solve_dfs(self):
        path = self.depthFirstSearch(self.start, self.end)
        path.append(self.start.getLocation())
        print("\n")
        print("################################################")
        self.printMaze(path)
        return len(path), self.getAmountVisited()


if __name__ == '__main__':
    # make a user input bit where they input the mazes that they want to traverse
    while True:
        user_choice = input("Welcome to the maze solver! \n"
                            "What would you like to do \n"
                            "1. Solve a maze \n"
                            "2. Quit \n"
                            " ------ : ")
        if user_choice == "1":
            user_maze = input("Please input your maze\n"
                              "Make sure you input the full file name: ")
            t0 = time.time()
            maze = None
            try:
                path_length, visited = Maze(user_maze).solve_dfs()
                t1 = time.time()
                total = t1 - t0
                print("################################################")
                print("\n")
                print("Execution time:", total)
                print("Steps in path:", path_length)
                print("Nodes Visited:", visited)
                print("\n")
                print("################################################")
            except:
                print("Sorry this file doesn't exist \n"
                      "Mazes must be in the mazes folder")
                continue
        elif user_choice == "2":
            break
        else:
            print("Not a valid input!")




