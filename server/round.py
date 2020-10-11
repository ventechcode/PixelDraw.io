import time
from _thread import *

class Round:
    def __init__(self, word, player_drawing, game):
        self.word = word
        self.player_drawing = player_drawing
        self.game = game
        self.players_guessed = []
        self.draw_time = 90
        self.player_scores = {player: 0 for player in self.game.players}
        start_new_thread(self.timer, ())

    def timer(self):
        while self.draw_time > 0:
            time.sleep(1)
            self.draw_time -= 1

    def got_correct_guess(self, player, word) -> bool:
        if word.lower() == self.word.lower():
            self.players_guessed.append(player)
            return True
        else:
            return False