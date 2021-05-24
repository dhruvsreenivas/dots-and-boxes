from copy import deepcopy


class State():
    def __init__(self, game, playerID):
        self.board = game
        self.playerID = playerID
        self.good_guy = game.p1 if playerID == game.p1.id else game.p2
        self.bad_guy = game.p2 if playerID == game.p1.id else game.p1

    def good_guy_turn(self):
        return self.playerID == self.board.curr_player.id

    def available_edges(self):
        return self.board.available_edges[:]

    def is_terminal(self):
        return len(self.board.available_edges) == 0

    def result(self):
        score = self.good_guy.score - self.bad_guy.score
        if score > 0:
            return 1
        elif score == 0:
            return 0
        else:
            return -1

    def take(self, action):
        board = deepcopy(self.board)
        edge = board.get_edge(action)
        board.step(edge)
        return State(board, self.playerID)
