from heuristics.heuristic import Heuristic
import numpy as np
import matplotlib.pyplot as plt

class HeatmapCornersToCorner(Heuristic):

    def __init__(self):
        super().__init__()
        self.heatmap = {}

        self.heatmap[2] = [[abs(x + y)*2 + abs(x - y) + 10 for x in range(16)] for y in range(16)]
        self.heatmap[1] = [[abs(32-x - y)*2 + abs(x - y) + 10 for x in range(16)] for y in range(16)]
        for i in range(0, 5):
            for j in range(0, 5):
                if i + j < 6:
                    self.heatmap[2][i][j] -= 10
                    self.heatmap[1][i][j] += 5
        self.heatmap[1][0][0] += 15
        self.heatmap[1][1][0] += 15
        self.heatmap[1][0][1] += 15
        self.heatmap[1][15][11] -= 4
        self.heatmap[1][14][11] -= 4
        self.heatmap[1][11][15] -= 4
        self.heatmap[1][11][14] -= 4
        self.heatmap[1][13][13] -= 2
        for i in range(1, 6):
            for j in range(1, 6):
                if i + j < 8:
                    self.heatmap[1][16-i][16-j] -= 10
                    self.heatmap[2][16-i][16-j] += 5
        self.heatmap[2][15][15] += 15
        self.heatmap[2][14][15] += 15
        self.heatmap[2][15][14] += 15
        self.heatmap[2][0][4] -= 4
        self.heatmap[2][1][4] -= 4
        self.heatmap[2][4][0] -= 4
        self.heatmap[2][4][1] -= 4
        self.heatmap[2][2][2] -= 2

    def calculate(self, board, player):
        # self.print_heat_map(player)

        positions = board.getPlayerPositions(player)

        sum_heuristic = 0
        for position in positions:
            sum_heuristic = sum_heuristic + self.single_move(position, player)

        player = (player % 2) + 1
        positions = board.getPlayerPositions(player)

        for position in positions:
            sum_heuristic = sum_heuristic - self.single_move(position, player)

        return sum_heuristic

    def single_move(self, position, player):
        return self.heatmap[player][position[0]][position[1]]

    def print_heat_map(self,player):
        heatmap = np.zeros((16, 16))

        for x in range(16):
            for y in range(16):
                heatmap[x, y] = self.single_move((x, y), player)

        plt.imshow(heatmap, cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.title('Heat Map')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()