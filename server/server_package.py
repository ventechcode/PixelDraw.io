class ServerPackage:
    def __init__(self):
        self.start = False  # game start
        self.guessed = False  # player guessed (bool)
        self.score = 0  # players score
        self.round = 0  # current round
        self.word = ''  # current word
        self.time = 0  # round time
        self.is_drawing = False