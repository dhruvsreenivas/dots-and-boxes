import sys
import numpy as np
import random


class colors:
    BLUE = '\033[96m'
    RED = '\033[91m'
    REDBLOCK = '\033[101m'
    BLUEBLOCK = '\033[106m'
    ENDC = '\033[0m'


class Player():
    def __init__(self, id, color):
        self.id = id
        self.color = color
        self.score = 0

    def get_fill(self):
        return colors.REDBLOCK if self.color == colors.RED else colors.BLUEBLOCK

    def get_score(self):
        return self.score

    def give_point(self):
        self.score += 1

    def get_color(self):
        return self.color


class Edge():
    def __init__(self, point1, point2):
        self.edge = (point1, point2)
        self.player = None
        self.boxes = []

    def take_edge(self, player):
        if self.player is None:
            self.player = player

    def add_box(self, box):
        self.boxes.append(box)


class Box():
    def __init__(self, edges):
        self.edges = edges
        self.player = None

    def is_complete(self):
        return all([edge.player is not None for edge in self.edges])

    def take_box(self, player):
        if self.player is None:
            self.player = player

    def get_player(self):
        return self.player


class State():

    def get_legal_actions(self):
        '''
        Modify according to your game or
        needs. Constructs a list of all
        possible actions from current state.
        Returns a list.
        '''
        pass

    def is_game_over(self):
        '''
        Modify according to your game or
        needs. It is the game over condition
        and depends on your game. Returns
        true or false
        '''
        pass

    def game_result(self):
        '''
        Modify according to your game or
        needs. Returns 1 or 0 or -1 depending
        on your state corresponding to win,
        tie or a loss.
        '''
        pass

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
        pass


class Game():
    def __init__(self, m, n):
        self.board = np.zeros((m, n))
        self.horizontal_edges = []
        self.vertical_edges = []
        self.dimensions = (m, n)
        self.p1 = Player(1, colors.RED)
        self.p2 = Player(2, colors.BLUE)
        self.curr_player = self.p1

        # m rows, n columns
        # each row is of the form (n * k, (n+1)k - 1)
        for i in range(m):
            self.horizontal_edges.append(
                [Edge(i * n + j, i * n + j + 1) for j in range(n-1)])

        for i in range(m-1):
            self.vertical_edges.append(
                [Edge(i * n + j, (i+1) * n + j) for j in range(n)])

        self.boxes = []
        for i in range(m-1):
            row = []
            for j in range(n-1):
                edges = [self.horizontal_edges[i][j],
                         self.horizontal_edges[i+1][j],
                         self.vertical_edges[i][j],
                         self.vertical_edges[i][j+1]]
                box = Box(edges)

                for edge in box.edges:
                    edge.add_box(box)
                row.append(box)
            self.boxes.append(row)

        # at this point, all edges have boxes that they're a part of, and all
        # boxes are a collection of edges

        # now need a set of all available edges to start
        self.available_edges = []
        for edge_list in self.horizontal_edges + self.vertical_edges:
            for edge in edge_list:
                self.available_edges.append(edge)

    def print_board(self):
        (m, n) = self.dimensions
        h_lines = []

        top_line = "  "

        for i in range(m):
            line = str(i) + " "
            for j in range(n - 1):
                player = self.horizontal_edges[i][j].player
                line += "+ " + player.get_color() + "--" + colors.ENDC + \
                    " " if player is not None else "+    "
            h_lines.append(line + "+")

        v_lines = []
        for i in range(m - 1):
            line = "  "
            for j in range(n):
                filled = ""
                if j != n - 1 and self.boxes[i][j].is_complete():
                    filled = self.boxes[i][j].get_player().get_fill()
                player = self.vertical_edges[i][j].player
                line += player.get_color() + "| " + filled + "  " + colors.ENDC + " " + colors.ENDC if player is not None \
                    else "     "
            v_lines.append(line[:-4])

        v_lines.append('')

        board_lines = [val for pair in zip(
            h_lines, v_lines) for val in pair][:-1]

        for i in range(n):
            top_line += str(i) + "    "
        board_lines = [top_line] + board_lines

        print("\n" + "\n".join(board_lines) + "\n")

    def step(self, edge):
        box_taken = False
        reward = 0
        # make edge color whatever the current player is
        if edge in self.available_edges:
            self.available_edges.remove(edge)
            edge.take_edge(self.curr_player)
            for box in edge.boxes:
                if box.is_complete():
                    box_taken = True
                    box.take_box(self.curr_player)
                    self.curr_player.give_point()
                    reward = 1

            if not box_taken:
                self.curr_player = self.p1 if self.curr_player == self.p2 \
                    else self.p2

            return reward

    def play_game(self):
        while len(self.available_edges) > 0:
            self.print_board()
            i = random.randint(0, len(self.available_edges) - 1)
            edge = self.available_edges[i]
            self.step(edge)
        self.print_board()
        print(self.p1.score)
        print(self.p2.score)


if __name__ == '__main__':

    game = Game(3, 4)
    game.play_game()

# def main():
#     '''
#     This is the main() function. Initialize the root node and call the
#     best_action function to get the best node. This is not a member
#     function of the class. All the other functions are member function
#     of the class.
#     '''
#     root = MonteCarloTreeSearchNode(state=initial_state)
#     selected_node = root.best_action()
#     return
