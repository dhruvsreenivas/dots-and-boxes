import argparse
from game import *
from algos.q_learning import QLearningAgent
from algos.random_agent import RandomAgent

parser = argparse.ArgumentParser(description='Dots and Boxes AI arguments')
# ======== Game Arguments ========
parser.add_argument('--board_dims', type=tuple, default=(3, 4),
                    help='dimensions of game board for Dots and Boxes')

# ======== Player Arguments ========
parser.add_argument('--p1_learning_method', default='q_learning',
                    help='learning method for player 1 (either "q_learning", "gts", or "mcts")')
parser.add_argument('--p2_learning_method', default=None,
                    help='learning method for player 2 (if None it will be random)')

# ======== Simulation Arguments ========
parser.add_argument('--n_train_games', type=int, default=1000,
                    help='number of games to train each agent')
parser.add_argument('--n_eval_games', type=int, default=400,
                    help='number of games to evaluate agent')

args = parser.parse_args()

# Board setup
m, n = args.board_dims
game = Game(m, n)

# need to implement stuff for other algos given args later on
q_learner = QLearningAgent(game)
other_q_learner = QLearningAgent(game)

# training q learning agent
for i in range(args.n_train_games):
    game.reset()
    state = game.get_state_rep()
    done = False

    while not done:
        if game.curr_player == game.p1:
            action = q_learner.get_action(state)
            reward, done = game.step(action)
            next_state = game.get_state_rep()
            q_learner.update(state, action, reward, next_state)
        else:
            action = other_q_learner.get_action(state)
            reward, done = game.step(action)
            next_state = game.get_state_rep()
            other_q_learner.update(state, action, reward, next_state)
        state = next_state

for i in range(args.n_eval_games):
    # evaluate against random agent
    random_agent = RandomAgent(game)
    game.reset()
    state = game.get_state_rep()
    done = False

    while not done:
        if game.curr_player == game.p1:
            action = q_learner.get_action(state)
            reward, done = game.step(action)
            next_state = game.get_state_rep()
            q_learner.update(state, action, reward, next_state)
        else:
            action = random_agent.get_action(state)
            _, done = game.step(action)
        state = next_state
