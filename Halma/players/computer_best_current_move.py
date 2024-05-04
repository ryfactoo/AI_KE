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

    def min_max_elem(self, list, max_first):
        max = -1

        for elem in list:
            if max == -1:
                max = elem
                continue

            if max_first and elem[0] > max[0]:
                max = elem
                continue
            elif not max_first and elem[0] < max[0]:
                max = elem
                continue

            tmp_elem = elem[1:]
            tmp_max = max[1:]
            tmp_max_first = not max_first

            while (len(tmp_elem) > 1):
                if tmp_max_first and tmp_elem[0] > tmp_max[0]:
                    max = elem
                    break
                elif not tmp_max_first and tmp_elem[0] < tmp_max[0]:
                    max = elem
                    break
                tmp_max = tmp_max[1:]
                tmp_elem = tmp_elem[1:]
                tmp_max_first = not tmp_max_first
        return max
