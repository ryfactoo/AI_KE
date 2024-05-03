from players.player_mode import PlayerMode
import heapq

class ComputerBestCurrentMove(PlayerMode):

    def __init__(self, heuristic, player):
        self.heuristic = heuristic
        self.player = player

    def move(self, board):
        possible_moves = board.possible_movements_for_player(self.player)

        pq = []

        for possible_move in possible_moves:
            if not any(possible_moves[possible_move]):
                continue

            for move in possible_moves[possible_move]:
                board.move_piece(possible_move,move)
                heapq.heappush(pq,(self.heuristic.calculate(board,self.player),(possible_move,move)))
                board.move_piece(move,possible_move)

        best_heuristic, move = heapq.heappop(pq)
        print(best_heuristic)
        return move
