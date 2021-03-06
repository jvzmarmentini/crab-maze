# Distance betwenn two point P(x',y') and Q(x",y") is givin by: d(P,Q) = sqrt(pow(x"-x',2) + pow(y"-y',2))
# G cost = distance from starting node
# H cost = distance from end node
# F cost = G cost + H cost

# SEE AStarGuide.jpeg (sorry for the bad quality ;-;)


# @see https://www.youtube.com/watch?v=-L-WgKMFuhE

# @see https://networkx.org/
import networkx as nx
# @see https://matplotlib.org/
import matplotlib.pyplot as plt
import math
import heapq


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


def aStar(graph, maze):
    # both odd or even
    if(XNOR(isOdd(sum(crabP)), isOdd(sum(exitP)))):
        # open
        open_nodes = Heap(key=lambda self: self.fCost())

        # closed
        closed_nodes = Heap()

        # start node
        crab_node = Node(position=crabP)
        graph.add_node(crab_node)

        # end node
        exit_node = Node(position=exitP)
        graph.add_node(exit_node)

        # add current to open
        open_nodes.push(crab_node)

        while(open_nodes.size() > 0):
            current = open_nodes.pop()
            closed_nodes.push(current)

            if(current == exit_node):
                path = []
                while current != crab_node:
                    path.append(current)
                    current = current.parent
                return path[::-1]

            for neighbor in traversableNeighbors(current, maze):
                # skip if neighbor is in closed
                if(closed_nodes.hasNode(neighbor)):
                    continue

    else:
        return -1


def isOdd(x):
    return x % 2


def XNOR(A, B):
    return not(A ^ B)


class Heap(object):
    def __init__(self, initial=None, key=lambda x: x):
        self.key = key
        self.index = 0
        self._data = []
        self.queueIndex = {}

    def push(self, item):
        heapq.heappush(self._data, (self.key(item), self.index, item))
        self.queueIndex[self.key(item)] = item
        self.index += 1

    def pop(self):
        result = heapq.heappop(self._data)[2]
        del self.queueIndex[self.key(result)]
        return result

    # TODO test
    def hasNode(self, item):
        return self.key(item) in self.queueIndex

    def size(self):
        return len(self._data)


class Node():
    def __init__(self, parent=None, position=[0, 0]):
        self.parent = parent
        self.position = position
        self.g_cost = getDistance(crabP, position)
        self.h_cost = getDistance(exitP, position)

    def fCost(self):
        return self.g_cost + self.h_cost


def traversableNeighbors(current, maze):
    # TODO add edges

    neighbors_nodes = []
    currentX = current.position[0]
    currentY = current.position[1]

    # North
    if(maze[currentX][currentY+2] == '.' and maze[currentX][currentY+1] == '.'):
        neighbors_nodes.append(Node(current, position=[currentX, currentY+2]))

    if(maze[currentX+1][currentY+1] == '.'):
        neighbors_nodes.append(
            Node(current, position=[currentX+1, currentY+1]))

    # East
    if(maze[currentX+2][currentY] == '.' and maze[currentX+1][currentY] == '.'):
        neighbors_nodes.append(Node(current, position=[currentX+2, currentY]))

    if(maze[currentX+1][currentY-1] == '.'):
        neighbors_nodes.append(
            Node(current, position=[currentX+1, currentY-1]))

    # South
    if(maze[currentX][currentY-2] == '.' and maze[currentX][currentY-1] == '.'):
        neighbors_nodes.append(Node(current, position=[currentX, currentY-2]))

    if(maze[currentX-1][currentY-1] == '.'):
        neighbors_nodes.append(
            Node(current, position=[currentX-1, currentY-1]))

    # West
    if(maze[currentX-2][currentY] == '.' and maze[currentX-1][currentY] == '.'):
        neighbors_nodes.append(Node(current, position=[currentX-2, currentY]))

    if(maze[currentX-1][currentY+1] == '.'):
        neighbors_nodes.append(
            Node(current, position=[currentX-1, currentY+1]))

    return neighbors_nodes


def getDistance(nodeA, nodeB):
    dstX = abs(nodeA[0] - nodeB[0])
    dstY = abs(nodeA[1] - nodeB[1])
    if(dstX > dstY):
        return 14*dstY + 10*(dstX - dstY)
    return 14*dstX + 10*(dstY-dstX)


maze = readFile("3_3.txt")
global crabP
crabP = getPosition(maze, 'C')
global exitP
exitP = getPosition(maze, 'S')
graph = nx.Graph()
print(aStar(graph, maze))

nx.draw(graph, with_labels=True, font_weight='bold')
plt.show()
