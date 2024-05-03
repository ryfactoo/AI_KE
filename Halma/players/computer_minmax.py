from players.computer_best_current_move import ComputerBestCurrentMove


class ComputerMinmax(ComputerBestCurrentMove):
    def __init__(self, heuristic, player, targetDepth):
        super().__init__(heuristic, player)
        self.targetDepth = targetDepth

    def move(self, board):

        if self.targetDepth == 1:
            return super().move(board)
        else:
            return self.minimax(1, True, board)[1]

    def minimax(self, curDepth,
                maxTurn, board):

        player = self.player if maxTurn else (self.player % 2) + 1

        possible_moves = board.possible_movements_for_player(player)

        pq = []

        for possible_move in possible_moves:
            if not any(possible_moves[possible_move]):
                continue

            for move in possible_moves[possible_move]:
                board.move_piece(possible_move, move)

                if curDepth != self.targetDepth:
                    pq.append((self.minimax(curDepth + 1, not maxTurn, board), (possible_move, move)))
                else:
                    pq.append((self.heuristic.calculate(board, self.player), (possible_move, move)))

                board.move_piece(move, possible_move)

        best_move = min(pq, key=lambda x: x[0]) if maxTurn else max(pq, key=lambda x: x[0])
        return best_move
