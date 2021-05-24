import numpy as np
import random
import objects.player as play
import objects.colors as colors
from algos.monte_carlo import MonteNode
import state
from copy import deepcopy
from algos.minimax import bestMoveP1, bestMoveP2
from algos.minimax import bestMovePlayer1, bestMovePlayer2
import math


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

    def would_take_box(self):
        for box in self.boxes:
            if box.count() == 3:
                return True
        return False

    def would_set_up(self):
        for box in self.boxes:
            if box.count() == 2:
                return True
        return False


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

    def count(self):
        return sum([1 for e in self.edges if e.player is not None])


class Game():

    def __init__(self, m, n):
        self.board = np.zeros((m, n))
        self.horizontal_edges = []
        self.vertical_edges = []
        self.dimensions = (m, n)
        self.p1 = play.Player(1, colors.RED)
        self.p2 = play.Player(2, colors.BLUE)
        self.curr_player = self.p1

        self.alpha = -math.inf
        self.beta = math.inf

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

    #
    # ****************HELPERS****************
    #
    def get_state_rep(self):
        rep = ''
        for edge_list in self.horizontal_edges + self.vertical_edges:
            for edge in edge_list:
                if edge.player is None:
                    rep += '0'
                elif edge.player == self.p1:
                    rep += '1'
                else:
                    rep += '-1'
        return rep

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
                line += player.get_color() + "| " + filled + "  " + \
                    colors.ENDC + " " + colors.ENDC \
                    if player is not None else "     "
            v_lines.append(line[:-4])

        v_lines.append('')

        board_lines = [val for pair in zip(
            h_lines, v_lines) for val in pair][:-1]

        for i in range(n):
            top_line += str(i) + "    "
        board_lines = [top_line] + board_lines

        print("\n".join(board_lines) + "\n")

    def get_edge(self, edge):
        for e in self.available_edges:
            if edge.edge == e.edge:
                return e
        assert 1 == 0

    def reset(self):
        m, n = self.board.shape
        self.board = np.zeros((m, n))
        self.horizontal_edges = []
        self.vertical_edges = []
        self.dimensions = (m, n)
        self.p1 = play.Player(1, colors.RED)
        self.p2 = play.Player(2, colors.BLUE)
        self.curr_player = self.p1
        self.alpha = -10000000
        self.beta = 10000000

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
    #
    # ****************END HELPERS****************
    #

    #
    # ****************ALGORITHMS****************
    #

    def get_input(self):
        edge = None
        while edge is None:
            try:
                x = int(input('First number: '))
                y = int(input('Second number: '))
                e = Edge(x, y)
                edge = self.get_edge(e)
            except Exception:
                print('Try Again')
        return edge

    def monte_carlo(self, enumerations):
        root = MonteNode(state.State(deepcopy(self), self.curr_player.id))
        action = root.best_edge(enumerations)
        return self.get_edge(action)

    def minimax(self):
        if self.curr_player.id == 1:
            action = bestMoveP1(self)
        else:
            action = bestMoveP2(self)
        return self.get_edge(action)

    def minimaxExp(self):
        if self.curr_player.id == 1:
            action = bestMovePlayer1(self)
        else:
            action = bestMovePlayer2(self)
        return self.get_edge(action)

    def policy(self):
        for e in self.available_edges:
            if e.would_take_box():
                return e
        options = []
        for e in self.available_edges:
            if not e.would_set_up():
                options.append(e)
        if options:
            return options[random.randint(0, len(options) - 1)]
        k = random.randint(0, len(self.available_edges) - 1,)
        return self.available_edges[k]

    def random(self):
        i = random.randint(0, len(self.available_edges) - 1)
        return self.available_edges[i]
    #
    # ****************END ALGORITHMS****************
    #

    #
    # ****************GAME PLAY****************
    #

    def step(self, edge):
        box_taken = False
        reward = 0
        # make edge color whatever the current player is
        self.available_edges.remove(edge)
        edge.take_edge(self.curr_player)
        for box in edge.boxes:
            if box.is_complete():
                box_taken = True
                box.take_box(self.curr_player)
                self.curr_player.give_point()
                reward += 1

        if not box_taken:
            self.curr_player = self.p1 if self.curr_player == self.p2 \
                else self.p2

        done = len(self.available_edges) == 0
        return reward, done

    def play_game(self):
        while len(self.available_edges) > 0:

            if self.curr_player == self.p1:
                edge = self.policy()
            else:
                edge = self.monte_carlo(200)
            self.step(edge)

        self.print_board()
        return self.p1.score - self.p2.score
    #
    # ****************END GAME PLAY****************
    #


if __name__ == '__main__':
    wins = 0
    ties = 0
    losses = 0
    for _ in range(10):
        game = Game(4, 4)
        score = game.play_game()
        if score > 0:
            wins += 1
        elif score == 0:
            ties += 1
        else:
            losses += 1
    print('Player 1: ' + str(wins) + ' wins, ' + str(losses) +
          ' losses, ' + str(ties) + ' ties.\n')
    print('Player 2: ' + str(losses) + ' wins, ' + str(wins) +
          ' losses, ' + str(ties) + ' ties.\n')
