import numpy as np
import random
from collections import defaultdict


class QLearningAgent():
    '''
    Inputs:

    :param alpha: learning rate for Q function
    :param epsilon: parameter that regulates exploration vs exploitation
    :param gamma: discount factor in game
    '''

    def __init__(self, alpha=0.01, epsilon=0.1, gamma=0.99):
        self.lr = alpha
        self.eps = epsilon
        self.gamma = gamma

        self.q_table = defaultdict(lambda: defaultdict(int))

    def get_value(self, state, action):
        return self.q_table[state][action]

    def get_action(self, state, action_set):
        if np.random.uniform() < self.eps:
            # go full random
            idx = np.random.uniform(0, len(action_set))
            action = action_set[idx]
        else:
            # take best action according to current Q function
            idx = np.argmax([self.q_table[state][a] for a in action_set])
            action = action_set[idx]
        return action

    def update(self, old_state, old_action, reward, new_state):
        new_value = reward + max([self.q_table[new_state][a]
                                  for a in self.q_table[new_state].keys()])  # r + max_{a'} Q(s', a')
        old_value = self.q_table[old_state][old_action]
        self.q_table[old_state][old_action] = old_value + \
            self.lr * (new_value - old_value)
