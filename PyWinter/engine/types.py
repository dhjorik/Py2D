from PySide6.QtCore import QPoint


class Position:
    _pos = None

    def __init__(self):
        self._pos = QPoint(0, 0)