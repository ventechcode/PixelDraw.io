import random
from round import Round
from grid import Grid
from chat import MessageType, Chat
import time
from _thread import *

class Game:
    def __init__(self, players):
        self.players = players
        self.used_words = set()
        self.drawing_order = []
        self.drawing_player_index = 0
        self.round = None
        self.max_rounds = 3
        self.grid = Grid()
        self.chat = Chat()
        self.round_count = 1
        self.chat.add_message(f'{MessageType.INFO}Round {self.round_count}/{self.max_rounds} started.')
        self.start_new_round()

    def start_new_round(self):
        if len(self.drawing_order) < len(self.players) and self.round_count == 1:  # Round one
            drawing_player = random.choice(self.players)
            if drawing_player not in self.drawing_order:
                self.drawing_order.append(drawing_player)
                self.round = Round(self.get_random_word(), drawing_player, self)
            else:
                self.start_new_round()
        elif self.drawing_player_index < len(self.drawing_order) and self.round_count == 2:
            self.round = Round(self.get_random_word(), self.drawing_order[self.drawing_player_index], self)
            self.drawing_player_index += 1
        elif self.drawing_player_index < len(self.drawing_order) and self.round_count == 3:
            self.round = Round(self.get_random_word(), self.drawing_order[self.drawing_player_index], self)
            self.drawing_player_index += 1
        else:
            if self.round_count < self.max_rounds:
                self.round_count += 1
                self.drawing_player_index = 0
                self.chat.add_message(f'{MessageType.INFO}Round {self.round_count}/{self.max_rounds} started.')
                self.start_new_round()
            else:
                self.end_game()

    def make_player_guess(self, player, word):
        self.round.got_correct_guess(player, word)
        if player in self.round.players_guessed:
            player.guessed = True

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
            self.chat.add_message(f'{MessageType.ERROR}{player.name} left.')
        if len(self.players) == 1:
            self.end_game()

    def end_game(self):
        self.chat.add_message(f'{MessageType.INFO}The game has ended.')
        time.sleep(2)
        for p in self.players:
            p.set_game(None)

    def end_round(self):
        self.grid.new_empty_grid()
        for player in self.players:
            player.guessed = False
            player.drawing = False
        self.start_new_round()
