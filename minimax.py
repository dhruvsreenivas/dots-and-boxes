import math
from copy import deepcopy


inf = 10000000


def evaluation(game):
    return game.p2.score - game.p1.score


def evaluation2(game):
    return game.p1.score - game.p2.score


# Function for AI to make move
def bestMovePlayer2(game):
    bestEdge = -inf
    move = None
    for i in range(len(game.available_edges)):
        current = game.curr_player
        gameCopy = deepcopy(game)
        action = gameCopy.available_edges[i]
        gameCopy.step(action)
        if gameCopy.curr_player != current:
            score = minimaxPlayer2(gameCopy, 0, False)
        else:
            score = minimaxPlayer2(gameCopy, 0, True)
        if score > bestEdge:
            bestEdge = score
            move = action
    return move


def minimaxPlayer2(game, depth, isMaximizing):
    if len(game.available_edges) == 0:
        return evaluation(game)
    elif isMaximizing:
        bestScore = -10000000

        for i in range(0, len(game.available_edges)):
            current = game.curr_player
            gameCopy = deepcopy(game)
            action = gameCopy.available_edges[i]
            gameCopy.step(action)
            if gameCopy.curr_player != current:
                score = minimaxPlayer2(gameCopy, depth + 1, False)
            else:
                score = minimaxPlayer2(gameCopy, depth + 1, True)
            current = evaluation(game)
            if current >= game.beta:
                return current
            else:
                game.alpha = max(game.alpha, current)
            bestScore = max(bestScore, score)
        return bestScore
    else:
        bestScore = inf

        for i in range(0, len(game.available_edges)):
            current = game.curr_player
            gameCopy = deepcopy(game)
            action = gameCopy.available_edges[i]
            gameCopy.step(action)
            if gameCopy.curr_player != current:
                score = minimaxPlayer2(gameCopy, depth + 1, True)
            else:
                score = minimaxPlayer2(gameCopy, depth + 1, False)
            current = evaluation(game)
            if current <= game.alpha:
                return current
            else:
                game.beta = min(game.beta, current)
            bestScore = min(bestScore, score)

        return bestScore


# Function for AI to make move
def bestMovePlayer1(game):
    bestEdge = -inf
    move = None
    for i in range(len(game.available_edges)):
        current = game.curr_player
        gameCopy = deepcopy(game)
        action = gameCopy.available_edges[i]
        gameCopy.step(action)
        if gameCopy.curr_player != current:
            score = minimaxPlayer1(gameCopy, 0, False)
        else:
            score = minimaxPlayer1(gameCopy, 0, True)
        if score > bestEdge:
            bestEdge = score
            move = action
    return move


def minimaxPlayer1(game, depth, isMaximizing):
    if len(game.available_edges) == 0:
        return evaluation2(game)
    elif isMaximizing:
        bestScore = -inf
        for i in range(0, len(game.available_edges)):
            current = game.curr_player
            gameCopy = deepcopy(game)
            action = gameCopy.available_edges[i]
            gameCopy.step(action)
            if gameCopy.curr_player != current:
                score = minimaxPlayer1(gameCopy, depth + 1, False)
            else:
                score = minimaxPlayer1(gameCopy, depth + 1, True)
            current = evaluation2(game)
            if current >= game.beta:
                return current
            else:
                game.alpha = max(game.alpha, current)
            bestScore = max(bestScore, score)
        return bestScore
    else:
        bestScore = inf

        for i in range(0, len(game.available_edges)):
            current = game.curr_player
            gameCopy = deepcopy(game)
            action = gameCopy.available_edges[i]
            gameCopy.step(action)
            if gameCopy.curr_player != current:
                score = minimaxPlayer1(gameCopy, depth + 1, True)
            else:
                score = minimaxPlayer1(gameCopy, depth + 1, False)
            current = evaluation2(game)
            if current <= game.alpha:
                return current
            else:
                game.beta = min(game.beta, current)
            bestScore = min(bestScore, score)
        return bestScore
