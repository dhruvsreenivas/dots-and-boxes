import sys
import numpy as np


class Game():
     def __init__(self, n):
         self.board = np.zeros(n, n)
         self.edges = []
         self.A = 0
         self.B = 0


