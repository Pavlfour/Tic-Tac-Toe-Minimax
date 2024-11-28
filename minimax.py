# Console based game made by Pavlfour

from math import inf
from random import randint
from time import sleep

board = "---------" # This is the main board of the game

pc = None
human = None
first = -1

# This function below is needed because strings are immutable
def changeString(position,value):

    global board

    board = list(board)
    board[position] = value
    board = ''.join(board)


def printTable():

    print(board[:3]+'\n'+board[3:6]+'\n'+board[6:]+'\n')


def setGame():
    
    global pc,human,first

    while ((human != 'X' and human != 'O') or (first != 0 and first != 1)):
        try:
            human = input("Choose X or O: ").upper()
            first = int(input("Who plays first?(You = 0, PC = 1): "))
            
        except:
            print("Invalid input!")
    
    pc = 'O' if human == 'X' else 'X'


def win():
    
    # All possible winning states of the game
    winStates=[
         board[:3],
         board[3:6],
         board[6:],
         board[::3],
         board[1::3],
         board[2::3],
         board[::4],
         board[2:7:2]
         ]
    
    if 3*pc in winStates:
        return 1*(board.count('-')+1) # Utility function for maximizer +1*(remaining_empty_tiles + 1)
    elif 3*human in winStates:
        return -1*(board.count('-')+1) # Utility function for minimizer -1*(remaining_empty_tiles + 1)
    else:
        return 0


def minimax(player):
    
    if player == pc: # Maximizer
        best = [-1,-inf]
    else:
        best = [-1,inf] # Minimizer
        
    if not '-' in board or win():
        return [-1,win()]
    
    for index,position in enumerate(board):

        if position == '-':

            changeString(index,player)
            score = minimax(human if player == pc else pc)
            changeString(index,'-')
            score[0] = index
        
            if player == pc:
                if score[1] > best[1]:
                    best = score
            else:
                if score[1] < best[1]:
                    best = score
    
    return best


def aiTurn():

    if not '-' in board or win():
        return

    sleep(1)

    if board.count('-') == 9:
        changeString(randint(0,8),pc)
    else:
        move = minimax(pc)
        changeString(move[0],pc)


def playerTurn():

    if not '-' in board or win():
        return

    while True:
        try:
            choice = int(input("Choose a tile for your option[1...9]: "))
            if choice > 9 or choice < 1:
                raise Exception
            elif board[choice-1] == '-':
                changeString(choice-1,human)
                return
            else:
                raise Exception
        except:
            print("Try again")


# Initiate game
setGame()

# Main loop of the game
while not win() and '-' in board:
    printTable()
    if not first:
        playerTurn()
        printTable()
        first = -1
    print("Computer chooses: ")
    aiTurn()
    printTable()
    playerTurn()

# Results
if not win():
    printTable()
    print("It's a draw!")
elif win()>0:
    print("Ai took over the world!")
else:
    print("Mister lucky won!")
