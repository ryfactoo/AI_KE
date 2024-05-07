from heuristics.heuristic import Heuristic
from heuristics.manhattan import Manhattan
from heuristics.heatmap_corners_to_corner_three_main_way import HeatmapCornersToCornerThreeMainWay


class AVGManhattanHeatmapCornersToCornerThreeMainWay(Heuristic):


    def __init__(self):
        super().__init__()
        self.manhattan = Manhattan()
        self.heatmapCornersToCornerThreeMainWay = HeatmapCornersToCornerThreeMainWay()


    def calculate(self, board, player):
        value = self.heatmapCornersToCornerThreeMainWay.calculate(board, player)
        value = value + self.manhattan.calculate(board,player)
        return value/2
