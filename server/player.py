
class Player:

    @staticmethod
    def parse_client(client):
        return Player(client.name, client.uid)

    def __init__(self, name, uid):
        self.name = name
        self.ready = False
        self.uid = uid
        self.rank = 1
        self.points = 0
        self.game = None
        self.drawing = False
        self.guessed = False

    def set_game(self, game):
        self.game = game

    def guess(self, word):
        return self.game.make_player_guess(self, word)

    def update_points(self, points):
        self.points += points

    def update_rank(self, rank):
        self.rank = rank