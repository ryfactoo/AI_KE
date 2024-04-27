class Board:
    SIZE = 16
    PAWNS_NUMBER = 19

    def __init__(self):
        self.board = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]

    def print_board(self):
        symbols = {0: '.', 1: 'X', 2: 'O'}  # Definicja symboli dla różnych wartości

        print("    ", end="")
        for i in range(1, self.SIZE + 1):
            print(f"{i:2}", end=" ")
        print()

        for i, row in enumerate(self.board):
            print(f"{i + 1:2}", end="   ")

            print('  '.join([symbols[cell] for cell in row]), end="  ")

            print(f"{i + 1:2}")

    def init_game(self):
        for i in range(1, 6):
            for j in range(1, 6):
                if i + j < 8:
                    self.board[self.SIZE - i][self.SIZE - j] = 2
        for i in range(0, 5):
            for j in range(0, 5):
                if i + j < 6:
                    self.board[i][j] = 1

    def is_valid_move(self, start, end):
        start_x, start_y = start
        end_x, end_y = end
        if start_x < 0 or start_x >= self.SIZE or start_y < 0 or start_y >= self.SIZE:
            return False
        if end_x < 0 or end_x >= self.SIZE or end_y < 0 or end_y >= self.SIZE:
            return False
        if self.board[end_x][end_y] != 0:
            return None
        else:
            return True

    def check_jump(self, start, jump):
        start_x, start_y = start
        jump_x, jump_y = jump
        end_x = 2 * jump_x - start_x
        end_y = 2 * jump_y - start_y

        if start_x < 0 or start_x >= self.SIZE or start_y < 0 or start_y >= self.SIZE:
            return False
        if end_x < 0 or end_x >= self.SIZE or end_y < 0 or end_y >= self.SIZE:
            return False
        if self.board[end_x][end_y] != 0:
            return False
        else:
            return end_x, end_y

    def possible_movements_single(self, start):
        positions = set()
        start_x, start_y, mode = start

        for x in range(-1, 2):
            if x + start_x < 0 or x + start_x >= self.SIZE:
                continue

            for y in range(-1, 2):
                value = self.is_valid_move((start_x, start_y), (start_x + x, start_y + y))
                if value is None:
                    end = self.check_jump((start_x, start_y), (start_x + x, start_y + y))
                    if end:
                        positions.add((end[0], end[1], "J"))

                elif value and mode == "S":
                    positions.add((start_x + x, start_y + y, "M"))

        return positions

    def possible_movements(self, start):
        movements = set()
        new_movements = set()
        new_movements.add((start[0], start[1], "S"))

        while new_movements:
            position = new_movements.pop()

            if position[2] == "M":
                movements.add(position)
                continue
            new_positions = self.possible_movements_single(position)
            new_movements.update(new_positions.difference(movements))
            movements.add(position)
        movements.discard(start)

        return {(t[0], t[1]) for t in movements}

    def move_piece(self, start, end):
        if self.is_valid_move(start, end):
            start_x, start_y = start
            end_x, end_y = end
            self.board[end_x][end_y] = self.board[start_x][start_y]
            self.board[start_x][start_y] = 0
            return True
        else:
            return False

    def is_end(self, player):

        if player == 1:
            for i in range(1, 6):
                for j in range(1, 6):
                    if i + j < 8 and self.board[self.SIZE - i][self.SIZE - j] != 1:
                        return False
            return True
        else:
            for i in range(0, 5):
                for j in range(0, 5):
                    if i + j < 6 and self.board[i][j] != 2:
                        return False
            return True
