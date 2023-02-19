class node():
    def __init__(self, position):
        self.Position = position
        self.Neighbours = [None, None, None, None]
        self.visited = False

class maze():
    def __init__(self, maze_array):
        self.maze_array = maze_array
        self.start, self.end = self.findStartEnd()

    def abstractMaze(self):
        pass

    def findStartEnd(self) -> tuple[[int], [int]]:
        start = self.maze_array[0]
        end = maze[len(self.maze_array) - 1]
        start_coords = [0, start.index('-')]
        end_coords = [len(self.maze_array) - 1, end.index('-')]
        return start_coords, end_coords







