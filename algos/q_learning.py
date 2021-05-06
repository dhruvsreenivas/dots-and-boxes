import numpy as np
import random
from collections import defaultdict


class QLearningAgent:
    '''
    Inputs:

    :param alpha: learning rate for Q function
    :param epsilon: parameter that regulates exploration vs exploitation
    :param gamma: discount factor in game
    '''

    def __init__(self, game, alpha=0.01, epsilon=0.1, gamma=0.99):
        self.game = game
        self.lr = alpha
        self.eps = epsilon
        self.gamma = gamma

        self.q_table = defaultdict(lambda: defaultdict(float))
        # if state ends up being winning through trial and error, we set value of it to 1.0 (not super precise but we have to do it)

    def get_action(self, state):
        action_set = self.game.available_edges
        if np.random.uniform() < self.eps:
            # go full random
            idx = np.random.uniform(0, len(action_set))
            action = action_set[idx]
        else:
            # take best action according to current Q function
            if len(self.q_table[state].keys()) == 0:
                # no actions so you just go random
                idx = np.random.uniform(0, len(action_set))
                action = action_set[idx]
            else:
                idx = np.argmax([self.q_table[state][a] for a in action_set])
                action = action_set[idx]
        return action

    def update(self, old_state, old_action, reward, new_state):
        if new_state in self.q_table.keys() and len(self.q_table[new_state]) > 0:
            new_value = reward + self.gamma * max([self.q_table[new_state][a]
                                                   for a in self.q_table[new_state].keys()])  # r + gamma * max_{a'} Q(s', a')
        else:
            # in this case we have it defaulted to 0 for the Q values so we just get r
            new_value = reward

        old_value = self.q_table[old_state][old_action]
        # Q_new(s, a) = Q(s, a) + alpha (r + gamma * max_{a'} Q(s', a') - Q(s, a))
        self.q_table[old_state][old_action] = old_value + \
            self.lr * (new_value - old_value)
