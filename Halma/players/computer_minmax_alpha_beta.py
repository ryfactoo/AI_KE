from players.computer_best_current_move import ComputerBestCurrentMove

MAX = 10000
MIN = -10000


class ComputerMinmaxAlphaBeta(ComputerBestCurrentMove):

    def __init__(self, heuristic, player, targetDepth):
        super().__init__(heuristic, player)
        self.targetDepth = targetDepth

    def move(self, board):

        if self.targetDepth == 1:
            return super().move(board)
        else:
            return self.minimax(1, True, board, MAX, MIN)[1]

    def minimax(self, curDepth,
                maxTurn, board, alpha, beta):

        player = self.player if maxTurn else (self.player % 2) + 1
        best = (MAX,) if maxTurn else (MIN,)

        possible_moves = board.possible_movements_for_player(player)

        for possible_move in possible_moves:
            if not any(possible_moves[possible_move]):
                continue

            for move in possible_moves[possible_move]:
                board.move_piece(possible_move, move)

                if curDepth != self.targetDepth:
                    val = (self.minimax(curDepth + 1, not maxTurn, board, alpha, beta)[0], (possible_move, move))
                else:
                    val = (self.heuristic.calculate(board, self.player), (possible_move, move))

                board.move_piece(move, possible_move)

                if maxTurn:
                    best = min(best, val, key=lambda x: x[0])
                    alpha = min(alpha, best[0])
                else:
                    best = max(best, val, key=lambda x: x[0])
                    beta = max(beta, best[0])

                if beta >= alpha:
                    break

        return best
