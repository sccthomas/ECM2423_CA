import sys
import time

sys.setrecursionlimit(100000000)


class Node:
    def __init__(self, location: [int]):
        self.location = location
        self.neighbours = []  # will contain references to neighbouring nodes
        self.visited = False
        self.g = 0
        self.h = 0
        self.f = sys.maxsize
        self.parent = None

    def set_visited(self):
        self.visited = True

    def get_location(self):
        return self.location

    def get_visited(self):
        return self.visited

    def add_to_neighbourhood(self, node):
        self.neighbours.append(node)

    def get_neighbours(self):
        return self.neighbours

    def set_parent(self, node):
        self.parent = node

    def get_parent(self):
        return self.parent

    def set_g(self,g):
        self.g = g

    def set_f(self,f):
        self.f = self.h + self.g

    def set_h(self,h):
        self.h = h

    def get_f(self):
        return self.f

    def get_g(self):
        return self.g

    def get_h(self):
        return self.h


class Maze:
    def __init__(self, maze: str):
        self.maze = maze
        self.maze_to_array()
        self.width = len(self.maze[0])
        self.height = len(self.maze)
        self.Nodes = {}
        self.create_nodes()
        self.find_neighbourhood()
        self.start, self.end = self.find_start_end()

    def maze_to_array(self) -> [[str]]:
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

    def print_maze(self, path: [[int]]):
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

    def find_start_end(self) -> tuple[[int], [int]]:
        start = self.maze[0]
        end = self.maze[len(self.maze) - 1]
        start_coords = [0, start.index('-')]
        end_coords = [len(self.maze) - 1, end.index('-')]
        start_coords = self.Nodes.get(tuple(start_coords))
        end_coords = self.Nodes.get(tuple(end_coords))
        return start_coords, end_coords

    def create_nodes(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.maze[i][j] == '-':
                    node = Node([i, j])
                    self.Nodes.update({(i, j): node})

    def find_neighbour(self, x: int, y: int) -> [int]:
        if 0 <= x <= self.height-1 and 0 <= y <= self.width-1:
            new_move = self.maze[x][y]
            if new_move == '-':
                return [x, y]
        else:
            return None

    def find_neighbourhood(self):
        for node in self.Nodes.values():
            coordinates = node.get_location()
            x = coordinates[0]
            y = coordinates[1]
            position_left = self.find_neighbour(x, y - 1)

            position_down = self.find_neighbour(x + 1, y)
            if position_down is not None:
                node.add_to_neighbourhood(self.Nodes.get((x + 1, y)))

            if position_left is not None:
                node.add_to_neighbourhood(self.Nodes.get((x, y - 1)))

            position_up = self.find_neighbour(x - 1, y)
            if position_up is not None:
                node.add_to_neighbourhood(self.Nodes.get((x - 1, y)))

            position_right = self.find_neighbour(x, y + 1)
            if position_right is not None:
                node.add_to_neighbourhood(self.Nodes.get((x, y + 1)))

    def get_amount_visited(self) -> int:
        amount = 0
        for node in self.Nodes.values():
            if node.get_visited():
                amount += 1
        return amount

    def calculate_manhattan(self, node):
        h = abs(node.get_location()[0] - self.end.get_location()[0]) + \
            abs(node.get_location()[1] - self.end.get_location()[1])
        return h

    def a_star(self):
        open_list = {}
        open_list.update({self.start: 0})
        while len(open_list) != 0:
            current = min(open_list, key=open_list.get)
            open_list.pop(current)
            if current.get_visited():
                continue
            current.set_visited()
            if current == self.end:
                return current
            for neighbour in current.get_neighbours():
                neighbour.set_h(self.calculate_manhattan(neighbour))
                temp_g = current.get_g() + 1
                temp_f = neighbour.get_h() + temp_g
                if temp_f < neighbour.get_f():
                    neighbour.set_g(temp_g)
                    neighbour.set_f(temp_f)
                    open_list.update({neighbour: neighbour.get_f()})
                    neighbour.set_parent(current)

    def backtrack(self, node):
        current = node
        amount = 1
        path = [current.get_location()]
        while current != self.start:
            current = current.get_parent()
            path.append(current.get_location())
            amount += 1
        return path, amount


if __name__ == '__main__':
    # make a user input bit where they input the mazes that they want to traverse
    while True:
        user_choice = input("Welcome to the maze solver! \n"
                            "What would you like to do \n"
                            "1. Solve a maze \n"
                            "2. Quit \n"
                            " ------ : ")
        if user_choice == "1":
            print("Note all maze files must be stored in the directory mazes!")
            user_maze = input("Please input your maze\n"
                              "Make sure you input the full file name: ")
            maze = None
            try:
                maze = Maze(user_maze)
                t0 = time.time()
                path, amount = (maze.backtrack(maze.a_star()))
                t1 = time.time()
                maze.print_maze(path)
                total = t1 - t0
                print("################################################")
                print("\n")
                print("Execution time:", total)
                print("Steps in path:", amount)
                print("Nodes Visited:", maze.get_amount_visited())
                print("\n")
                print("################################################")
            except():
                print("Sorry this file doesn't exist \n"
                      "Mazes must be in the mazes folder")
                continue
        elif user_choice == "2":
            break
        else:
            print("Not a valid input!")




