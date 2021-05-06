import numpy as np
import random


class RandomAgent:
    '''
    Random agent that takes random actions all the time
    '''

    def __init__(self, game):
        self.game = game

    def get_action(self, state):
        action_set = self.game.available_edges
        idx = np.random.uniform(0, len(action_set))
        action = action_set[idx]
        return action
