class Status:
    game = None

    _players = [(0, 0)]

    def __init__(self, game):
        self.game = game

    def get_player1_x(self):
        return self._players[0][0]

    def set_player1_x(self, value):
        self._players[0][0] = value
        if value < self.sprite_area_min_x:
            self._players[0][0] = self.sprite_area_min_x
        if value > self.sprite_area_max_x:
            self._players[0][0] = self.sprite_area_max_x

    player1_x = property(get_player1_x, set_player1_x)

    def get_player1_y(self):
        return self._players[0][1]

    def set_player1_y(self, value):
        self._players[0][1] = value
        if value < self.sprite_area_min_y:
            self._players[0][1] = self.sprite_area_min_y
        if value > self.sprite_area_max_y:
            self._players[0][1] = self.sprite_area_max_y

    player1_y = property(get_player1_y, set_player1_y)
