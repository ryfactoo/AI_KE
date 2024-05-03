from abc import ABC, abstractmethod

class PlayerMode(ABC):
    @abstractmethod
    def move(self, board):
        pass