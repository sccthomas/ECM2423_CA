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


def findPath(maze: [[str]], start: [int], end: [int]) -> [[int]]:
    stack = []
    visited = []
    stack.append(start)
    # if there are nodes around that are not visited then we push to path
    while stack:
        current_node = stack.pop()
        x = current_node[0]
        y = current_node[1]
        anymore = 0
        # we try to find all directions that we can go
        try:
            if maze[x+1][y] == '-':  # down
                if [x+1, y] not in visited:
                    stack.append([x+1, y])
                    anymore += 1
        except:
            pass
        try:
            if maze[x][y-1] == '-':  # left
                if [x, y-1] not in visited:
                    stack.append([x, y-1])
                    anymore += 1
        except:
            pass
        try:
            if maze[x-1][y] == '-':  # up
                if [x-1, y] not in visited:
                    stack.append([x-1, y])
                    anymore += 1
        except:
            pass
        try:
            if maze[x][y+1] == '-':  # right
                if [x, y+1] not in visited:
                    stack.append([x, y+1])
                    anymore += 1
        except:
            pass

        print(current_node)
        visited.append(current_node)
        if [x, y] == end:
            print("found!")
            return visited

def printMaze(path:[[str]], maze:[[str]]):
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
    print(end)
    path = findPath(maze, start, end)
    printMaze(path, maze)
