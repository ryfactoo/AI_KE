from heuristics.heuristic import Heuristic
from heuristics.manhattan import Manhattan
from heuristics.heatmap_corners_to_corner_three_main_way import HeatmapCornersToCornerThreeMainWay
import numpy as np
import matplotlib.pyplot as plt

class AVGManhattanHeatmapCornersToCornerThreeMainWay(Heuristic):


    def __init__(self):
        super().__init__()
        self.manhattan = Manhattan()
        self.heatmapCornersToCornerThreeMainWay = HeatmapCornersToCornerThreeMainWay()


    def calculate(self, board, player):
        value = self.heatmapCornersToCornerThreeMainWay.calculate(board, player)
        value = value + self.manhattan.calculate(board,player)
        self.print_heat_map(player)
        return value/2

    def print_heat_map(self,player):
        heatmap = np.zeros((16, 16))

        for x in range(16):
            for y in range(16):
                heatmap[x, y] = self.manhattan.single_move((15,15),(x, y), player)
                heatmap[x, y] = heatmap[x, y] + self.heatmapCornersToCornerThreeMainWay.single_move((x, y), player)
                heatmap[x, y] = heatmap[x, y] / 2

        plt.imshow(heatmap, cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.title('Heat Map')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()
