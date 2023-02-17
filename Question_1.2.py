import time

def mazeToArray(file: str) -> [[str]]:
    maze = []
    maze_file = open("mazes/" + file, "r")
    rows = maze_file.readlines()
    for row in rows:
        if len(row) > 1:
            row_final = []
            for item in list(row):
                if item != ' ':
                    row_final.append(item)
            row_final.remove('\n')
            maze.append(row_final)
    return maze


def findStartEnd(maze: [[str]]) -> tuple[[int], [int]]:
    start = maze[0]
    end = maze[len(maze) - 1]
    start_coords = [0, start.index('-')]
    end_coords = [len(maze) - 1, end.index('-')]
    return start_coords, end_coords


def findNeighbours(maze: [[str]], x: int, y: int, visited: [[int]]) -> [int]:
    try:
        if 0 <= x <= len(maze) and 0 <= y <= len(maze[0]):
            new_move = maze[x][y]
            if [x, y] not in visited:
                if new_move == '-':
                    return [x, y]
    except:
        pass


def findPath(maze: [[str]], start: [int], end: [int]) -> tuple[[[int]], [[int]]]:
    stack = [start]
    neighbours = []
    visited = []
    path = {}  # this will be used to store the visited nodes and their parent node
    while stack:
        current_node = stack.pop()
        if current_node in visited:
            continue
        visited.append(current_node)
        x = current_node[0]
        y = current_node[1]
        # we try to find all directions that we can go
        position_up = findNeighbours(maze, x-1, y, visited)
        if position_up is not None:
            stack.append(position_up)
            neighbours.append(position_up)
        position_down = findNeighbours(maze, x+1, y, visited)
        if position_down is not None:
            stack.append(position_down)
            neighbours.append(position_down)
        position_left = findNeighbours(maze, x, y-1, visited)
        if position_left is not None:
            stack.append(position_left)
            neighbours.append(position_left)
        position_right = findNeighbours(maze, x, y+1, visited)
        if position_right is not None:
            stack.append(position_right)
            neighbours.append(position_right)

        path.update({tuple(current_node): neighbours})
        neighbours = []

        if [x, y] == end:
            print("found!")
            return path, visited


def pathToCoords(path: dict, end: [int], start: [int]) -> [[int]]:
    coords_path = [start]
    current = end
    while current != start:
        coords_path.append(current)
        for key in path.keys():
            if current in path.get(key):
                current = list(key)
                break
    return coords_path


def printMaze(path: [[int]], maze: [[str]]):
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            if maze[i][j] != '#':
                maze[i][j] = ' '
    for coord in path:
        x = coord[0]
        y = coord[1]
        maze[x][y] = 'X'
    for row in maze:
        print((', '.join(map(str, row))).replace(',',""))



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
            maze = []
            try:
                maze = mazeToArray(user_maze)
            except:
                print("Sorry this file doesn't exist \n"
                      "Mazes must be in the mazes folder")
                continue
            start, end = findStartEnd(maze)
            path, visited = findPath(maze, start, end)
            coords_path = pathToCoords(path, end, start)
            t1 = time.time()
            total = t1-t0
            print("################################################")
            print("\n")
            print("Execution time:", total)
            print("Nodes Visited:", len(visited))
            print("Steps in path:", len(coords_path))
            print("\n")
            printMaze(coords_path,maze)
            print("\n")
            print("################################################")

        elif user_choice == "2":
            break
        else:
            print("Not a valid input!")
