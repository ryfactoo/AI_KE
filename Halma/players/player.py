from players.player_mode import PlayerMode
import pyinputplus as pyip


class Player(PlayerMode):
    def move(self, board):
        return self.player_input()

    def player_input(self):
        start_row = pyip.inputInt("Start row (1 - 16): ", min=1, max=16)
        start_column = pyip.inputInt("Start column (1 - 16): ", min=1, max=16)
        end_row = pyip.inputInt("End row (1 - 16): ", min=1, max=16)
        end_column = pyip.inputInt("End column (1 - 16): ", min=1, max=16)

        return (start_row - 1, start_column - 1), (end_row - 1, end_column - 1)
