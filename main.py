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


def findPath(maze: [[str]], start: [int], end: [int]) -> [[int]]:
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
            return path


def pathToCoords(path: dict, end: [int], start: [int]) -> [[int]]:
    coords_path = []
    current = end
    while current != start:
        coords_path.append(current)
        for key in path.keys():
            if current in path.get(key):
                current = list(key)
                break
    print(coords_path)
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
        for i in range(0, len(row)*2, 2):
            row.insert(i, ' ')
        print((', '.join(map(str, row))).replace(',',""))




if __name__ == '__main__':
    # make a user input bit where they input the mazes that they want to traverse
    maze = mazeToArray("maze-Easy.txt")
    start, end = findStartEnd(maze)
    path = findPath(maze, start, end)
    coords_path = pathToCoords(path, end, start)
    printMaze(coords_path,maze)
