import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def createModel():
    df = pd.read_csv("connect4_data.csv")

    winning_moves = df[df["result"] == 1]   # only keep rows where the move led to a win

    X = winning_moves.drop(["column_played", "result"], axis=1)
    y = winning_moves["column_played"]

    model = RandomForestClassifier()
    model.fit(X, y)

    return model

# The answer value is used to ask for what prediction you want. The value 0 is the most likely the value 6 is least likely to win the game.

def getPrediction(model, board, answer):
    flat = np.array(board).flatten().reshape(1, -1)
    return int(model.predict(flat)[0])


