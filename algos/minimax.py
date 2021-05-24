from copy import deepcopy
import math

inf = math.inf


def evaluationPlayer2(game):
    return game.p2.score - game.p1.score


def evaluationPlayer1(game):
    return game.p1.score - game.p2.score


# Function for AI to make move
def bestMoveP2(game):
    bestEdge = -inf
    move = None
    for i in range(len(game.available_edges)):
        current = game.curr_player
        gameCopy = deepcopy(game)
        action = gameCopy.available_edges[i]
        gameCopy.step(action)
        if gameCopy.curr_player != current:
            score = minimaxP2(gameCopy, 0, False, -inf, inf)
        else:
            score = minimaxP2(gameCopy, 0, True, -inf, inf)
        if score > bestEdge:
            bestEdge = score
            move = action
    return move


def minimaxP2(game, depth, isMaximizing, alpha, beta):
    if len(game.available_edges) == 0:
        return evaluationPlayer2(game)
    elif isMaximizing:
        bestScore = -inf
        for i in range(0, len(game.available_edges)):
            current = game.curr_player
            gameCopy = deepcopy(game)
            action = gameCopy.available_edges[i]
            gameCopy.step(action)
            if gameCopy.curr_player != current:
                score = minimaxP2(gameCopy, depth + 1, False, alpha, beta)
            else:
                score = minimaxP2(gameCopy, depth + 1, True, alpha, beta)
            if score >= beta:
                return score
            else:
                alpha = max(alpha, score)
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
                score = minimaxP2(gameCopy, depth + 1, True, alpha, beta)
            else:
                score = minimaxP2(gameCopy, depth + 1, False, alpha, beta)
            if score <= alpha:
                return score
            else:
                beta = min(beta, score)
            bestScore = min(bestScore, score)
        return bestScore


# Function for AI to make move
def bestMoveP1(game):
    bestEdge = -inf
    move = None
    for i in range(len(game.available_edges)):
        current = game.curr_player
        gameCopy = deepcopy(game)
        action = gameCopy.available_edges[i]
        gameCopy.step(action)
        if gameCopy.curr_player != current:
            score = minimaxP1(gameCopy, 0, False, -inf, inf)
        else:
            score = minimaxP1(gameCopy, 0, True, -inf, inf)
        if score > bestEdge:
            bestEdge = score
            move = action
    return move


def minimaxP1(game, depth, isMaximizing, alpha, beta):
    if len(game.available_edges) == 0:
        return evaluationPlayer1(game)
    elif isMaximizing:
        bestScore = -inf
        for i in range(0, len(game.available_edges)):
            current = game.curr_player
            gameCopy = deepcopy(game)
            action = gameCopy.available_edges[i]
            gameCopy.step(action)
            if gameCopy.curr_player != current:
                score = minimaxP1(gameCopy, depth + 1, False, alpha, beta)
            else:
                score = minimaxP1(gameCopy, depth + 1, True, alpha, beta)
            if score >= beta:
                return score
            else:
                alpha = max(alpha, score)
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
                score = minimaxP1(gameCopy, depth + 1, True, alpha, beta)
            else:
                score = minimaxP1(gameCopy, depth + 1, False, alpha, beta)
            if score <= alpha:
                return score
            else:
                beta = min(beta, score)
            bestScore = min(bestScore, score)
        return bestScore


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
        return evaluationPlayer2(game)
    elif isMaximizing:
        bestScore = -10000000
        current = evaluationPlayer2(game)
        if current >= game.beta:
            return current
        else:
            game.alpha = max(game.alpha, current)
        for i in range(0, len(game.available_edges)):
            current = game.curr_player
            gameCopy = deepcopy(game)
            action = gameCopy.available_edges[i]
            gameCopy.step(action)
            if gameCopy.curr_player != current:
                score = minimaxPlayer2(gameCopy, depth + 1, False)
            else:
                score = minimaxPlayer2(gameCopy, depth + 1, True)
            bestScore = max(bestScore, score)
        return bestScore
    else:
        bestScore = inf
        current = evaluationPlayer2(game)
        if current <= game.alpha:
            return current
        else:
            game.beta = min(game.beta, current)
        for i in range(0, len(game.available_edges)):
            current = game.curr_player
            gameCopy = deepcopy(game)
            action = gameCopy.available_edges[i]
            gameCopy.step(action)
            if gameCopy.curr_player != current:
                score = minimaxPlayer2(gameCopy, depth + 1, True)
            else:
                score = minimaxPlayer2(gameCopy, depth + 1, False)
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
        return evaluationPlayer1(game)
    elif isMaximizing:
        bestScore = -inf
        current = evaluationPlayer1(game)
        if current >= game.beta:
            return current
        else:
            game.alpha = max(game.alpha, current)
        for i in range(0, len(game.available_edges)):
            current = game.curr_player
            gameCopy = deepcopy(game)
            action = gameCopy.available_edges[i]
            gameCopy.step(action)
            if gameCopy.curr_player != current:
                score = minimaxPlayer1(gameCopy, depth + 1, False)
            else:
                score = minimaxPlayer1(gameCopy, depth + 1, True)
            bestScore = max(bestScore, score)
        return bestScore
    else:
        bestScore = inf
        current = evaluationPlayer1(game)
        if current <= game.alpha:
            return current
        else:
            game.beta = min(game.beta, current)
        for i in range(0, len(game.available_edges)):
            current = game.curr_player
            gameCopy = deepcopy(game)
            action = gameCopy.available_edges[i]
            gameCopy.step(action)
            if gameCopy.curr_player != current:
                score = minimaxPlayer1(gameCopy, depth + 1, True)
            else:
                score = minimaxPlayer1(gameCopy, depth + 1, False)
            bestScore = min(bestScore, score)
        return bestScore
