import random
import math

# THIS WAS INSPIRED BY https://ai-boson.github.io/mcts/


class MonteNode():

    def __init__(self, state, parent=None, parent_edge=None):
        self.state = state

        self._w = 0
        self._l = 0
        self._n = 0

        self._parent = parent
        self._parent_edge = parent_edge
        self._children = []
        self._edges = self.state.available_edges()

    def _backpropagation(self, result):
        self._n += 1.
        if result == 1:
            self._w += 1
        elif result == -1:
            self._l += 1
        if self._parent:
            self._parent._backpropagation(result)

    def f(self, m, bigN, c):
        w, l, n = self._w, self._l, self._n
        return m * ((w - l) / n) + c * math.sqrt(2 * math.log(bigN) / n)

    def _select_child(self, c=0.1):
        m = 1 if self.state.good_guy_turn() else -1
        max_i = -1
        max_w = -math.inf
        for i in range(len(self._children)):
            weight = self._children[i].f(m, self._n, c)
            if weight > max_w:
                max_w = weight
                max_i = i

        return self._children[max_i]

    def _policy(self, moves):
        for e in moves:
            if e.would_take_box():
                return e
        options = []
        for e in moves:
            if not e.would_set_up():
                options.append(e)
        if options:
            return options[random.randint(0, len(options) - 1)]
        return moves[random.randint(0, len(moves) - 1)]

    def _simulation(self):
        node_state = self.state
        while True:
            if node_state.is_terminal():
                break
            edges = node_state.available_edges()
            edge = self._policy(edges)
            node_state = node_state.take(edge)
        return node_state.result()

    def _expansion(self):
        edge = self._edges.pop()
        next_state = self.state.take(edge)
        new_node = MonteNode(next_state, self, edge)
        self._children.append(new_node)
        return new_node

    def _selection(self):
        node = self
        while True:
            if node.state.is_terminal():
                break
            elif len(node._edges) == 0:
                node = node._select_child()
            else:
                return node._expansion()
        return node

    def best_edge(self, enumerations):
        for _ in range(enumerations):
            v = self._selection()
            result = v._simulation()
            v._backpropagation(result)
        return self._select_child(c=0.)._parent_edge
