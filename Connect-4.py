import time
import main

board = [['-','-','-','-','-','-'],
         ['-','-','-','-','-','-'],
         ['-','-','-','-','-','-'],
         ['-','-','-','-','-','-'],
         ['-','-','-','-','-','-'],
         ['-','-','-','-','-','-'],
         ['-','-','-','-','-','-']]

first_player = True
model = main.createModel()




def get_user_input():
    column = int(input("Column: ")) - 1
    return column

def get_ai_input(value):
    prediction = main.getPrediction(model, board, value)
    return prediction

def play_turn(column):
    global first_player

    while True:

        free_slot = 0
        for y in range(7):
            if board[y][column] != '-':
                free_slot = free_slot + 1
                print(free_slot)

        if column >= 7 or column <= 0:
            print("Invalid Input")
            return False

        elif free_slot <= 6:
            if first_player:
                board[6 - free_slot][column] = 'x'
                first_player = False
            else:
                board[6 - free_slot][column] = 'o'
                first_player = True
        else:
            print("Row is Full, Select Again.")
            return False

        for x in range(len(board)):
            print(board[x])
            time.sleep(1)

        return True


# Main game loop
while True:
    success = False

    if first_player == True:
        while success == False:
            turn = get_user_input()
            success = play_turn(turn)

    else:
        number_of_tries = 0
        while success == False:
            if number_of_tries <= 6:
                turn = main.getPrediction(model, board, number_of_tries)
                success = play_turn(turn)
                number_of_tries += 1
            else:
                print("The board is full!")
