import sys
import time
from collections import deque

sys.setrecursionlimit(100000000)
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


def findNeighbours(maze: [[str]], x: int, y: int, visited: [[int]], width, height) -> [int]:
    if 0 <= x <= height and 0 <= y <= width:
        new_move = maze[x][y]
        if [x, y] not in visited:
            if new_move == '-':
                return [x, y]
    else:
        return None


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


#working with 3
def depthFirstSearch__(start: [int], end: [int], maze: [[str]], width, height, visited: [[int]]):
    visited.append(start)
    if start == end:
        return [start]
    x = start[0]
    y = start[1]
    # find all neighbours
    neighbours = []
    position_up = findNeighbours(maze, x - 1, y, visited, width, height)
    if position_up is not None:
        neighbours.append(position_up)

    position_right = findNeighbours(maze, x, y + 1, visited, width, height)
    if position_right is not None:
        neighbours.append(position_right)

    position_down = findNeighbours(maze, x + 1, y, visited, width, height)
    if position_down is not None:
        neighbours.append(position_down)

    position_left = findNeighbours(maze, x, y - 1, visited, width, height)
    if position_left is not None:
        neighbours.append(position_left)

    for i in range(0, len(neighbours)):
        path = depthFirstSearch__(neighbours[i], end, maze, width, height, visited)
        if path != 0:
            path += [neighbours[i]]
            print(path)
            return path
    return 0




"""
def dfs(start: [int], end: [int], maze: [[str]], width, height):
    if start == end:
        return start
    stack = [start]
    visited = []
    past = {}
    past.update({tuple(start): None})
    while len(stack) > 0:
        current = stack.pop()
        visited.append(current)
        x = current[0]
        y = current[1]
        neighbours = []
        position_up = findNeighbours(maze, x - 1, y, visited, width, height)
        if position_up is not None:
            neighbours.append(position_up)

        position_right = findNeighbours(maze, x, y + 1, visited, width, height)
        if position_right is not None:
            neighbours.append(position_right)

        position_down = findNeighbours(maze, x + 1, y, visited, width, height)
        if position_down is not None:
            neighbours.append(position_down)

        position_left = findNeighbours(maze, x, y - 1, visited, width, height)
        if position_left is not None:
            neighbours.append(position_left)

        for neighbour in neighbours:
            past.update({tuple(neighbour): current})
            if neighbour not in visited and neighbour not in stack:
                if neighbour == end:
                    pass
                stack.append(neighbour)
    return 0

"""


##########################  Make the visited an array that works by indexing so that we do not have to search it each time
############  visited = [False] * (width * height)
################### (x,y) is the position we want to make visited so visited[x*y] = True
################ then when we check we can go if visited[x*y]: then


def game():
    maze = mazeToArray("maze-Medium.txt")
    start, end = findStartEnd(maze)
    width = len(maze[0])
    height = len(maze)
    p = depthFirstSearch__(start, end, maze, width, height, visited=[False]*(width*height))
    p.append(start)
    printMaze(p, maze)


game()

"""
#Not working
def depthFirstSearch(start: [int], end: [int],maze: [[str]], visited: [[int]], path):
    visited.append(start)
    path.append(start)
    if start == end:
        printMaze(path, maze)
    x = start[0]
    y = start[1]
    # find all neighbours

    position_up = findNeighbours(maze, x - 1, y, visited)
    if position_up is not None:
        depthFirstSearch([x-1, y], end, maze, visited, path)

    position_right = findNeighbours(maze, x, y + 1, visited)
    if position_right is not None:
        depthFirstSearch([x, y + 1], end, maze, visited, path)

    position_down = findNeighbours(maze, x + 1, y, visited)
    if position_down is not None:
        depthFirstSearch([x + 1, y], end, maze, visited, path)

    position_left = findNeighbours(maze, x, y - 1, visited)
    if position_left is not None:
        depthFirstSearch([x, y - 1], end, maze, visited, path)

    else:
        path.pop()

#Not working
def depthFirstSearch_(start: [int], end: [int], maze: [[str]], width, height, visited: [[int]], path):
    visited.append(start)
    path.append(start)
    if start == end:
        print(len(visited))
        print(len(path))
        return path
    x = start[0]
    y = start[1]
    # find all neighbours
    neighbours = []
    position_up = findNeighbours(maze, x - 1, y, visited, width, height)
    if position_up is not None:
        neighbours.append(position_up)

    position_right = findNeighbours(maze, x, y + 1, visited, width, height)
    if position_right is not None:
        neighbours.append(position_right)

    position_down = findNeighbours(maze, x + 1, y, visited, width, height)
    if position_down is not None:
        neighbours.append(position_down)

    position_left = findNeighbours(maze, x, y - 1, visited, width, height)
    if position_left is not None:
        neighbours.append(position_left)

    if len(neighbours) > 0:
        for i in range(0, len(neighbours)):
            depthFirstSearch_(neighbours[i], end, maze, width, height, visited, path)
            path.pop()

"""