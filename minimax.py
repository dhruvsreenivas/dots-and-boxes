import math
from copy import deepcopy


inf = 10000000


def evaluation(game):
    return game.p2.score - game.p1.score


def evaluation2(game):
    return game.p1.score - game.p2.score

# Function for AI to make move


def bestMove4(game):
    bestEdge = -inf
    move = None
    for i in range(len(game.available_edges)):
        action = game.available_edges[i]
        p1_point = game.p1.score
        p2_point = game.p2.score
        current = game.curr_player
        game.step(action)
        if game.curr_player != current:
            score = minimax4(game, 0, False, -inf, inf)
        else:
            score = minimax4(game, 0, True, -inf, inf)
        game.curr_player = current
        game.reverseStep(action, i)
        game.p1.score = p1_point
        game.p2.score = p2_point
        if score > bestEdge:
            bestEdge = score
            move = action
    return move


def minimax4(game, depth, isMaximizing, alpha, beta):
    if len(game.available_edges) == 0:
        return evaluation(game)
    elif isMaximizing:
        bestScore = -inf
        for i in range(0, len(game.available_edges)):
            action = game.available_edges[i]
            p1_point = game.p1.score
            p2_point = game.p2.score
            current = game.curr_player
            game.step(action)
            if game.curr_player != current:
                score = minimax4(game, depth + 1, False, alpha, beta)
            else:
                score = minimax4(game, depth + 1, True, alpha, beta)
            bestScore = max(bestScore, score)
            game.curr_player = current
            game.reverseStep(action, i)
            game.p1.score = p1_point
            game.p2.score = p2_point
            if bestScore >= beta:
                return bestScore
            alpha = max(alpha, score)
        return bestScore
    else:
        bestScore = inf
        for i in range(0, len(game.available_edges)):
            action = game.available_edges[i]
            p1_point = game.p1.score
            p2_point = game.p2.score
            current = game.curr_player
            game.step(action)
            if game.curr_player != current:
                score = minimax4(game, depth + 1, True, alpha, beta)
            else:
                score = minimax4(game, depth + 1, False, alpha, beta)
            bestScore = min(bestScore, score)
            game.curr_player = current
            game.reverseStep(action, i)
            game.p1.score = p1_point
            game.p2.score = p2_point
            if bestScore <= alpha:
                return bestScore
            beta = min(beta, score)
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
        return evaluation(game)
    elif isMaximizing:
        bestScore = -10000000
        current = evaluation(game)
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
        current = evaluation(game)
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
        return evaluation2(game)
    elif isMaximizing:
        bestScore = -inf
        current = evaluation2(game)
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
        current = evaluation2(game)
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


# Function for AI to make move
def bestMove(game):
    bestEdge = -inf
    move = None
    for i in range(len(game.available_edges)):
        current = game.curr_player
        gameCopy = deepcopy(game)
        action = gameCopy.available_edges[i]
        gameCopy.step(action)
        if game.curr_player != current:
            score = minimax4(gameCopy, 0, False, -inf, inf)
        else:
            score = minimax4(gameCopy, 0, True, -inf, inf)
        if score > bestEdge:
            bestEdge = score
            move = action
    return move


def minimax(game, depth, isMaximizing, alpha, beta):
    if len(game.available_edges) == 0:
        return evaluation(game)
    elif isMaximizing:
        bestScore = -inf
        for i in range(0, len(game.available_edges)):
            current = game.curr_player
            gameCopy = deepcopy(game)
            action = gameCopy.available_edges[i]
            gameCopy.step(action)
            if game.curr_player != current:
                score = minimax4(gameCopy, depth + 1, False, alpha, beta)
            else:
                score = minimax4(gameCopy, depth + 1, True, alpha, beta)
            bestScore = max(bestScore, score)
            if bestScore >= beta:
                return bestScore
            alpha = max(alpha, bestScore)
        return bestScore
    else:
        bestScore = inf
        for i in range(0, len(game.available_edges)):
            current = game.curr_player
            gameCopy = deepcopy(game)
            action = gameCopy.available_edges[i]
            gameCopy.step(action)
            if game.curr_player != current:
                score = minimax4(gameCopy, depth + 1, True, alpha, beta)
            else:
                score = minimax4(gameCopy, depth + 1, False, alpha, beta)
            bestScore = min(bestScore, score)
            if bestScore <= alpha:
                return bestScore
            beta = min(beta, bestScore)
        return bestScore
