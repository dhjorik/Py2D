

class Point:
    _x = 0
    _y = 0

    def __init__(self, px, py):
        self._x = px
        self._y = py

    def _get_x(self):
        return self._x

    def _set_x(self, value):
        self._x = value

    x = property(_get_x, _set_x)

    def _get_y(self):
        return self._y

    def _set_y(self, value):
        self._y = value

    y = property(_get_y, _set_y)

    def move(self, px, py):
        self._x = px
        self._y = py

    def step(self, dx, dy):
        self._x += dx
        self._y += dy
