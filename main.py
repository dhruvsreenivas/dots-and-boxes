import argparse
from game import *
from algos import *

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
