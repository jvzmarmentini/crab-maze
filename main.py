# Distance betwenn two point P(x',y') and Q(x",y") is givin by: d(P,Q) = sqrt(pow(x"-x',2) + pow(y"-y',2))
# G cost = distance from starting node
# H cost = distance from end node
# F cost = G cost + H cost

# SEE AStarGuide.jpeg (sorry for the bad quality ;-;)

# PSEUDOCODE

# OPEN //the set of nodes to be evaluated
# CLOSED //the set of nodes already evaluated
# add the start node to OPEN

# loop
#     current = node in OPEN with the lowest f_cost
#     remove current from OPEN
#     add current to CLOSED

#     if current is the target node //path has been found
#         return

#     foreach neighbour of the current node
#         if neighbour is not traversable or neighbour is in CLOSED
#             skip to the next neighbour

#         if new path to neighbour is shorter OR neighbour is not in OPEN
#             set f_cost of neighbour
#             set parent of neighbour to current
#             if neighbour is not in OPEN
#                 add neighbour to OPEN

import networkx as nx
import matplotlib.pyplot as plt
import math


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
    return [x, y]


def aStar(graph, maze, crabP, exitP):
    # both odd or even
    if(XNOR(isOdd(sum(crabP)), isOdd(sum(exitP)))):
        # start node
        g_cost = 0
        h_cost = int(math.sqrt(pow(exitP[0] + crabP[0], 2) +
                               pow(exitP[1] + crabP[1], 2)) * 10)
        f_cost = g_cost + h_cost
        graph.add_node('C', g_cost=g_cost, h_cost=h_cost, f_cost=f_cost)

        # end node
        g_cost = int(math.sqrt(pow(crabP[0] + exitP[0], 2) +
                               pow(crabP[1] + exitP[1], 2)) * 10)
        h_cost = 0
        f_cost = g_cost + h_cost
        graph.add_node('S', g_cost=g_cost, h_cost=h_cost, f_cost=f_cost)
        print(graph.nodes.data())
    else:
        return -1


def isOdd(x):
    return x % 2


def NOT(A):
    return ~A+2


def XNOR(A, B):
    return NOT(A ^ B)


maze = readFile("3_3.txt")
crab_position = getPosition(maze, 'C')
exit_position = getPosition(maze, 'S')
graph = nx.Graph()
aStar(graph, maze, crab_position, exit_position)


nx.draw(graph, with_labels=True, font_weight='bold')


plt.show()
