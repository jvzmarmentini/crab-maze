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
    y = next(x for x, v in enumerate(list) if char in v)
    x = list[y].index(char)
    return [x, y]


def aStar(graph, maze, crabP, exitP):
    # both odd or even
    if(XNOR(isOdd(sum(crabP)), isOdd(sum(exitP)))):
        # start node
        """
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
        """
        for x in range(len(maze)):
            for y in range(len(maze[x])):
                node = 'node{a}{b}'.format(a=x, b=y)
                if(maze[x][y] == 'C'):
                    node = 'C'
                elif(maze[x][y] == 'S'):
                    node = 'S'
                graph.add_node(node, pos=(y,x)) #CALCULAR E ADICIONAR F, G e H
                edge = 'edge{a}{b}'.format(a=x, b=y)
                
                if(maze[x][y] != 'X'): #QUANDO I OU J SÃO 0 NÃO FAZER -1
                    #laterais
                    graph.add_edge('{a}{b}'.format(a=x, b=y), (x,y))
                    print()
                    #diagonais
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

pos = nx.get_node_attributes(graph, 'pos') #gera dicionario com a posição dos nodos
print(pos)
options={
    'with_labels': False, 
    #'font_weight': 'bold',
    'node_size': 50,
    'pos': pos
}

nx.draw_networkx(graph, pos) #passando a posição ele ordena


plt.show()
