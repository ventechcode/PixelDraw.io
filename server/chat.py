class Chat:
    def __init__(self):
        self.messages = []

    def add_message(self, msg):
        self.messages.append(msg)

class MessageType:
    SUCCESS = 'SUCCESS'  # green server message for guessed words
    INFO = 'INFO'  # blue server message about game info
    ERROR = 'ERROR'  # red server message about game errors
    WARNING = 'WARNING'  # orange server message for important hints
    INVISIBLE = 'INVISIBLE'  # only appears to players who already guessed