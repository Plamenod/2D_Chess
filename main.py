from chess import ChessBoard
from point import Point
import pygame
import time


def pygame_main():

    pygame.init()
    pygame_mainloop()


def pygame_mainloop():

    chess_board = ChessBoard()
    player = 0
    chess_board.set_allowed_color(player)
    screen = pygame.display.set_mode((640, 480))
    board_image, chess_image = load_images()
    selected = surface()

    is_selected_cell = False
    selected_cell = Point(None, None)
    offset = 120

    print ("player's", player, "turn")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

            elif event.type == pygame.MOUSEBUTTONUP:
                new_position = make_a_point_from_mouse(event, offset)
                if is_into_board(new_position):
                    new_position.normalize_point()
                    if is_selected_cell:
                        is_selected_cell = False
                        can_play = chess_board.play(selected_cell, new_position)
                        if can_play:
                            player = change_player(player)
                            chess_board.set_allowed_color(player)
                            print ("player's", player, "turn")
                        else:
                            print("Invalid move!!! Try again")
                        selected_cell.set_point(None, None)
                    else:
                        selected_cell.set_point(
                            new_position.get_x(), new_position.get_y())
                        if chess_board.allowed_selection(selected_cell, player):
                            is_selected_cell = True

                        else:
                            selected_cell.set_point(None, None)

        screen.fill((109, 165, 165))
        screen.blit(board_image, (offset, offset))
        if selected_cell.get_x() is not None and \
                selected_cell.get_y() is not None:
            screen.blit(selected, (selected_cell.get_x()*32 + offset + 2,
                        selected_cell.get_y()*24 + offset + 2))
        prepare_board_to_update(chess_board, screen, chess_image, offset)
        pygame.display.update()
        time.sleep(0.04)
        if chess_board.is_end():
            print("The winner is Player {0}".format((player + 1) % 2))
            time.sleep(4)
            return


def load_images():
    piecestr = "prnbqk"
    pieces = pygame.image.load("imgs/chess-pieces.png").convert_alpha()

    chess_image = dict([
        ('b' + piecestr[x], pieces.subsurface((x*32, 0, 32, 32)))
        for x in range(6)])

    chess_image.update(dict([
        ('w' + piecestr[x], pieces.subsurface((x*32, 32, 32, 32)))
        for x in range(6)]))

    board_image = pygame.image.load("imgs/chess-board.png").convert_alpha()
    return board_image, chess_image


def surface():
    selected = pygame.Surface((32, 24), pygame.SWSURFACE | pygame.SRCALPHA, 32)
    selected.fill((255, 255, 0))
    return selected


def is_into_board(cell):
    return 0 <= cell.get_x() <= 255 and 0 <= cell.get_y() <= 191


def change_player(player):
    return (player + 1) % 2


def prepare_board_to_update(chess_board, screen, chess_image, offset):
    for y, col in enumerate(chess_board.get_board()):
            for x, piece in enumerate(col):
                if piece[0] != ' ':
                    screen.blit(chess_image[piece],
                                (x*32 + offset, y*24 + offset - 12))


def make_a_point_from_mouse(event, offset):
    new_position_x, new_position_y = event.pos
    new_position_x -= offset
    new_position_y -= offset
    return Point(new_position_x, new_position_y)

if __name__ == "__main__":
    pygame_main()
