import random
import copy
import sys
import time 

sys.setrecursionlimit(10000)
start_time = time.time()
# print(sys.getrecursionlimit())

initialState = [
    [0,1,2],
    [4,5,3],
    [7,8,6]
    # [1,0,3],
    # [4,2,6],
    # [7,5,8]
]

# 11840 nodes depth 22 time 43.67 seconds
hard = [
    [8,5,0],
    [4,3,6],
    [1,2,7]
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
def makeChildren(parent,nodeCount):

    if parent.array == goalState:
        print(nodeCount)
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
                makeChildren(y,nodeCount)
                
                
# generateViable(initialState)

root = Node(hard)
makeChildren(root,nodeCount)

count = 0
for x in reversed(printFinished):
    print("Count:",count)
    count+=1
    printArray(x)

print("--- %s seconds ---" % (time.time() - start_time))


