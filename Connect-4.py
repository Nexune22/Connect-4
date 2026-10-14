import time
import math

board = [['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-']]

SEARCH_DEPTH = 5

# -------------

def checkWinner(board, piece):
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

def isFull(board):
    for col in range(7):
        if board[0][col] == '-':
            return False
    return True

def isGameOver(board):
    return checkWinner(board, 'o') or checkWinner(board, 'x') or isFull(board)

# -------------

def generateMoves(board):
    order = sorted(range(7), key=lambda c: abs(c - 3))
    return [col for col in order if board[0][col] == '-']

def makeMove(board, col, piece):
    for row in range(5, -1, -1):
        if board[row][col] == '-':
            board[row][col] = piece
            return

def undoMove(board, col):
    for row in range(6):
        if board[row][col] != '-':
            board[row][col] = '-'
            return

# -------------

def score_window(window):
    ai = window.count('o')
    human = window.count('x')
    empty = window.count('-')

    if ai == 3 and empty == 1:
        return 100
    if ai == 2 and empty == 2:
        return 10
    if human == 3 and empty == 1:
        return -80
    if human == 2 and empty == 2:
        return -8
    return 0

def evaluate_connect_four(board):
    score = 0

    # Award centre column (most winning lines)
    score += 3 * [board[row][4] for row in range(6)].count('o')
    score -= 3 * [board[row][4] for row in range(6)].count('x')
    
    # Score by horizontal
    for row in range(6):
        for col in range(4):
            score += score_window([board[row][col + i] for i in range(4)]) 
    # By vertical
    for row in range(3):
        for col in range(7):
            score += score_window([board[row + i][col] for i in range(4)]) 
    # By diagonal right and left
    for row in range(3):
        for col in range(4):
            score += score_window([board[row + i][col + i] for i in range(4)])
            score += score_window([board[row + 3 - i][col + i] for i in range(4)])

    return score

def alpha_beta_connect_four(board, depth, alpha, beta, is_maximising):
    if checkWinner(board, 'o'):
        return 1_000_000 + depth
    if checkWinner(board, 'x'):
        return -1_000_000 - depth
    if isFull(board):
        return 0
    if depth == 0:
        return evaluate_connect_four(board)

    if is_maximising:
        best_score = -math.inf
        for move in generateMoves(board):
            makeMove(board, move, 'o')
            score = alpha_beta_connect_four(board, depth - 1, alpha, beta, False)
            undoMove(board, move)
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = math.inf
        for move in generateMoves(board):
            makeMove(board, move, 'x')
            score = alpha_beta_connect_four(board, depth - 1, alpha, beta, True)
            undoMove(board, move)
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score

def choose_ai_move(board, depth=SEARCH_DEPTH):
    best_score = -math.inf
    best_move = None
    for move in generateMoves(board):
        makeMove(board, move, 'o')
        score = alpha_beta_connect_four(board, depth - 1, -math.inf, math.inf, False)
        undoMove(board, move)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

# -------------

loop = True
FirstPlayer = True

while loop:
    if FirstPlayer:
        column = int(input("Column: ")) - 1
        if column >= 7 or column < 0:
            print("Invalid input.")
            continue
    else:
        print("AI is thinking")
        column = choose_ai_move(board)

    free_slot = 0

    for y in range(6):
        if board[y][column] != '-':
            free_slot = free_slot + 1
 
    if free_slot < 6:
        if FirstPlayer:
            board[5 - free_slot][column] = 'x'
            FirstPlayer = False
        else:
            board[5 - free_slot][column] = 'o'
            FirstPlayer = True
    else:
        print("Column is Full, Select Again.")
        continue
 
    for x in range(len(board)):
        print(board[x])
 
    if checkWinner(board, 'x'):
        print("You win!")
        loop = False
    elif checkWinner(board, 'o'):
        print("The AI wins!")
        loop = False
    elif isFull(board):
        print("It's a draw!")
        loop = False


