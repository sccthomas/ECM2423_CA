import sys
import time


sys.setrecursionlimit(100000000)


class Node:
    """
        This is a class to represent all positions that could be taken in the maze
        With the given mazes these represent the '-' spaces in the text files.

        - These node objects contain a list of neighbours through their object reference
        - Nodes contain a location which is the coordinates of the node on the maze when
          converted into a 2D array.
        - As A* is being used we have attributes g, h, f and parent (the parent node).
        - The node contains the visited attribute to represent if it has been represented

    """
    def __init__(self, location: [int]):
        self.location = location
        self.neighbours = []  # will contain references to neighbouring nodes
        self.visited = False
        self.g = 0
        self.h = 0
        self.f = sys.maxsize  # Set to a large number
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
        """
        This class represents a maze that the user wants to solve.
        - The maze is converted into a 2D array
        - All nodes and neighbourhoods for the maze are created
        - The width, height, start and end of the maze are found
        Once these steps have been completed the maze is now ready to be
        solved using the methods that are attached to each maze object.

        :param maze: The maze file that the user has inputted
        """
        self.maze = maze
        self.maze_to_array()
        self.width = len(self.maze[0])
        self.height = len(self.maze)
        self.Nodes = {}  # A dictionary which contains node coordinates paired up with node objects
        self.create_nodes()
        self.find_neighbourhood()
        self.start, self.end = self.find_start_end()

    def maze_to_array(self) -> [[str]]:
        """
        This function uses the maze file name provided by the user,
        and attempts to open the maze. It then loops through the lines
        in the file and converts each to a row in a 2D array.

        :return : 2D array of the maze text file
        """
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
        """
        Print maze is a function that will take as a parameter the solution path
        and at each coordinate in the path enter an X in the 2D array.
        Once this is completed the 2D maze array will be outputted to the user in a
        formatted way.
        :param path: The mazes solution path, containing the coordinated of each move
                    needed in the maze.
        """
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
        """
        This function will find the coordinates of the start and end of
        the maze inputted. Allowing for the program to work with mazes of
        varying start and end points.
        :return: A tuple containing the end and start coordinates
        """
        start = self.maze[0]
        end = self.maze[len(self.maze) - 1]
        start_coords = [0, start.index('-')]
        end_coords = [len(self.maze) - 1, end.index('-')]
        start_coords = self.Nodes.get(tuple(start_coords))
        end_coords = self.Nodes.get(tuple(end_coords))
        return start_coords, end_coords

    def create_nodes(self):
        """
        This function will iterate through the 2D maze array and create a node object
        for each position that is a '-'. These will be stored in a dictionary where
        the key is the coordinates of the object and the value is the object.

        """
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.maze[i][j] == '-':
                    node = Node([i, j])
                    self.Nodes.update({(i, j): node})

    def find_neighbour(self, x: int, y: int) -> [int]:
        """
        This function is used by the function find_neighbourhood(). The function is given some coordinates
        and determines if there is a movable position there.

        :param x: The x coordinate being checked
        :param y: The y coordinate being checked
        :return: If true return the coordinates of the position, or none
        """
        if 0 <= x <= self.height-1 and 0 <= y <= self.width-1:
            new_move = self.maze[x][y]
            if new_move == '-':
                return [x, y]
        else:
            return None

    def find_neighbourhood(self):
        """
        This function will locate the neighbouring nodes of all nodes in the 2D maze array. So that we can easily
        locate the adjacent nodes of a given node later on in the search, thus reducing time complexity. Each
        successful node is added to the node object being searched for.

        """
        for node in self.Nodes.values():
            coordinates = node.get_location()
            x = coordinates[0]
            y = coordinates[1]

            position_down = self.find_neighbour(x + 1, y)
            if position_down is not None:
                node.add_to_neighbourhood(self.Nodes.get((x + 1, y)))

            position_left = self.find_neighbour(x, y - 1)
            if position_left is not None:
                node.add_to_neighbourhood(self.Nodes.get((x, y - 1)))

            position_up = self.find_neighbour(x - 1, y)
            if position_up is not None:
                node.add_to_neighbourhood(self.Nodes.get((x - 1, y)))

            position_right = self.find_neighbour(x, y + 1)
            if position_right is not None:
                node.add_to_neighbourhood(self.Nodes.get((x, y + 1)))

    def get_amount_visited(self) -> int:
        """
        This function will iterate though the nodes dictionary and identify all nodes that have been
        visited during the search. During the loop it will keep a tally of those visited.
        :return: The amount of nodes visited during the search.
        """
        amount = 0
        for node in self.Nodes.values():
            if node.get_visited():
                amount += 1
        return amount

    def calculate_manhattan(self, node):
        """
        This function is the heuristic function in my A* searching algorithm.
        It uses the manhattan distance between a given node and the end node.
        :param node: The node the heuristic is being calculated for.
        :return: The heuristic value of h(n), where n is node.
        """
        h = abs(node.get_location()[0] - self.end.get_location()[0]) + \
            abs(node.get_location()[1] - self.end.get_location()[1])
        return h

    def a_star(self):
        """
        This function performs an A* search on the maze object.
        :return: The goal node which has been updated to have a parent node.
        """
        open_list = {}  # My open list of nodes that are yet to be visited but have been identified in neighbourhoods
        # it is a dictionary that contains the key as a node and the value as the nodes f value.
        open_list.update({self.start: self.calculate_manhattan(self.start)})  # The start node is added to the
        # dictionary with an f value as its heuristic value
        while len(open_list) != 0:  # While there are nodes to be searched
            current = min(open_list, key=open_list.get)  # This lambda expression will get the node with the lowest f
            open_list.pop(current)
            if current.get_visited():  # If the node is visited skip to next iteration
                continue
            current.set_visited()  # Set the node as visited
            if current == self.end:  # If the current node is the end node then the loop breaks
                return current  # Return the end node which will allow for backtracking the path
            for neighbour in current.get_neighbours():
                neighbour.set_h(self.calculate_manhattan(neighbour))  # Calculate the heuristic value for each
                # neighbour when it is needed saving on time complexity
                # Calculate the temporary comparison f = g + h
                temp_g = current.get_g() + 1
                temp_f = neighbour.get_h() + temp_g
                if temp_f < neighbour.get_f():  # If the temporary f is smaller than the current change the path
                    neighbour.set_g(temp_g)
                    neighbour.set_f(temp_f)
                    open_list.update({neighbour: neighbour.get_f()})  # Update/Add the f value in open_list
                    neighbour.set_parent(current)  # Set the neighbours parent as the current node, allowing for
                    # backtracking

    def backtrack(self, node):
        """
        Once the path is found we must backtrack from the end node to create the path taken.

        :param node: The end node which will start the backtracking process.
        :return: The path and amount of nodes in the solution path.
        """
        current = node
        amount = 1
        path = [current.get_location()]
        while current != self.start:
            current = current.get_parent()
            path.append(current.get_location())
            amount += 1
        return path, amount


if __name__ == '__main__':
    # Code that will provide the user with a UI, where they can input mazes to be solved.
    while True:
        user_choice = input("Welcome to the maze solver! With A* \n"
                            "What would you like to do \n"
                            "1. Solve a maze \n"
                            "2. Quit \n"
                            " ------ : ")
        if user_choice == "1":
            print("Note all maze files must be stored in the directory mazes!")
            user_maze = input("Please input your maze\n"
                              "Make sure you input the full file name: ")
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




