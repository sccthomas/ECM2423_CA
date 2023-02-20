import sys
import time

sys.setrecursionlimit(100000000)


class Node:
    def __init__(self, location: [int]):
        self.location = location
        self.neighbours = []  # will contain references to neighbouring nodes
        self.visited = False

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

            position_up = self.find_neighbour(x - 1, y)
            if position_up is not None:
                node.add_to_neighbourhood(self.Nodes.get((x - 1, y)))

            position_right = self.find_neighbour(x, y + 1)
            if position_right is not None:
                node.add_to_neighbourhood(self.Nodes.get((x, y + 1)))

            position_down = self.find_neighbour(x + 1, y)
            if position_down is not None:
                node.add_to_neighbourhood(self.Nodes.get((x + 1, y)))

            position_left = self.find_neighbour(x, y - 1)
            if position_left is not None:
                node.add_to_neighbourhood(self.Nodes.get((x, y - 1)))

    def get_amount_visited(self) -> int:
        amount = 0
        for node in self.Nodes.values():
            if node.get_visited():
                amount += 1
        return amount

    def depth_first_search(self, node: [int], end: [int]) -> [[int]]:
        node.set_visited()
        coords = node.get_location()
        if coords == end.get_location():
            return [node.get_location()]
        neighbours = node.get_neighbours()
        for i in range(0, len(neighbours)):
            if not neighbours[i].get_visited():
                path = self.depth_first_search(neighbours[i], end)
                if path != 0:
                    path += [neighbours[i].get_location()]
                    return path
        return 0

    def solve_dfs(self):
        path = self.depth_first_search(self.start, self.end)
        path.append(self.start.get_location())
        print("\n")
        print("################################################")
        path.pop(0)  # remove duplicated end node
        self.print_maze(path)
        return len(path), self.get_amount_visited()


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




