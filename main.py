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
parser.add_argument('--training_learning_method',
                    default='q_learning', help='learning method to train player 1')
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

# training q learning agent through self-play (play against itself or another copy of itself)
if args.training_learning_method == 'q_learning':
    other_q_learner = QLearningAgent(game)
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
else:
    random_train_agent = RandomAgent(game)
    for i in range(args.n_train_games):
        game.reset()
        ob = game.get_state_rep()
        done = False

        while not done:
            if game.curr_player == game.p1:
                action = q_learner.get_action(state)
                reward, done = game.step(action)
                next_state = game.get_state_rep()
                q_learner.update(state, action, reward, next_state)
            else:
                action = random_train_agent.get_action(state)
                _, done = game.step(action)
            state = next_state

if args.p2_learning_method is None:
    random_eval_agent = RandomAgent(game)
    q_learner.eps = 0.0
    wins = 0
    for i in range(args.n_eval_games):
        # evaluate against random agent
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
                action = random_eval_agent.get_action(state)
                _, done = game.step(action)
            state = next_state

        if game.p1.get_score() > game.p2.get_score():
            wins += 1

    print(f'Number of wins for Q learner: {wins}')
    print(f'Number of games played: {args.n_eval_games}')

print('====== Q Learner Table Stats ======')
print(len(q_learner.q_table.keys()))
print(np.mean([len(q_learner.q_table[key].keys())
               for key in q_learner.q_table.keys()]))
