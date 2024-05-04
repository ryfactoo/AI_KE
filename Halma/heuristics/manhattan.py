from heuristics.heuristic import Heuristic
import numpy as np
# import matplotlib.pyplot as plt

class Manhattan(Heuristic):

    def calculate(self, board, player):
        end_point = (0,0) if player == 2 else (15, 15)
        # self.print_heat_map(end_point,player)

        positions = board.getPlayerPositions(player)

        sum_heuristic = 0
        for position in positions:
            sum_heuristic = sum_heuristic + self.single_move(end_point, position, player)

        player = (player % 2) + 1
        positions = board.getPlayerPositions(player)
        end_point = (0,0) if player == 2 else (15, 15)

        for position in positions:
            sum_heuristic = sum_heuristic - self.single_move(end_point, position, player)

        return sum_heuristic

    def single_move(self, end_point, position, player):
        distance = abs(position[0] - end_point[0]) + abs(position[1] - end_point[1]) + 10

        if position in self.end_zone[player]:
            return distance - 10
        elif position == self.end_zone[(player % 2) + 1][0]:
            return distance + 30
        elif distance == 39:
            return distance + 20
        elif position in self.end_zone[(player % 2) + 1]:
            return distance + 5
        return distance

    # def print_heat_map(self,end_point,player):
    #     heatmap = np.zeros((16, 16))
    #
    #     for x in range(16):
    #         for y in range(16):
    #             heatmap[x, y] = self.single_move(end_point, (x, y), player)
    #
    #     plt.imshow(heatmap, cmap='hot', interpolation='nearest')
    #     plt.colorbar()
    #     plt.title('Heat Map')
    #     plt.xlabel('X')
    #     plt.ylabel('Y')
    #     plt.show()