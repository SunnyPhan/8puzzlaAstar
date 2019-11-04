import random

arr = [
    [1,2,3],
    [4,5,6],
    [7,0,8]
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

def genRandom(arr):
    
    ranNumbers = [0,1,2,3,4,5,6,7,8]
    random.shuffle(ranNumbers)

    count = 0 
    length = len(arr)
    for x in range(length):
        for y in range(length):
            arr[x][y] = ranNumbers[count]
            count += 1


def printArray(arr):

    length = len(arr)
    for y in range(length):
        print(arr[y])


def zeroPosition(arr):

    length = len(arr)
    for x in range(length):
        for y in range(length):
            if arr[y][x] == 0:
                return y,x

def goLeft(arr):
    #VERY IMPORTANT, zeroPosition function returns as x and y
    y,x = zeroPosition(arr)
    #edge case
    if x == 0:
        print("You cannot go left any further")
        return
    temp = arr[y][x]
    arr[y][x] = arr[y][x-1]
    arr[y][x-1] = temp
    
def goRight(arr):
    #VERY IMPORTANT, zeroPosition function returns as x and y
    y,x = zeroPosition(arr)
    #edge case
    if x == 2:
        print("You cannot go right any further")
        return
    temp = arr[y][x]
    arr[y][x] = arr[y][x+1]
    arr[y][x+1] = temp

def goDown(arr):
    #VERY IMPORTANT, zeroPosition function returns as x and y
    y,x = zeroPosition(arr)
    #edge case
    if y == 2:
        print("You cannot go down any further")
        return
    temp = arr[y][x]
    arr[y][x] = arr[y+1][x]
    arr[y+1][x] = temp

def goUp(arr):
    #VERY IMPORTANT, zeroPosition function returns as x and y
    y,x = zeroPosition(arr)
    #edge case
    if y == 0:
        print("You cannot go up any further")
        return
    temp = arr[y][x]
    arr[y][x] = arr[y-1][x]
    arr[y-1][x] = temp

def main():
    
    print("Would you like a random board or easy board? Please R(random) or E(easy)")
    input1 = input()

    if input1 == "R":
        genRandom(arr)
        printArray(arr)
    else: 
        printArray(arr)


    while True:

        print("Where would you like to move the blank? Please enter U(up), D(down), L(left), R(right)")

        input1 = input()

        if input1 == "U":
            print("You entered up")
            goUp(arr)

        if input1 == "D":
            print("You entered down")
            goDown(arr)

        if input1 == "L":
            print("You entered left")
            goLeft(arr)

        if input1 == "R":
            print("You entered right")
            goRight(arr)

        printArray(arr)

        if arr == goalState:
            print("You win!")
            break

# Python program to introduce Binary Tree 

# A class that represents an individual node in a 
# Binary Tree 


class Node:
    def __init__(self,key):
        self.first = None
        self.second = None 
        self.third = None
        self.val = key

    

root = Node(1)
root.first = Node(2)
root.second = Node(3)
root.third = Node(4)



print(root.third.val)