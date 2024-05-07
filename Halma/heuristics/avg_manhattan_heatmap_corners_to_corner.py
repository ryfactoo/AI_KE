from heuristics.heuristic import Heuristic
from heuristics.manhattan import Manhattan
from heuristics.heatmap_corners_to_corner import HeatmapCornersToCorner


class AVGManhattanHeatmapCornersToCorner(Heuristic):


    def __init__(self):
        super().__init__()
        self.manhattan = Manhattan()
        self.heatmapCornersToCorner = HeatmapCornersToCorner()


    def calculate(self, board, player):
        value = self.heatmapCornersToCorner.calculate(board,player)
        value = value + self.manhattan.calculate(board,player)
        return value/2
