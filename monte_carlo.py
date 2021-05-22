import numpy as np
from collections import defaultdict


# ALL OF THIS WAS COPIED FROM https://ai-boson.github.io/mcts/

# THIS IS NOT MY WORK

class MonteCarloTreeSearchNode():

    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def untried_actions(self):
        '''
        Returns the list of untried actions from a given state. For the first
        turn of our game there are 81 possible actions. For the second turn it
        is 8 or 9. This varies in our game.
        '''
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    def q(self):
        '''
        Returns the difference of wins - losses
        '''
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        '''
        Returns the number of times each node is visited.
        '''
        return self._number_of_visits

    def expand(self):
        '''
        From the present state, next state is generated depending on the action
        which is carried out. In this step all the possible child nodes
        corresponding to generated states are appended to the children array
        and the child_node is returned. The states which are possible from the
        present state are all generated and the child_node corresponding to
        this generated state is returned.
        '''

        action = self._untried_actions.pop()

        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        '''
        This is used to check if the current node is terminal or not. Terminal
        node is reached when the game is over.
        '''
        # NEED is_game_over() function in Game
        return self.state.is_game_over()

    def rollout(self):
        '''
        From the current state, entire game is simulated till there is an
        outcome for the game. This outcome of the game is returned. For example
        if it results in a win, the outcome is 1. Otherwise it is -1 if it
        results in a loss. And it is 0 if it is a tie. If the entire game is
        randomly simulated, that is at each turn the move is randomly selected
        out of set of possible moves, it is called light playout.
        '''
        current_rollout_state = self.state

        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()

    def backpropagate(self, result):
        '''
        In this step all the statistics for the nodes are updated. Untill the
        parent node is reached, the number of visits for each node is
        incremented by 1. If the result is 1, that is it resulted in a win,
        then the win is incremented by 1. Otherwise if result is a loss, then
        loss is incremented by 1.
        '''
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        '''
        All the actions are poped out of _untried_actions one by one. When it
        becomes empty, that is when the size is zero, it is fully expanded.
        '''
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):
        '''
        Once fully expanded, this function selects the best child out of the
        children array. The first term in the formula corresponds to
        exploitation and the second term corresponds to exploration.
        '''
        mult = 1
        if self.state.board.curr_player == self.state.board.p2:
            mult = -1
        choices_weights = [mult * ((c.q() / c.n())) + c_param *
                           np.sqrt((2 * np.log(self.n()) / c.n())) for c in
                           self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        '''
        Randomly selects a move out of possible moves. This is an example of
        random playout.
        '''
        for e in possible_moves:
            if e.would_take_box():
                return e
        options = []
        for e in possible_moves:
            if not e.would_set_up():
                options.append(e)
        if options:
            return options[np.random.randint(len(options))]
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        '''
        Selects node to run rollout.
        '''
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self, enumerations):
        '''
        This is the best action function which returns the node corresponding
        to best possible move. The step of expansion, simulation and
        backpropagation are carried out by the code above.
        '''
        simulation_no = enumerations
        for _ in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.)
