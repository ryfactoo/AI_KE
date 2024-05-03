from abc import ABC, abstractmethod

class Heuristic(ABC):

    def __init__(self):
        self.end_zone = {1:[], 2:[]}

        for i in range(1, 6):
            for j in range(1, 6):
                if i + j < 8:
                    self.end_zone[1].append((16-i,16-j))
        for i in range(0, 5):
            for j in range(0, 5):
                if i + j < 6:
                    self.end_zone[2].append((i,j))

    @abstractmethod
    def calculate(self, board, player):
        pass