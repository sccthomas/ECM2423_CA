import sys

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
        path = self.depthFirstSearch(self.start, self.end)
        path.append(self.start.getLocation())
        self.printMaze(path)

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







maze = Maze("maze-VLarge.txt")
"""
node = (maze.Nodes.get((1, 1)))
for n in (node.getNeighbours()):
    print(n.getVisited())
maze.Nodes.get((0, 1)).setVisited()
node = (maze.Nodes.get((1, 1)))
for n in (node.getNeighbours()):
    print(n.getVisited())
"""


