import networkx as nx


def readFile(file_path):
    with open(file_path) as reader:
        maze = reader.read().rstrip()
        hSize = 3
        vSize = 3
        print(len(maze[0]))
        print(maze.index("C"))
        crab_position = [int(maze.index("C") / hSize), maze.index("C") % hSize]
        print(crab_position)
        # for i in range(hSize):
        #     for j in range(vSize):
        #         print()


readFile("3_3.txt")
