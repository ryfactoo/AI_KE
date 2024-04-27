import argparse
import board as game_board
import players.player as human_player

class Game:
    def player_mode(self,player):

        if(player == "P"):
            return human_player.Player()

    def init(self, board):
        if board:
            self.board.board = board
        else:
            self.board.init_game()

    def start_game(self, p1, p2, board = None):
        self.board = game_board.Board()

        self.init(board)

        self.p1 = self.player_mode(p1)
        self.p2 = self.player_mode(p2)

        self.game()

    def game(self):
        while(True):
            while(True):
                self.board.print_board()
                print("Player 1 (X)")
                move = self.p1.move()
                moves = self.board.possible_movements(move[0])
                if move[1] in moves:
                    self.board.move_piece(move[0],move[1])
                    break
                print("Invalid move")
            if self.board.is_end(2):
                self.board.print_board()
                print("WIN Player 1")
                break

            while(True):
                self.board.print_board()
                print("Player 2 (O)")
                move = self.p1.move()
                moves = self.board.possible_movements(move[0])
                if move[1] in moves:
                    self.board.move_piece(move[0],move[1])
                    break
                print("Invalid move")
            if self.board.is_end(1):
                self.board.print_board()
                print("WIN Player 1")
                break




if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-p1", "--player1",
                        choices=['P', 'O'],
                        help="Player 1 mode - P - Player",
                        required=True)

    parser.add_argument("-p2", "--player2",
                        choices=['P', 'O'],
                        help="Player 2 mode - P - Player",
                        required=True)

    args = parser.parse_args()

    game = Game()

    # board = [[0 for _ in range(16)] for _ in range(16)]
    #
    # for i in range(1, 6):
    #     for j in range(1, 6):
    #         if i + j < 8:
    #             board[16 - i][16 - j] = 1
    # for i in range(0, 5):
    #     for j in range(0, 5):
    #         if i + j < 6:
    #             board[i][j] = 2
    # game.start_game(args.player1, args.player2, board)


    game.start_game(args.player1, args.player2)


