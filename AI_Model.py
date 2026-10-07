import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def swap_view(digits, player):
    # Make the mover's pieces always 1 and the opponent's always 2
    if player == 2:
        return digits.translate(str.maketrans("12", "21"))
    return digits


def createModel():
    df = pd.read_csv("AITrainingData.csv", dtype={"flat_board": str})

    # Turn "#1000..." into 42 numbers, from the mover's point of view
    boards = [
        [int(d) for d in swap_view(b[1:], p)]
        for b, p in zip(df["flat_board"], df["player"].astype(int))
    ]
    X = np.array(boards)
    y = df["column_played"]

    model = RandomForestClassifier()
    model.fit(X, y)
    return model


# board: 6x7 list of 0 (empty), 1 or 2. player: 1 or 2 (who is moving).
# answer: 0 = best column, 1 = second best, and so on.
def getPrediction(model, board, player, answer=0):
    # turn the board into a string of 0s, 1s and 2s
    flat = ""
    for row in board:
        for square in row:
            if square == 'x':
                flat = flat + "1"
            elif square == 'o':
                flat = flat + "2"
            else:
                flat = flat + "0"

    x = np.array([int(d) for d in swap_view(flat, player)]).reshape(1, -1)

    probs = model.predict_proba(x)[0]
    order = np.argsort(probs)[::-1]

    # best columns first, skipping any that are full
    legal = []
    for i in order:
        column = int(model.classes_[i])
        if board[0][column] == '-':
            legal.append(column)

    return legal[answer]