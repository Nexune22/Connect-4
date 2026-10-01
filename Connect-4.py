board = [['-','-','-','-','-','-'],
         ['-','-','-','-','-','-'],
         ['-','-','-','-','-','-'],
         ['-','-','-','-','-','-'],
         ['-','-','-','-','-','-'],
         ['-','-','-','-','-','-'],
         ['-','-','-','-','-','-']]

loop = True
FirstPlayer = True

while loop:
    column = int(input("Column: ")) -1
    free_slot = 0

    for y in range(7):
        if board[y][column] != '-':
            free_slot = free_slot +1
            print(free_slot)

    if column >=7 or column <= 0:
        print("Invalid Input")
    elif free_slot <=6:
        if FirstPlayer:
            board[6-free_slot][column] = 'x'
            FirstPlayer = False
        else:
            board[6 - free_slot][column] = 'o'
            FirstPlayer = True
    else:
        print("Row is Full, Select Again.")

    for x in range(len(board)):
        print(board[x])