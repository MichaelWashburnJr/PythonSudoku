"""
file: Sudoku.py
author: Michael Washburn Jr <michaeljr@citlink.net>
description: A self generating Sudoku game using
a tkinter based GUI.
"""
from copy import deepcopy
from random import randrange, shuffle
from tkinter import *

def init():
    """
    initializes the random sudoku board.
    Returns: board - A 2D array representation of the sudoku board
             key - a solved board
    """
    board = [None] * 9
    for n in range(0,len(board)):
        board[n] = [None] * 9
    board = randomize(board)
    board = solve(board)
    key = deepcopy(board)
    board = removeSpots(board)
    return board, key

def solutions(board):
    """
    finds out all possible solutions to a board configuration.
    - used to see if a board is valid
    Returns: solutions - a list of all possible solutions to
                         a single board.
    """
    solutions = []
    if isGoal(board) == True:
        solutions.append(deepcopy(board))
        return solutions
    else:
        for successor in getSuccessors(board):
            if valid(successor):
                solution = solve(successor)
                if solution == False:
                    return False
                elif (solution != None):
                    solutions.append(solution)
                elif len(solutions) > 1:
                    return False
        return solutions

def hint():
    """
    updates the board with one correct value.
    """
    global board
    global key
    if isGoal(board):
        Input.delete(0,END)
        Input.insert(0,"You Won!")
    else:
        lst = []
        for r in range(0,9):
            for c in range(0,9):
                if board[r][c] == None:
                    lst.append((r,c))
        n = randrange(0,len(lst))
        r, c = lst[n]
        board[r][c] = key[r][c]
        display.configure(text=toString(board))
        return board
    if isGoal(board):
        Input.delete(0,END)
        Input.insert(0,"You Won!")   
   
def removeSpots(board):
    """
    removes spaces from our key until removing one more space will
    give the board multiple solutions.
    """
    lst = []
    for r in range(0,9):
        for c in range(0,9):
            lst.append((r,c))
    shuffle(lst)
    for pair in lst:
        lst.remove(pair)
        r,c = pair
        if board[r][c] != None:
            board1 = deepcopy(board)
            board[r][c] = None
            boardcopy = deepcopy(board)
            if solutions(boardcopy) == False:
                board = deepcopy(board1)
    return board

def randomize(board):
    """
    Inserts random, valid, values into a blank board
    so that each new game is different from the last.
    """
    for r in range(0,9):
        x = 0
        while x < 1:
            c = randrange(0,9)
            if board[r][c] == None:
                bcopy = deepcopy(board)
                board[r][c] = randrange(1,10)
                if valid(board):
                    x += 1
                else:
                    board = bcopy
    return board
    
def solve(board):
    """
    solves a board for a valid configuration.
    Returns: solution - a completely solved board
    """
    if isGoal(board) == True:
        return board
    else:
        for successor in getSuccessors(board):
            if valid(successor):
                solution = solve(successor)
                if (solution != None):
                    return solution

def getSuccessors(board):
    """
    finds all successors of a board for backtracking
    algorithm
    """
    successors = []
    for r in range(0,9):
        for c in range(0,9):
            if board[r][c] == None:
                for n in range(1,10):
                    board[r][c] = n
                    successors.append(deepcopy(board))
                return successors
                            
                        
                                
                    
def isGoal(board):
    """
    Returns true if a board is a goal.
    """
    for row in board:
        for cell in row:
            if cell == None:
                return False
    if valid(board) == False:
        return False
    return True
        
                
def valid(board):
    """
    Returns if a board configuration is valid so far
    """
    boardcopy = deepcopy(board)
    for row in boardcopy:
        while len(row) > 0:
            cur = row.pop(0)
            if cur != None:
                if cur in row:
                    return False
    for c in range(0,9):
        col = mkCol(board, c)
        while len(col) > 0:
            cur = col.pop(0)
            if cur != None:
                if cur in col:
                    return False
    squares = []
    y = 0
    x = 0
    while len(squares) < 9:
        square = board[y][x:x+3] + board[y+1][x:x+3] + board[y+2][x:x+3]
        x+=3
        if x == 9:
            y += 3
            x = 0
        squares.append(deepcopy(square))
    for square in squares:
        while len(square) > 0:
            cur = square.pop(0)
            if cur != None:
                if cur in square:
                    return False
            
    return True

        
def mkCol(board,c):
    """
    Returns a list of all values in one column of the board
    """
    col = []
    i = 0
    while len(col) != 9:
        col.append(board[i][c])
        i +=1
    return col
        
            
def toString(board):
    """
    Turns a board configuration into a printable string.
     --used to display the board
    """
    if board == None:
        return "NONE"
    string = "      A  B  C     D  E  F    G  H  I\n \n"
    n = 0
    for row in board:
        n+=1
        string += "   " + str(n) + "      "
        for c in range(0,9):
            if row[c] == None:
                string += "X"
            else:
                string += str(row[c])
            string += "  "
            if (c+1) % 3 == 0:
                string +="   "
        if n %3 == 0:
            string += "\n"
        string += "\n"
    return string

def move():
    """
    uses user input to change values of the board.
    """
    global board
    global key
    inp = Input.get()
    if isGoal(board):
        Input.delete(0,END)
        Input.insert(0,"You Won!")
    elif inp == "You Won!":
        pass
    elif inp=="":
        pass
    elif len(inp) == 4:
        inp = inp.split()
        r = inp[0][1]
        c = inp[0][0]
        value = inp[1]
        if (ord(r) >= 49) and (ord(r) <= 57):
            r = int(r) - 1
            if (ord(c) >= 97) and (ord(c) <= 105) or (ord(c) <= 73) and (ord(c) >= 65 ):
                if (ord(c) >= 97) and (ord(c) <= 105):
                    c = ord(c) - 97
                elif (ord(c) <= 73) and (ord(c) >= 65 ):
                    c = ord(c) - 65
                if (value != "X") and (value != "x"):
                    if (ord(value) >= 49) and (ord(value) <= 57):
                        value = int(value)
                if (value == "X") or (value == "x"):
                    board[r][c] = None
                else:
                    board[r][c] = value
                display.configure(text=toString(board))
                Input.delete(0,END)
    if isGoal(board):
        Input.delete(0,END)
        Input.insert(0,"You Won!")
    return board, key


def newGame():
    """
    Makes a new game
    """
    global board
    global key
    board,key = init()
    display.configure(text=toString(board))
    return board,key
        
root = Tk()
root.wm_title("Sudoku")

board, key = init()

prompt = Label(root, text="Your Move: ")
prompt.grid(row=0, column=0,rowspan=2,sticky=E)

Input = Entry(root)
Input.grid(row=0,column=1,rowspan=2,sticky=E)
Input.insert(0,"Ex: A5 5")
Input.focus()

Submit = Button(root,text="Submit",command=move,width=8,height=3,bg="gray")
Submit.grid(row=0,column=2,rowspan=2,sticky=W)

Newgame = Button(root,text="New Game",command=newGame,width=14,bg="gray")
Newgame.grid(row=1,column=3,sticky=W)

Hint = Button(root,text="Hint",command=hint,width=14,bg="gray")
Hint.grid(row=0,column=3,sticky=E)

display = Label(root,text=toString(board),font=("Arial",16))
display.grid(row=2,columnspan=4)


root.mainloop()
        
