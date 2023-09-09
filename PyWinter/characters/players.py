from PyWinter.characters.actors import Actor


class Player01(Actor):
    def __init__(self, game):
        super(Player01, self).__init__('player_01', game)
        self.load_assets()
