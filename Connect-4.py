import AI_Model
import time

board = [['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-']]

first_player = True
model = AI_Model.createModel()


def get_user_input():
    column = int(input("It is now your turn. Enter the column that you would like to play: ")) - 1
    return column


def play_turn(column):
    global first_player

    if column < 0 or column > 6:
        print("Invalid Input")
        return False

    if board[0][column] != '-':
        print("Column is full, select again.")
        return False

    # find the lowest empty slot in the column
    row = 5
    while board[row][column] != '-':
        row = row - 1

    if first_player:
        board[row][column] = 'x'
        first_player = False
    else:
        board[row][column] = 'o'
        first_player = True

    printBoard(board)
    return True


def printBoard(board):
    for x in range(len(board)):
        print(board[x])
    print()

# Main game loop
printBoard(board)

while True:
    if '-' not in board[0]:
        print("The board is full!")
        break

    if first_player:
        success = False
        while success == False:
            turn = get_user_input()
            success = play_turn(turn)
    else:
        turn = AI_Model.getPrediction(model, board, 2)
        play_turn(turn)
        time.sleep(2)