import argparse
import time
import board as game_board
import players.player as human_player
import players.computer_best_current_move as CBMC
import players.computer_minmax_alpha_beta as CMMAB
import players.computer_minmax as CMM
import heuristics.manhattan as manhattan
import heuristics.random as randomHeuristic
import heuristics.heatmap_corners_to_corner as cornersHeuristic
import heuristics.heatmap_corners_to_corner_three_main_way as cornersHeuristicThreeMainWay
import heuristics.manhattan_heatmap_corners_to_corner as manhattanHeatmapCornersToCoerner
import heuristics.avg_manhattan_heatmap_corners_to_corner as avg_manhattan_heatmap_corners_to_corner
import heuristics.avg_manhattan_heatmap_corners_to_corner_three_main_way as avg_manhattan_heatmap_corners_to_corner_three_main_way


class Game:
    def player_mode(self, player, heuristic_type, player_char, minmax_depth):

        if player == "P":
            return human_player.Player()
        elif player == "CBCM":
            heuristic = self.heuristic_mode(heuristic_type)
            return CBMC.ComputerBestCurrentMove(heuristic, player_char)
        elif player == "CMM":
            heuristic = self.heuristic_mode(heuristic_type)
            return CMM.ComputerMinmax(heuristic, player_char, minmax_depth)
        elif player == "CMMAB":
            heuristic = self.heuristic_mode(heuristic_type)
            return CMMAB.ComputerMinmaxAlphaBeta(heuristic, player_char, minmax_depth)

    def heuristic_mode(self, heuristic):

        if (heuristic == "M"):
            return manhattan.Manhattan()
        elif (heuristic == "R"):
            return randomHeuristic.Random()
        elif (heuristic == "HCC"):
            return cornersHeuristic.HeatmapCornersToCorner()
        elif (heuristic == "HCC3MW"):
            return cornersHeuristicThreeMainWay.HeatmapCornersToCornerThreeMainWay()
        elif (heuristic == "M+HCC"):
            return manhattanHeatmapCornersToCoerner.ManhattanHeatmapCornersToCorner()
        elif (heuristic == "AVGMHCC"):
            return avg_manhattan_heatmap_corners_to_corner.AVGManhattanHeatmapCornersToCorner()
        elif (heuristic == "AVGMHCC3MW"):
            return avg_manhattan_heatmap_corners_to_corner_three_main_way.AVGManhattanHeatmapCornersToCornerThreeMainWay()

    def init(self, board):
        if board:
            self.board.board = board
        else:
            self.board.init_game()

    def start_game(self, p1, p2, heuristic_p1, heuristic_p2, minmax_depth=2, board=None):
        self.board = game_board.Board()

        self.init(board)

        self.p1 = self.player_mode(p1, heuristic_p1, 1, minmax_depth)
        self.p2 = self.player_mode(p2, heuristic_p2, 2, minmax_depth)

        self.game()

    def game(self):
        round = 1
        start_time = 0
        end_time = 0

        while (True):
            while (True):
                self.board.print_board()
                print("Player 1 (X)")
                print("Round: " + str(round))
                start_time = time.time()
                move = self.p1.move(self.board)
                end_time = time.time()
                moves = self.board.possible_movements(move[0])
                if move[1] in moves:
                    self.board.print_possible_move(1)
                    print(move)
                    print(end_time - start_time)
                    self.board.move_piece(move[0], move[1])
                    round = round + 1
                    break
                print("Invalid move")
            if self.board.is_end(2):
                self.board.print_board()
                print("Round: " + str(round))
                print("WIN Player 1")
                break

            # time.sleep(1)

            while (True):
                self.board.print_board()
                print("Player 2 (O)")
                print("Round: " + str(round))
                start_time = time.time()
                move = self.p2.move(self.board)
                end_time = time.time()
                moves = self.board.possible_movements(move[0])
                if move[1] in moves:
                    self.board.print_possible_move(1)
                    print(move)
                    print(end_time - start_time)
                    self.board.move_piece(move[0], move[1])
                    round = round + 1
                    break
                print("Invalid move")
            if self.board.is_end(1):
                self.board.print_board()
                print("Round: " + str(round))
                print("WIN Player 2")
                break

            # time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-p1", "--player1",
                        choices=['P', 'CBCM', 'CMM', 'CMMAB'],
                        help="Player 1 mode : P - Player , CBCM - Computer best current move , CMM - Computer minmax , CMMAB - Computer minmax alpha beta",
                        required=True)

    parser.add_argument("-h1", "--heuristicP1",
                        choices=['M', 'R', 'HCC','HCC3MW','M+HCC','AVGMHCC','AVGMHCC3MW'],
                        help="Heuristic for p1: M - Manhattan heuristic, R - Random heuristic",
                        default='M')

    parser.add_argument("-p2", "--player2",
                        choices=['P', 'CBCM', 'CMM', 'CMMAB'],
                        help="Player 2 mode :"
                             " M - Manhattan heuristic,"
                             " R - Random heuristic"
                             " HCC - Heatmap heuristic corners to corner"
                             " HCC3MW - Heatmap corners to corner three main way heuristic"
                             " M+HCC - Manhattan start game, when first pawn is in end zone then heatmap corners to corner"
                             " AVGMHCC - AVG manhattan and heatmap corners to corner"
                             " AVGMHCC3MW - AVG manhattan and heatmap corners to corner three main way",
                        required=True)

    parser.add_argument("-h2", "--heuristicP2",
                        choices=['M', 'R', 'HCC','HCC3MW','M+HCC','AVGMHCC','AVGMHCC3MW'],
                        help="Heuristic for p2:"
                             " M - Manhattan heuristic,"
                             " R - Random heuristic"
                             " HCC - Heatmap heuristic corners to corner"
                             " HCC3MW - Heatmap corners to corner three main way heuristic"
                             " M+HCC - Manhattan start game, when first pawn is in end zone then heatmap corners to corner"
                             " AVGMHCC - AVG manhattan and heatmap corners to corner"
                             " AVGMHCC3MW - AVG manhattan and heatmap corners to corner three main way",
                        default='M')

    parser.add_argument("-md", "--minmaxdepth",
                        type=int,
                        help="Minmax depth",
                        default=2)

    args = parser.parse_args()

    game = Game()

    game.start_game(args.player1, args.player2, args.heuristicP1, args.heuristicP2, args.minmaxdepth)
