# This is a sample Python script.
import board
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi():
    # Use a breakpoint in the code line below to debug your script.
    game = board.Board()
    game.init_game()
    game.move_piece((0,4),(0,5))
    game.print_board()
    # print(game.check_jump((0,3),(0,2)))
    # game.print_board()
    print(game.possible_movements((2,3)))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
