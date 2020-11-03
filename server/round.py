import time
from _thread import *
from chat import MessageType

class Round:
    def __init__(self, word, player_drawing, game):
        self.word = word
        self.player_drawing = player_drawing
        self.game = game
        self.players_guessed = []
        self.draw_time = 90
        self.player_scores = {player: 0 for player in self.game.players}
        self.game.chat.add_message(f'{MessageType.INFO}{self.player_drawing.name} is drawing!')
        start_new_thread(self.timer, ())

    def timer(self):
        while self.draw_time > 0:
            time.sleep(1)
            self.draw_time -= 1
        self.end()

    def got_correct_guess(self, player, word):
        if player in self.players_guessed or player.uid == self.player_drawing.uid:
            self.game.chat.add_message(f'{MessageType.INVISIBLE}{player.name}: {word}')
            return
        elif word.lower() == self.word.lower():
            self.players_guessed.append(player)
            self.player_scores[player] += 5 * self.draw_time
            self.game.chat.add_message(f'{MessageType.SUCCESS}{player.name} guessed the word!')
            if len(self.players_guessed) == len(self.game.players) - 1:
                self.draw_time = 0
            return
        else:
            self.game.chat.add_message(f'{player.name}: {word}')
            return

    def end(self):
        self.game.chat.add_message(f'{MessageType.INFO}The word was: {self.word}')
        for player, score in self.player_scores.items():
            player.points += score
            if player == self.player_drawing:
                self.player_scores[player] = sum([self.player_scores[player] for player in self.players_guessed]) // 3
                player.points += self.player_scores[player]

        for player in self.players_guessed:
            self.game.chat.add_message(f'{MessageType.INFO}{player.name}: +{self.player_scores[player]} points')

        sorted_scores = sorted(self.player_scores.items(), key=lambda x: x[1], reverse=True)
        for i, item in enumerate(sorted_scores):
            item[0].rank = i + 1

        self.game.end_round()