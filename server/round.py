import time
from _thread import *
from chat import Chat
from chat import MessageType

class Round:
    def __init__(self, word, player_drawing, game):
        self.word = word
        self.player_drawing = player_drawing
        self.game = game
        self.players_guessed = []
        self.draw_time = 90
        self.player_scores = {player: 0 for player in self.game.players}
        self.chat = Chat()
        self.chat.add_message(f'{MessageType.INFO}{self.player_drawing.name} is drawing!')
        start_new_thread(self.timer, ())

    def timer(self):
        while self.draw_time > 0:
            time.sleep(1)
            self.draw_time -= 1
        self.game.end_round()

    def got_correct_guess(self, player, word):
        if player in self.players_guessed or player.uid == self.player_drawing.uid:
            self.chat.add_message(f'{MessageType.INVISIBLE}{player.name}: {word}')
            return
        elif word.lower() == self.word.lower():
            self.players_guessed.append(player)
            self.chat.add_message(f'{MessageType.SUCCESS}{player.name} guessed the word!')
            return
        else:
            self.chat.add_message(f'{player.name}: {word}')
            return