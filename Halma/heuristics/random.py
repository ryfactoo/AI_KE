import random as pyRandom

from heuristics.heuristic import Heuristic


class Random(Heuristic):

    def calculate(self, board, player):
        return pyRandom.randint(0,500)