from heuristics.heuristic import Heuristic
from heuristics.manhattan import Manhattan
from heuristics.heatmap_corners_to_corner import HeatmapCornersToCorner


class ManhattanHeatmapCornersToCorner(Heuristic):


    def __init__(self):
        super().__init__()
        self.heatmap = False
        self.manhattan = Manhattan()
        self.heatmapCornersToCorner = HeatmapCornersToCorner()


    def calculate(self, board, player):
        if self.heatmap or any(pos in self.end_zone[player] for pos in board.getPlayerPositions(player)):
            self.heatmap = True
            return self.heatmapCornersToCorner.calculate(board,player)
        else:
            return self.manhattan.calculate(board,player)
