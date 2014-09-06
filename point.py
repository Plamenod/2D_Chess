class Point:

    def __init__(self, x, y, info=None):
        self._x = x
        self._y = y
        self._info = info

    def get_color(self):
        return self._info[0]

    def get_type(self):
        return self._info[1]

    def get_figure(self):
        return self._info

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_info(self, figure):
        self._info = figure

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y

    def set_point(self, x, y):
        self._x = x
        self._y = y

    def increase(self, x, y):
        self._x += x
        self._y += y

    def normalize_point(self):
        self._x = int(self._x / 32)
        self._y = int(self._y / 24)

    def prepare_first_move_black_pawn(self, selected_position):
        if selected_position.get_y() < 2 and self.get_y() == 2:
            self.set_y(1)
            print("move black pawn 2 cells 52")

    def prepare_first_move_white_pawn(self, selected_position):
        if selected_position.get_y() > 5 and self.get_y() == -2:
            print("move white pawn 2 cells 56")
            self.set_y(-1)
