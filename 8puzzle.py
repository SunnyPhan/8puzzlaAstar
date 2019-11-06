import random
import copy

initialState = [
    [5,1,3],
    [8,6,0],
    [2,7,4]
]

goalState = [
    [1,2,3],
    [4,5,6],
    [7,8,0]
]

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


# Print array function
def printArray(arr):

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
    #edge case
    if x == 0:
        # print("You cannot go left any further")
        return
    temp = copy.deepcopy(array[y][x])
    array[y][x] = array[y][x-1]
    array[y][x-1] = temp
    
def goRight(arr):
    #VERY IMPORTANT, zeroPosition function returns as x and y
    array = arr 
    y,x = zeroPosition(array)
    #edge case
    if x == 2:
        # print("You cannot go right any further")
        return
    temp = copy.deepcopy(array[y][x])
    array[y][x] = array[y][x+1]
    array[y][x+1] = temp

def goDown(arr):
    #VERY IMPORTANT, zeroPosition function returns as x and y
    array = arr
    y,x = zeroPosition(array)
    #edge case
    if y == 2:
        # print("You cannot go down any further")
        return
    temp = copy.deepcopy(array[y][x])
    array[y][x] = array[y+1][x]
    array[y+1][x] = temp

def goUp(arr):
    #VERY IMPORTANT, zeroPosition function returns as x and y
    array = arr
    y,x = zeroPosition(array)
    #edge case
    if y == 0:
        # print("You cannot go up any further")
        return
    temp = copy.deepcopy(array[y][x])
    array[y][x] = array[y-1][x]
    array[y-1][x] = temp

def main():
    
    print("Would you like a random board or easy board? Please R(random) or E(easy)")
    input1 = input()

    if input1 == "R":
        genRandom(initialState)
        printArray(initialState)
    else: 
        printArray(initialState)


    while True:

        print("Where would you like to move the blank? Please enter U(up), D(down), L(left), R(right)")

        input1 = input()

        if input1 == "U":
            print("You entered up")
            goUp(initialState)

        if input1 == "D":
            print("You entered down")
            goDown(initialState)

        if input1 == "L":
            print("You entered left")
            goLeft(initialState)

        if input1 == "R":
            print("You entered right")
            goRight(initialState)

        printArray(initialState)

        if initialState == goalState:
            print("You win!")
            break


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

repeatedStates = [] 

def makeChildren(arr,repeatedStates):

    # Initialize empty array to hold all states that have been observered

    #Make copies of previous array and each copy in a direction
    checkDown = copy.deepcopy(arr) 
    goDown(checkDown)
    checkUp = copy.deepcopy(arr)
    goUp(checkUp)
    checkLeft = copy.deepcopy(arr)
    goLeft(checkLeft)
    checkRight = copy.deepcopy(arr)
    goRight(checkRight)

    #Check numer of misplaced tiles for each direction 
    downCount = checkMisplaced(checkDown)       #0
    upCount = checkMisplaced(checkUp)           #1
    leftCount = checkMisplaced(checkLeft)       #2
    rightCount = checkMisplaced(checkRight)     #3

    # If the directed state exists within the repeatStates, set number of misplaced tiles to 1000 
    # so that the algo. does not choose that state when looking for smallest h(n)
    if checkDown in repeatedStates:
        downCount = 1000
    else: downCount = checkMisplaced(checkDown)

    if checkUp in repeatedStates:
        upCount = 1000
    else: upCount = checkMisplaced(checkUp)

    if checkLeft in repeatedStates:
        leftCount = 1000
    else: leftCount = checkMisplaced(checkLeft)

    if checkRight in repeatedStates:
        rightCount = 1000
    else: rightCount = checkMisplaced(checkRight)


    #Store misplaced counts in array 
    countArray = [downCount,upCount,leftCount,rightCount]

    #Find the index of the direction with smallest number of misplaced tiles
    for x in range(4):
        if countArray[x] == min(countArray) :
            smallIndex = x 
            break
    print("Small Index:",smallIndex)
    print("Count Array:",countArray)
    #Given index of direction w/ smallest number, set input array to array w/ given direction
    
    if smallIndex == 0:
        goDown(arr)
        temp = copy.deepcopy(arr)
        repeatedStates.append(temp)
    if smallIndex == 1:
        goUp(arr)
        temp = copy.deepcopy(arr)
        repeatedStates.append(temp)
    if smallIndex == 2:
        goLeft(arr)
        temp = copy.deepcopy(arr)
        repeatedStates.append(temp)
    if smallIndex == 3:
        goRight(arr)
        temp = copy.deepcopy(arr)
        repeatedStates.append(temp)



# genRandom(initialState)
count = 0 
while True:
    
    printArray(initialState)

    if initialState == goalState:
        print("Finished!")
        break
    
    count+=1
    makeChildren(initialState,repeatedStates)
    print("Run:",count)

# print("First run:")
# makeChildren(initialState,repeatedStates)
# printArray(initialState)

# print("Second run:")
# makeChildren(initialState,repeatedStates)
# printArray(initialState)

# print("Third run:")
# makeChildren(initialState,repeatedStates)
# printArray(initialState)

