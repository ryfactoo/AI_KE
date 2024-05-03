import argparse
import board as game_board
import players.player as human_player
import players.computer_best_current_move as CBMC
import players.computer_minmax as CMM
import heuristics.manhattan as manhattan
import heuristics.random as randomHeuristic

import time

class Game:
    def player_mode(self, player, heuristic_type ,player_char, minmax_depth):

        if(player == "P"):
            return human_player.Player()
        elif(player == "CBCM"):
            heuristic = self.heuristic_mode(heuristic_type)
            return CBMC.ComputerBestCurrentMove(heuristic, player_char)
        elif(player == "CMM"):
            heuristic = self.heuristic_mode(heuristic_type)
            return CMM.ComputerMinmax(heuristic, player_char, minmax_depth)

    def heuristic_mode(self, heuristic):

        if(heuristic == "M"):
            return manhattan.Manhattan()
        elif(heuristic == "R"):
            return randomHeuristic.Random()

    def init(self, board):
        if board:
            self.board.board = board
        else:
            self.board.init_game()

    def start_game(self, p1, p2, heuristic_p1, heuristic_p2, minmax_depth = 2, board = None):
        self.board = game_board.Board()

        self.init(board)

        self.p1 = self.player_mode(p1, heuristic_p1, 1, minmax_depth)
        self.p2 = self.player_mode(p2, heuristic_p2, 2, minmax_depth)

        self.game()

    def game(self):
        while(True):
            while(True):
                self.board.print_board()
                print("Player 1 (X)")
                move = self.p1.move(self.board)
                moves = self.board.possible_movements(move[0])
                if move[1] in moves:
                    self.board.move_piece(move[0],move[1])
                    break
                print("Invalid move")
            if self.board.is_end(1):
                self.board.print_board()
                print("WIN Player 1")
                break

            # time.sleep(1)

            while(True):
                self.board.print_board()
                print("Player 2 (O)")
                move = self.p2.move(self.board)
                moves = self.board.possible_movements(move[0])
                if move[1] in moves:
                    self.board.move_piece(move[0],move[1])
                    break
                print("Invalid move")
            if self.board.is_end(2):
                self.board.print_board()
                print("WIN Player 2")
                break

            # time.sleep(1)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-p1", "--player1",
                        choices=['P', 'CBCM'],
                        help="Player 1 mode : P - Player, CBCM - Computer best current move",
                        required=True)

    parser.add_argument("-h1", "--heuristicP1",
                         choices=['M', 'R'],
                         help="Heuristic for p1: M - Manhattan heuristic, R - Random heuristic",
                         default='M')

    parser.add_argument("-p2", "--player2",
                        choices=['P', 'CBCM', 'CMM'],
                        help="Player 2 mode : P - Player , CBCM - Computer best current move , CMM - Computer minmax",
                        required=True)

    parser.add_argument("-h2", "--heuristicP2",
                         choices=['M', 'R'],
                         help="Heuristic for p2: M - Manhattan heuristic, R - Random heuristic",
                         default='M')

    args = parser.parse_args()

    game = Game()


    game.start_game(args.player1, args.player2, args.heuristicP1, args.heuristicP2)


