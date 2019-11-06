import random
import copy
import sys
import time 
import math

sys.setrecursionlimit(12000)
start_time = time.time()
# print(sys.getrecursionlimit())


# Uniform Cost: 50 nodes depth 9 time 0.0024340 seconds Max q size: 20
# Missing tile: 8 nodes depth 4 time 0.000440835 seconds Max queueu size: 4
# Manhattan Distance: 8 nodes depth 4 time 0.0005619 seconds Max q: 4
initialState = [
    [0,1,2],
    [4,5,3],
    [7,8,6]
    # [1,0,3],
    # [4,2,6],
    # [7,5,8]
]

# Uniform cost: 12980 nodes depth 45 time 64.25 seconds Max q size: 4608
# Missing tile: 1391 nodes depth 17 time 0.404481 seconds Max q size: 540
# Manhattan Distance: 174 nodes depth 17 time 0.014513 seconds Max q: 68
medium = [
    [7,4,3],
    [0,6,8],
    [1,5,2]
]

# Uniform cost: Hit limit
# Missing tile: 11840 nodes depth 22 time 43.67 seconds Max q size: 4267
# Manhattan Distance: 1162 nodes depth 22 time 0.477177 seconds Max q: 430
hard = [
    [8,5,0],
    [4,3,6],
    [1,2,7]
]

# Uniform cost: Hit limit
# Missing tile: 12980 nodes depth 45 time 51.65 seconds Max q size: 4608
# Manhattan Distance: 2031 nodes depth 45 time 1.043218 seconds Max q: 743
evenHarder = [
    [6,5,0],
    [1,8,2],
    [7,4,3]
]

# Uniform cost: Hit limit
# Missing tile: Hit limit
# Manhattan Distance: 1959 nodes depth 47 time 1.30827 seconds Max q: 703
puzzle1 = [
    [3,6,1],
    [5,8,7],
    [4,0,2]
]

# Uniform cost: Hit limit
# Manhattan Distance: 998 nodes depth 23 time 0.339037 seconds Max q: 348
puzzle2 = [
    [8,0,6],
    [3,4,5],
    [2,7,1]
]

# Uniform Cost: ??? Nodes depth 2199 time 1.03232 seconds
# Missing Tile: 82 Nodes depth 10 time 0.00479 seconds Max queue size: 34
# Manhattan Distance: 38 nodes depth 10 time 0.0022511 seconds Max q: 19
puzzle3 = [
    [1,2,3],
    [4,5,8],
    [0,6,7]
]

goalState = [
    [1,2,3],
    [4,5,6],
    [7,8,0]
]

# Determine if a state is solvable. Routine is referenced 
def solvable(initialState):

    length = len(initialState)
    tiles = []

    for x in range(length):
        for y in range(length):
            tiles.append(initialState[x][y])
            
    inversions = 0

    for i in range(8):
        for j in range(i+1, 9):
            if tiles[j] and tiles[i] and tiles[i] > tiles[j]:
                inversions += 1

    return inversions % 2 == 0



# x-1 makes go left
# x+1 makes go right
# y+1 makes go down
# y-1 makes go up

#print(A[1][1])
# First index is row
# second index is column


# Randomize initial state 
def genRandom(arr):
    
    ranNumbers = [0,1,2,3,4,5,6,7,8]
    random.shuffle(ranNumbers)

    count = 0 
    length = len(arr)
    for x in range(length):
        for y in range(length):
            arr[x][y] = ranNumbers[count]
            count += 1


# Keep on generating random states until a solveable one appears
def generateViable(arr):
    genRandom(arr)
    solvable(arr)
    
    while True:
        genRandom(arr)
        if solvable(arr) is True:
            return


# Print array function
def printArray(arr):

    if arr == None:
        print("Not existing array")
    else: 
        length = len(arr)
        for y in range(length):
            print(arr[y])

# Return the y and x position of the 0 in the state
def zeroPosition(arr):

    length = len(arr)
    for x in range(length):
        for y in range(length):
            if arr[y][x] == 0:
                return y,x


# Directional functions to change the position of the 0 in the state



def goLeft(arr):
    #VERY IMPORTANT, zeroPosition function returns as x and y
    array = arr 
    y,x = zeroPosition(array)
    # If valid move, return 1. Not valid return 0
    validMove = 1
    #edge case
    if x == 0:
        # print("You cannot go left any further")
        validMove = 0
        return validMove
    temp = copy.deepcopy(array[y][x])
    array[y][x] = array[y][x-1]
    array[y][x-1] = temp
    return validMove
    
def goRight(arr):
    #VERY IMPORTANT, zeroPosition function returns as x and y
    array = arr 
    y,x = zeroPosition(array)
    validMove = 1
    #edge case
    if x == 2:
        # print("You cannot go right any further")
        validMove = 0
        return validMove
    temp = copy.deepcopy(array[y][x])
    array[y][x] = array[y][x+1]
    array[y][x+1] = temp
    return validMove 

def goDown(arr):
    #VERY IMPORTANT, zeroPosition function returns as x and y
    array = arr
    y,x = zeroPosition(array)
    validMove = 1
    #edge case
    if y == 2:
        # print("You cannot go down any further")
        validMove = 0
        return validMove
    temp = copy.deepcopy(array[y][x])
    array[y][x] = array[y+1][x]
    array[y+1][x] = temp
    return validMove

def goUp(arr):
    #VERY IMPORTANT, zeroPosition function returns as x and y
    array = arr
    y,x = zeroPosition(array)
    validMove = 1
    #edge case
    if y == 0:
        # print("You cannot go up any further")
        validMove = 0
        return validMove
    temp = copy.deepcopy(array[y][x])
    array[y][x] = array[y-1][x]
    array[y-1][x] = temp
    return validMove


#Return how many tiles are misplaced
# Input: array
# Output: returns misplaced tiles 
def checkMisplaced(arr):        #h(n) evaluates the distance from the goal state using misplaced tiles heuristic
    length = len(arr)
    count = 1 
    misplacedCount = 0
    for y in range(length):
        for x in range(length):       #Do not count the last tile/zero as a misplaced tile
            if arr[y][x] != count:
                misplacedCount += 1
            count+=1

    return misplacedCount - 1

# Input: array
# Output: returns manhattan distance 
def checkManhattan(arr):        #h(n) evaluates the distance from the goal state using manhattan distance  heuristic

    length = len(arr)
    
    goalX = 0 
    goalY = 0
    manhattanDistance = 0
    for x in range(length):
        for y in range(length):
            value = arr[x][y]
            goalX = math.ceil(value/length)
            goalY= abs(value-(goalX-1)*length)
            goalX -= 1
            goalY -= 1
            difference = abs(goalX-x) + abs(goalY-y)
            if arr[x][y] == 0:
                difference = 0
            manhattanDistance+=difference
    return manhattanDistance



def printRoute():
    count = 0
    for x in reversed(printFinished):
        print("Count:",count)
        count+=1
        printArray(x)

def printTime():
    print("--- %s seconds ---" % (time.time() - start_time))


class Node:
    def __init__(self,key):
        self.parent = None
        self.array = key
        self.misplaced = 0   #H(n)
        self.depth = 0       #F(n)
        self.totalDistance = 0
        self.count = 0 

repeatStates = []
fringeNodes = [] 
nodeCount = 0
printFinished = []

# Input: Parent Node Output: 4 Children nodes w/ depth and h(n)(misplaced tiles)
# *** Make sure to check if the node != none before making children *** 
def misplacedTiles(parent,nodeCount):

    tempMax = len(fringeNodes)
    maxFringe = tempMax

    if parent.array == goalState:
        print("Expanded Nodes:",nodeCount,"Max queue size:",maxFringe)
        while True:
            printFinished.append(parent.array)
            parent = parent.parent
            if parent.parent == None:
                printFinished.append(parent.array)
                nodeCount+=1
                parent.count = nodeCount
                return

        
        return  

    # If empty node, end branch.
    root = parent
    if root.array == None:
        print("Empty node!")
        return

    # Set f(n), h(n), and g(n) for parent node
    if root.parent == None:
        root.depth = 0                          # Initialize root depth to 0
        root.count = nodeCount                  # Initialize root (node)count to 0
        nodeCount+=1
        repeatStates.append(root.array)         # Append the root array into repeatedStates because we are appending the rest of the children as we populate
        fringeNodes.append(root)                # Same with the fringe nodes
    root.misplaced = checkMisplaced(root.array)

    root.totalDistance = root.misplaced + root.depth


    # Make deep copies of going in each direction 
    checkDown = copy.deepcopy(parent.array) 
    checkUp = copy.deepcopy(parent.array)
    checkLeft = copy.deepcopy(parent.array)
    checkRight = copy.deepcopy(parent.array)

    # Check if direction is a valid move or not. 
    # If not valid move. set Node to None, otherwise set node to new state in that direction
    if goDown(checkDown) == 0:
        downNode = Node(None)
    else: downNode = Node(checkDown)
    # If state is not None, calculate misplaced tiles 
    if downNode.array is not None:
        downNode.misplaced = checkMisplaced(downNode.array)   
        # Set parent pointer and increment depth level
        downNode.parent = root
        if downNode.parent is not None:
            downNode.depth = root.depth+1
        downNode.totalDistance = downNode.misplaced + downNode.depth

    if goUp(checkUp) == 0:
        upNode = Node(None)
    else: upNode = Node(checkUp)
    if upNode.array is not None: 
        upNode.misplaced = checkMisplaced(upNode.array)
        upNode.parent = root
        if upNode.parent is not None:
            upNode.depth = root.depth+1
        upNode.totalDistance = upNode.misplaced + upNode.depth

    if goLeft(checkLeft) == 0:
        leftNode = Node(None)
    else: leftNode = Node(checkLeft)
    if leftNode.array is not None:
        leftNode.misplaced = checkMisplaced(leftNode.array)
        leftNode.parent = root        
        if leftNode.parent is not None: 
            leftNode.depth = root.depth+1
        leftNode.totalDistance = leftNode.misplaced + leftNode.depth


    if goRight(checkRight) == 0:
        rightNode = Node(None)
    else: rightNode = Node(checkRight)
    if rightNode.array is not None:
        rightNode.misplaced = checkMisplaced(rightNode.array)
        rightNode.parent = root
        if rightNode.parent is not None:
            rightNode.depth = root.depth+1
        rightNode.totalDistance = rightNode.misplaced + rightNode.depth


    # If the parent node can make children, enqueue the children to fringe and dequeue parent from fringe
    # Make child only if the child if the array does not already exist in repeatStates 
    if downNode.array or upNode.array or leftNode.array or rightNode.array is not None:
        fringeNodes.remove(root)
        if downNode.array is not None and downNode.array not in repeatStates:
            nodeCount+=1
            fringeNodes.append(downNode)
            repeatStates.append(downNode.array)
        if upNode.array is not None and upNode.array not in repeatStates:
            nodeCount+=1
            fringeNodes.append(upNode)
            repeatStates.append(upNode.array)
        if leftNode.array is not None and leftNode.array not in repeatStates:
            nodeCount+=1
            fringeNodes.append(leftNode)
            repeatStates.append(leftNode.array)
        if rightNode.array is not None and rightNode.array not in repeatStates:
            nodeCount+=1
            fringeNodes.append(rightNode)
            repeatStates.append(rightNode.array)

    if maxFringe < len(fringeNodes):
        maxFringe = len(fringeNodes)
    
    #__Prints all the fringes__
    # count = 0 
    # for x in fringeNodes:
    #     print("Count:",count)
    #     count+=1
    #     printArray(x.array)

    #__Prints all the repeated states__ 
    # count = 0 
    # for x in repeatStates:
    #     printArray(x)
    #     print("Count;",count)
    #     count+=1

    # Find the fringes with the smallest F(n). If multiple fringes with same F(n), expand fringes with the smallest H(n)
    minDistance = 1000 #Used as a tempto find the smallest distance - F(n)
    maxDepth = 0
    for x in fringeNodes:
        if minDistance > x.totalDistance:  
            minDistance = x.totalDistance
        if maxDepth < x.depth:
            maxDepth = x.depth

    #Iterate from the lowest depths that appear in the fringe and evaluate if it is equal to the smallest totalDistaince - F(n)
    for x in range(maxDepth+1):
        for y in fringeNodes:
            if y.depth == x and y.totalDistance == minDistance and y.array is not None:
                # printArray(y.array)
                # nodeCount+=1
                # print("Count:",nodeCount,"F(n):",y.totalDistance,"H(n):",y.depth,"G(n):",y.misplaced)
                misplacedTiles(y,nodeCount)


def uniformCost(parent,nodeCount):

    tempMax = len(fringeNodes)
    maxFringe = tempMax

    if parent.array == goalState:
        print("Expanded Nodes:",nodeCount,"Max queue size:",maxFringe)
        while True:
            printFinished.append(parent.array)
            parent = parent.parent
            if parent.parent == None:
                printFinished.append(parent.array)
                nodeCount+=1
                parent.count = nodeCount
                return 

        return 

    # If empty node, end branch.
    root = parent
    if root.array == None:
        print("Empty node!")
        return

    # Set f(n), h(n), and g(n) for parent node
    if root.parent == None:
        root.depth = 0                          # Initialize root depth to 0
        root.count = nodeCount                  # Initialize root (node)count to 0
        nodeCount+=1
        repeatStates.append(root.array)         # Append the root array into repeatedStates because we are appending the rest of the children as we populate
        fringeNodes.append(root)                # Same with the fringe nodes
    # root.misplaced = checkMisplaced(root.array)
    root.misplaced = 0

    root.totalDistance = root.misplaced + root.depth


    # Make deep copies of going in each direction 
    checkDown = copy.deepcopy(parent.array) 
    checkUp = copy.deepcopy(parent.array)
    checkLeft = copy.deepcopy(parent.array)
    checkRight = copy.deepcopy(parent.array)

    # Check if direction is a valid move or not. 
    # If not valid move. set Node to None, otherwise set node to new state in that direction
    if goDown(checkDown) == 0:
        downNode = Node(None)
    else: downNode = Node(checkDown)
    # If state is not None, calculate misplaced tiles 
    if downNode.array is not None:
        # downNode.misplaced = checkMisplaced(downNode.array)   
        downNode.misplaced = 0                                  # We are hard coding 0 here to test uniform
        # Set parent pointer and increment depth level
        downNode.parent = root
        if downNode.parent is not None:
            downNode.depth = root.depth+1
        downNode.totalDistance = downNode.misplaced + downNode.depth

    if goUp(checkUp) == 0:
        upNode = Node(None)
    else: upNode = Node(checkUp)
    if upNode.array is not None: 
        # upNode.misplaced = checkMisplaced(upNode.array)
        upNode.misplaced = 0
        upNode.parent = root
        if upNode.parent is not None:
            upNode.depth = root.depth+1
        upNode.totalDistance = upNode.misplaced + upNode.depth

    if goLeft(checkLeft) == 0:
        leftNode = Node(None)
    else: leftNode = Node(checkLeft)
    if leftNode.array is not None:
        # leftNode.misplaced = checkMisplaced(leftNode.array)
        leftNode.misplaced = 0
        leftNode.parent = root        
        if leftNode.parent is not None: 
            leftNode.depth = root.depth+1
        leftNode.totalDistance = leftNode.misplaced + leftNode.depth


    if goRight(checkRight) == 0:
        rightNode = Node(None)
    else: rightNode = Node(checkRight)
    if rightNode.array is not None:
        # rightNode.misplaced = checkMisplaced(rightNode.array)
        rightNode.misplaced = 0
        rightNode.parent = root
        if rightNode.parent is not None:
            rightNode.depth = root.depth+1
        rightNode.totalDistance = rightNode.misplaced + rightNode.depth

    # If the parent node can make children, enqueue the children to fringe and dequeue parent from fringe
    # Make child only if the child if the array does not already exist in repeatStates 
    if downNode.array or upNode.array or leftNode.array or rightNode.array is not None:
        fringeNodes.remove(root)
        if downNode.array is not None and downNode.array not in repeatStates:
            nodeCount+=1
            fringeNodes.append(downNode)
            repeatStates.append(downNode.array)
        if upNode.array is not None and upNode.array not in repeatStates:
            nodeCount+=1
            fringeNodes.append(upNode)
            repeatStates.append(upNode.array)
        if leftNode.array is not None and leftNode.array not in repeatStates:
            nodeCount+=1
            fringeNodes.append(leftNode)
            repeatStates.append(leftNode.array)
        if rightNode.array is not None and rightNode.array not in repeatStates:
            nodeCount+=1
            fringeNodes.append(rightNode)
            repeatStates.append(rightNode.array)

    if maxFringe < len(fringeNodes):
        maxFringe = len(fringeNodes)

    #__Prints all the fringes__
    # count = 0 
    # for x in fringeNodes:
    #     print("Count:",count)
    #     count+=1
    #     printArray(x.array)

    #__Prints all the repeated states__ 
    # count = 0 
    # for x in repeatStates:
    #     printArray(x)
    #     print("Count;",count)
    #     count+=1

    # Find the fringes with the smallest F(n). If multiple fringes with same F(n), expand fringes with the smallest H(n)
    minDistance = 1000 #Used as a tempto find the smallest distance - F(n)
    maxDepth = 0
    for x in fringeNodes:
        if minDistance > x.totalDistance:  
            minDistance = x.totalDistance
        if maxDepth < x.depth:
            maxDepth = x.depth

    #Iterate from the lowest depths that appear in the fringe and evaluate if it is equal to the smallest totalDistaince - F(n)
    for x in range(maxDepth+1):
        for y in fringeNodes:
            if y.depth == x and y.totalDistance == minDistance and y.array is not None:
                # printArray(y.array)
                # nodeCount+=1
                # print("Count:",nodeCount,"F(n):",y.totalDistance,"H(n):",y.depth,"G(n):",y.misplaced)
                uniformCost(y,nodeCount)
                
def manhattanHeuristic(parent,nodeCount):

    tempMax = len(fringeNodes)
    maxFringe = tempMax

    if parent.array == goalState:
        print("Expanded Nodes:",nodeCount,"Max queue size:",maxFringe)
        while True:
            printFinished.append(parent.array)
            parent = parent.parent
            if parent.parent == None:
                printFinished.append(parent.array)
                nodeCount+=1
                parent.count = nodeCount
                return

        
        return  

    # If empty node, end branch.
    root = parent
    if root.array == None:
        print("Empty node!")
        return

    # Set f(n), h(n), and g(n) for parent node
    if root.parent == None:
        root.depth = 0                          # Initialize root depth to 0
        root.count = nodeCount                  # Initialize root (node)count to 0
        nodeCount+=1
        repeatStates.append(root.array)         # Append the root array into repeatedStates because we are appending the rest of the children as we populate
        fringeNodes.append(root)                # Same with the fringe nodes
    root.misplaced = checkManhattan(root.array)

    root.totalDistance = root.misplaced + root.depth


    # Make deep copies of going in each direction 
    checkDown = copy.deepcopy(parent.array) 
    checkUp = copy.deepcopy(parent.array)
    checkLeft = copy.deepcopy(parent.array)
    checkRight = copy.deepcopy(parent.array)

    # Check if direction is a valid move or not. 
    # If not valid move. set Node to None, otherwise set node to new state in that direction
    if goDown(checkDown) == 0:
        downNode = Node(None)
    else: downNode = Node(checkDown)
    # If state is not None, calculate misplaced tiles 
    if downNode.array is not None:
        downNode.misplaced = checkManhattan(downNode.array)   
        # Set parent pointer and increment depth level
        downNode.parent = root
        if downNode.parent is not None:
            downNode.depth = root.depth+1
        downNode.totalDistance = downNode.misplaced + downNode.depth

    if goUp(checkUp) == 0:
        upNode = Node(None)
    else: upNode = Node(checkUp)
    if upNode.array is not None: 
        upNode.misplaced = checkManhattan(upNode.array)
        upNode.parent = root
        if upNode.parent is not None:
            upNode.depth = root.depth+1
        upNode.totalDistance = upNode.misplaced + upNode.depth

    if goLeft(checkLeft) == 0:
        leftNode = Node(None)
    else: leftNode = Node(checkLeft)
    if leftNode.array is not None:
        leftNode.misplaced = checkManhattan(leftNode.array)
        leftNode.parent = root        
        if leftNode.parent is not None: 
            leftNode.depth = root.depth+1
        leftNode.totalDistance = leftNode.misplaced + leftNode.depth


    if goRight(checkRight) == 0:
        rightNode = Node(None)
    else: rightNode = Node(checkRight)
    if rightNode.array is not None:
        rightNode.misplaced = checkManhattan(rightNode.array)
        rightNode.parent = root
        if rightNode.parent is not None:
            rightNode.depth = root.depth+1
        rightNode.totalDistance = rightNode.misplaced + rightNode.depth

    # If the parent node can make children, enqueue the children to fringe and dequeue parent from fringe
    # Make child only if the child if the array does not already exist in repeatStates 
    if downNode.array or upNode.array or leftNode.array or rightNode.array is not None:
        fringeNodes.remove(root)
        if downNode.array is not None and downNode.array not in repeatStates:
            nodeCount+=1
            fringeNodes.append(downNode)
            repeatStates.append(downNode.array)
        if upNode.array is not None and upNode.array not in repeatStates:
            nodeCount+=1
            fringeNodes.append(upNode)
            repeatStates.append(upNode.array)
        if leftNode.array is not None and leftNode.array not in repeatStates:
            nodeCount+=1
            fringeNodes.append(leftNode)
            repeatStates.append(leftNode.array)
        if rightNode.array is not None and rightNode.array not in repeatStates:
            nodeCount+=1
            fringeNodes.append(rightNode)
            repeatStates.append(rightNode.array)

    if maxFringe < len(fringeNodes):
        maxFringe = len(fringeNodes)

    #__Prints all the fringes__
    # count = 0 
    # for x in fringeNodes:
    #     print("Count:",count)
    #     count+=1
    #     printArray(x.array)

    #__Prints all the repeated states__ 
    # count = 0 
    # for x in repeatStates:
    #     printArray(x)
    #     print("Count;",count)
    #     count+=1

    # Find the fringes with the smallest F(n). If multiple fringes with same F(n), expand fringes with the smallest H(n)
    minDistance = 1000 #Used as a tempto find the smallest distance - F(n)
    maxDepth = 0
    for x in fringeNodes:
        if minDistance > x.totalDistance:  
            minDistance = x.totalDistance
        if maxDepth < x.depth:
            maxDepth = x.depth

    #Iterate from the lowest depths that appear in the fringe and evaluate if it is equal to the smallest totalDistaince - F(n)
    for x in range(maxDepth+1):
        for y in fringeNodes:
            if y.depth == x and y.totalDistance == minDistance and y.array is not None:
                # printArray(y.array)
                # nodeCount+=1
                # print("Count:",nodeCount,"F(n):",y.totalDistance,"H(n):",y.depth,"G(n):",y.misplaced)
                manhattanHeuristic(y,nodeCount)
                

# generateViable(initialState)

root = Node(puzzle3)
# misplacedTiles(root,nodeCount)
# uniformCost(root,nodeCount)
manhattanHeuristic(root,nodeCount)

printRoute()
printTime()
printArray(initialState)



