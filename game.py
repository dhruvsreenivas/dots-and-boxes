import sys
import numpy as np


class Edge():
    def __init__(self, point1, point2):
        self.edge = (point1, point2)
        self.color = None
        self.boxes = []

    def take_edge(self, player):
        if self.color is None:
            self.color = player

    def add_box(self, box):
        self.boxes.append(box)


class Box():
    def __init__(self, edges):
        self.edges = edges
        self.player = None

    def is_complete(self):
        return all([edge.color is not None for edge in self.edges])

    def take_box(self, player):
        if self.player is None:
            self.player = player


class Game():
    def __init__(self, m, n):
        self.board = np.zeros((m, n))
        self.horizontal_edges = []
        self.vertical_edges = []

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
            for j in range(n-1):
                l = [self.horizontal_edges[i][j], self.horizontal_edges[i+1]
                     [j], self.vertical_edges[i][j], self.vertical_edges[i][j+1]]
                box = Box(l)
                self.boxes.append(box)

                for edge in box.edges:
                    edge.add_box(box)

        # at this point, all edges have boxes that they're a part of, and all boxes are a collection of edges

        # now need a set of all available edges to start
        self.available_edges = []
        for edge_list in self.horizontal_edges + self.vertical_edges:
            for edge in edge_list:
                self.available_edges.append(edge)

        self.A = 0
        self.B = 0
        self.curr_player = 0

    def step(self, edge):
        box_taken = False
        # make edge color whatever the current player is
        if edge in self.available_edges:
            self.available_edges.remove(edge)

            edge.take_edge(self.curr_player)
            for box in edge.boxes:
                if box.is_complete:
                    box_taken = True
                    box.take_box(self.curr_player)
                    if self.curr_player == 0:
                        self.A += 1
                    else:
                        self.B += 1

        self.curr_player = not self.curr_player if not box_taken else self.curr_player


if __name__ == '__main__':
    game = Game(2, 3)
    for edge_list in game.horizontal_edges:
        for edge in edge_list:
            # print(type(edge))
            print(edge.edge)
    print('------')
    for edge_list in game.vertical_edges:
        for edge in edge_list:
            # print(type(edge))
            print(edge.edge)

    print('box check and shit')
    for box in game.boxes:
        edge_list = box.edges
        for edge in edge_list:
            print(edge.edge)

        print('------')

    print([edge.edge for edge in game.available_edges])
