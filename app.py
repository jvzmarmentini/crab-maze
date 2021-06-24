import networkx as nx
import matplotlib.pyplot as plt
import time


def readFile(file_path):
    with open(file_path) as reader:
        line = reader.readline()
        maze = []
        while line != '':
            maze.append(line)
            line = reader.readline()
        maze = list(map(lambda s: s.strip('\n'), maze))
        return maze


def getPosition(list, char):
    y = next(i for i, v in enumerate(list) if char in v)
    x = list[y].index(char)
    return (y, x)


def isOdd(x):
    return x % 2


def XNOR(A, B):
    return not(A ^ B)


def dist(a, b):
    (x1, y1) = a
    (x2, y2) = b
    dstY = abs(x1 - x2)
    dstX = abs(y1 - y2)
    if(dstX > dstY):
        return 14*dstY + 20*(dstX - dstY)
    return 14*dstX + 20*(dstY-dstX)


def maze2graph(maze):
    graph = nx.Graph()
    global nodes
    nodes = {}

    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if(XNOR(isOdd(sum(crabP)), isOdd(sum([y, x])))):
                if(maze[y][x] != 'x'):
                    node = (y, x)
                    adjacencyList = traversableNeighbors(node, maze)
                    nodes[node] = adjacencyList

    for node in nodes:
        graph.add_node(node)
        for neighbor in nodes[node]:
            graph.add_edge(node, neighbor, color='black')

    return graph


def traversableNeighbors(node, maze):
    neighbors_nodes = []
    nodeY = node[0]
    nodeX = node[1]

    # North
    if(nodeY > 1 and maze[nodeY-2][nodeX] == '.' and maze[nodeY-1][nodeX] == '.'):
        neighbors_nodes.append((nodeY-2, nodeX))

    # NE
    if(nodeX < len(maze[0])-1 and maze[nodeY-1][nodeX+1] == '.' and nodeY > 0):
        neighbors_nodes.append((nodeY-1, nodeX+1))

    # East
    if(nodeX < len(maze[0]) - 2 and maze[nodeY][nodeX+2] == '.' and maze[nodeY][nodeX+1] == '.'):
        neighbors_nodes.append((nodeY, nodeX+2))

    # SE
    if(nodeY < len(maze)-1 and nodeX < len(maze[0])-1 and maze[nodeY+1][nodeX+1] == '.'):
        neighbors_nodes.append((nodeY+1, nodeX+1))

    # South
    if(nodeY < len(maze)-2 and maze[nodeY+2][nodeX] == '.' and maze[nodeY+1][nodeX] == '.'):
        neighbors_nodes.append((nodeY+2, nodeX))

    # SW
    if(nodeY < len(maze)-1 and nodeX > 0 and maze[nodeY+1][nodeX-1] == '.'):
        neighbors_nodes.append((nodeY+1, nodeX-1))

    # West
    if(nodeX > 1 and maze[nodeY][nodeX-2] == '.' and maze[nodeY][nodeX-1] == '.'):
        neighbors_nodes.append((nodeY, nodeX-2))

    # NW
    if(nodeY > 0 and nodeX > 0 and maze[nodeY-1][nodeX-1] == '.'):
        neighbors_nodes.append((nodeY-1, nodeX-1))

    return neighbors_nodes


start_time = time.time()

maze = readFile("test/50_50.txt")
crabP = getPosition(maze, 'C')
exitP = getPosition(maze, 'S')
if(not XNOR(isOdd(sum(crabP)), isOdd(sum(exitP)))):
    print("Não existe solução para este labirinto!")
    exit()

mazeGraph = maze2graph(maze)
color_map = []
for node in mazeGraph:
    y = list(node)[1]
    x = list(node)[0]
    if maze[x][y] == 'C':
        color_map.append('purple')
    elif maze[x][y] == 'S':
        color_map.append('orange')
    else:
        color_map.append('lightGreen')

pos = {}
for node in mazeGraph:
    pos[node] = node

node_sizes = []
for node in mazeGraph:
    node_sizes.append(50)


try:
    start_time = time.time()
    astar = nx.astar_path(mazeGraph, crabP, exitP,
                          heuristic=dist, weight="cost")
    astar_time = time.time() - start_time
    print("astar_path: %s seconds; nodes visited: " % astar_time, len(astar))

    start_time = time.time()
    dijkstra = nx.dijkstra_path(mazeGraph, crabP, exitP, weight="cost")
    dijkstra_time = time.time() - start_time
    print("dijkstra_path: %s seconds; nodes visited: " %
          dijkstra_time, len(dijkstra))

    start_time = time.time()
    shortest = nx.shortest_path(mazeGraph, crabP, exitP, weight="cost")
    shortest_time = time.time() - start_time
    print("shortest_path: %s seconds; nodes visited: " %
          shortest_time, len(shortest))

    mazeGraph.add_edges_from([(astar[i], astar[i+1])
                              for i in range(len(astar)-1)], color='red')
    colors = [mazeGraph[u][v]['color'] for u, v in mazeGraph.edges]

    nx.draw(mazeGraph, pos, node_color=color_map,
            edge_color=colors, node_size=node_sizes)
    print("after draw: %s seconds" % (time.time() - start_time))

    plt.show()
except nx.exception.NetworkXNoPath:
    print("Solução para esse caminho não existe")
