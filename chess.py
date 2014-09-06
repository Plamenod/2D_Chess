from valid_move import*
from point import Point


class ChessBoard:

    _rules_table = \
        {'r': ROCK, 'n': KNIGHT, 'b': BISHOP, 'q': QUEEN, 'k': KING, 'p': PAWN}

    def __init__(self):
        self._board = [['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
                       ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                       ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                       ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                       ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                       ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                       ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                       ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']]

        self._finish_game = 0
        self.color_of_players = ('w', 'b')

    def play(self, selected_figure, new_position):
        self.view_board()
        motion = self._make_motion(selected_figure, new_position)

        figure_info = self.get_figure_from_board(selected_figure)
        selected_figure.set_info(figure_info)

        if self._invalid_selection(selected_figure):
            return False
        # target means would be taken
        target_figure = self.get_figure_from_board(new_position)

        # pawn special check......
        if selected_figure.get_type() == 'p':

            if selected_figure.get_color() == 'b':

                motion.prepare_first_move_black_pawn(selected_figure)

                if self._get_with_black_pawn(motion, new_position):
                    self.set_end_of_the_game(target_figure)
                    self._attack_with_pawn(new_position,
                                          selected_figure, "bq")
                    return True

                elif self.invalid_move_black_pawn(motion, new_position):
                    print("invalid black pawn's move")
                    return False

            else:
                motion.prepare_first_move_white_pawn(selected_figure)

                if self._get_with_white_pawn(motion, new_position):
                    self.set_end_of_the_game(target_figure)
                    self._attack_with_pawn(
                        new_position, selected_figure, "wq")
                    print("take with white pown")
                    return True

                elif self.invalid_move_white_pawn(motion, new_position):
                    print("invalid white pawn's move")
                    return False
        # end pawn.....

        if self._checking_the_move_is_correct(selected_figure, motion):
            step_x, step_y = self._set_step_to_move(motion)
            prepare_moving = Point(step_x, step_y)

            if selected_figure.get_type() != 'n':

                while self.waiting_to_finish_this_turn(prepare_moving, motion):
                    next_cell = self._set_next_cell(selected_figure,
                                                   prepare_moving)

                    if self._try_jump_yours(next_cell, selected_figure):
                        print("try to jumb over your figure!!! Try again")
                        return False

                    elif self._try_jump_enemy(next_cell, selected_figure,
                                             prepare_moving, motion):
                        print("try to jumb over enemy figure!!! Try again")
                        return False

                    prepare_moving.increase(step_x, step_y)

            elif self.knight_invalid_move(new_position, selected_figure):
                print("It is your figure!!! Try again")
                return False

            self._finally_move(new_position, selected_figure)
            self.set_end_of_the_game(target_figure)
            return True

        else:
            return False

    # can't test it because it's a void
    def view_board(self):
        print('-------------------------------------\n', str(self),
              '\n-------------------------------------\n')

    def _make_motion(self, start_position, destination):
        motion_x = destination.get_x() - start_position.get_x()
        motion_y = destination.get_y() - start_position.get_y()
        motion = Point(motion_x, motion_y)
        return motion

    def get_figure_from_board(self, cell):
        return self._board[cell.get_y()][cell.get_x()]

    def _invalid_selection(self, selected_figure):
        return selected_figure.get_figure() == '  ' or \
            selected_figure.get_color() != self.get_allawod_color()

    def set_end_of_the_game(self, figure):
        if figure == "wk" or figure == "bk":
            self._finish_game = 1

    def _attack_with_pawn(self, new_position, selected_figure, prom_figure):
        if new_position.get_y() % 7:
            self._board[new_position.get_y()][new_position.get_x()] = \
                self.get_figure_from_board(selected_figure)
        else:
            print("Congratulation !!! Yoy have one more queen")
            self._promotion_queen(new_position, prom_figure)
        self.clean_cell(selected_figure)

    def _checking_the_move_is_correct(self, selected_figure, motion):
        figures_type = selected_figure.get_type()
        motion_x = motion.get_x()
        motion_y = motion.get_y()
        try:
            return self._rules_table[figures_type][(motion_x, motion_y)]
        except KeyError:
            return False

    def _set_step_to_move(self, motion):
        step_x = compare(motion.get_x(), 0)
        step_y = compare(motion.get_y(), 0)
        return step_x, step_y

    def waiting_to_finish_this_turn(self, moving, motion):
        return abs(moving.get_x()) <= abs(motion.get_x()) and \
            abs(moving.get_y()) <= abs(motion.get_y())

    def _set_next_cell(self, selected_figure, prepare_moving):
        aux_x = selected_figure.get_x() + prepare_moving.get_x()
        aux_y = selected_figure.get_y() + prepare_moving.get_y()
        return Point(aux_x, aux_y)

    def _try_jump_yours(self, aux, selected_figure):
        return self.get_figure_from_board(aux) != '  '\
            and self.get_color_of_figure(aux) == selected_figure.get_color()

    def _try_jump_enemy(self, next_cell, selected_figure, moving, motion):
        return self._board[next_cell.get_y()][next_cell.get_x()] != '  ' and\
            self._board[next_cell.get_y()][next_cell.get_x()][0] != \
            selected_figure.get_color()\
            and (abs(moving.get_x()) < abs(motion.get_x()) or
                 abs(moving.get_y()) < abs(motion.get_y()))

    # this method check whether trying to move on your's figure
    def knight_invalid_move(self, new_position, selected_figure):

        return self.get_color_of_figure(new_position) == \
            selected_figure.get_color()

    # after all check
    # it would erase selected cell and put the figure on the new cell
    def _finally_move(self, new_position, selected_figure):
        self._board[new_position.get_y()][new_position.get_x()] = \
            self.get_figure_from_board(selected_figure)
        self._board[selected_figure.get_y()][selected_figure.get_x()] = '  '

    def get_color_of_figure(self, cell):
        return self._board[int(cell.get_y())][int(cell.get_x())][0]

    def clean_cell(self, cell):
        self._board[cell.get_y()][cell.get_x()] = '  '

    def _get_with_black_pawn(self, motion, new_position):
        return self._can_pawn_move(motion, 1) and\
            self.get_figure_from_board(new_position)[0] == 'w'

    def _get_with_white_pawn(self, motion, new_position):
        return self._can_pawn_move(motion, -1) and \
            self.get_figure_from_board(new_position)[0] == 'b'

    def _can_pawn_move(self, motion, x):
        return abs(motion.get_x()) == abs(motion.get_y()) and \
            motion.get_y() == x

    def _promotion_queen(self, point, figure):
        self._board[point.get_y()][point.get_x()] = figure

    def invalid_move_white_pawn(self, motion, new_position):
        return motion.get_y() != -1 or motion.get_x() != 0 or \
            self.get_figure_from_board(new_position) != '  '

    def invalid_move_black_pawn(self, motion, new_position):
        return motion.get_y() != 1 or motion.get_x() != 0 or \
            self.get_figure_from_board(new_position) != '  '

    def set_allowed_color(self, player):
        self._color = self.get_color_of_player(player)

    def get_allawod_color(self):
        return self._color

    def __str__(self):
        return "\n-------------------------------------\n"\
            .join([" | ".join(x)for x in self._board])

    def allowed_selection(self, selected_cell, player):
        return self.get_current_figure_color(
            selected_cell.get_x(),
            selected_cell.get_y()) == self.get_color_of_player(player)

    def get_current_figure_color(self, x, y):
        return self._board[y][x][0]

    def get_color_of_player(self, player):
        return self.color_of_players[player]

    def is_end(self):
        return self._finish_game

    def get_board(self):
        return self._board


def compare(x, y):
    return (x > y) - (x < y)
