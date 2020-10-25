import random
from round import Round
from grid import Grid


class Game:
    def __init__(self, players):
        self.players = players
        self.used_words = set()
        self.round = None
        self.round_count = 0
        self.max_rounds = 3
        self.drawing_player_index = 0
        self.grid = Grid()
        self.start_new_round()

    def start_new_round(self):
        self.round = Round(self.get_random_word(), self.players[self.drawing_player_index], self)

    def make_player_guess(self, player, word):
        return self.round.got_correct_guess(player, word)

    def get_random_word(self):
        words = []
        with open('./server/words.txt', 'r') as f:
            for line in f.readlines():
                word = line.strip()
                if word not in self.used_words:
                    words.append(word)
        word = random.choice(words)
        self.used_words.add(word)
        return word

    def player_disconnect(self, player):
        if player in self.players:
            self.players.remove(player)
        if len(self.players) == 1:
            self.end_game()

    def end_game(self):
        for p in self.players:
            p.set_game(None)