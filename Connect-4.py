import AI_Model
import time

board = [['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-']]


colours = {
    'x': "\033[31m",  # red
    'o': "\033[32m",  # green
}

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

    print_board(board)
    return True

def check_winner(board, piece):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for row in range(6):
        for col in range(7):
            for dr, dc in directions:
                end_r, end_c = row + 3 * dr, col + 3 * dc
                if not (0 <= end_r < 6 and 0 <= end_c < 7):
                    continue
                if all(board[row + i * dr][col + i * dc] == piece for i in range(4)):
                    return True
    return False


def print_board(board):
    print("\033[36m1   2   3   4   5   6   7\033[0m")
    print()
    for x in range(len(board)):
        for y in range(len(board[x])):
            code = colours.get(board[x][y], "")  # no code for letters not in the dictionary
            print(code, board[x][y], "\033[0m   ", sep="", end="")
            code = ""
        print()
    print()
    print("\033[93m-------------------------\033[0m")
    print()

# Main game loop
print_board(board)

while True:
    if '-' not in board[0]:
        print("The board is full!")
        break

    if first_player:
        success = False
        while success == False:
            turn = get_user_input()
            success = play_turn(turn)

        if check_winner(board, 'x'):
            print("Player 1 won congrats!")
            break


    else:
        turn = AI_Model.getPrediction(model, board, 2)
        play_turn(turn)

        if check_winner(board, 'o'):
            print("The AI won!")
            break
        time.sleep(2)