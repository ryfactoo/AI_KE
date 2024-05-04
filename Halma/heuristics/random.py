import random as pyRandom

from heuristics.heuristic import Heuristic


class Random(Heuristic):

    def calculate(self, board, player):
        positions = board.getPlayerPositions(player)

        if self.end_zone[(player %2) +1][0] in positions:
            return pyRandom.randint(100, 500) ^ 2

        if tuple(self.end_zone[(player %2) +1]) in positions:
            return pyRandom.randint(10,500)^2

        return pyRandom.randint(0,500)