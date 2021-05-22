from copy import deepcopy


class State():
    def __init__(self, game):
        self.board = game

    def get_legal_actions(self):
        '''
        Modify according to your game or
        needs. Constructs a list of all
        possible actions from current state.
        Returns a list.
        '''
        return self.board.available_edges[:]

    def is_game_over(self):
        '''
        Modify according to your game or
        needs. It is the game over condition
        and depends on your game. Returns
        true or false
        '''
        return len(self.board.available_edges) == 0

    def game_result(self):
        '''
        Modify according to your game or
        needs. Returns 1 or 0 or -1 depending
        on your state corresponding to win,
        tie or a loss.
        '''
        score = self.board.p1.score - self.board.p2.score
        if score > 0:
            return 1
        elif score == 0:
            return 0
        else:
            return -1

    def move(self, action):
        '''
        Modify according to your game or
        needs. Changes the state of your
        board with a new value. For a normal
        Tic Tac Toe game, it can be a 3 by 3
        array with all the elements of array
        being 0 initially. 0 means the board
        position is empty. If you place x in
        row 2 column 3, then it would be some
        thing like board[2][3] = 1, where 1
        represents that x is placed. Returns
        the new state after making a move.
        '''
        board = deepcopy(self.board)
        edge = board.get_edge(action)
        board.step(edge)
        return State(board)
