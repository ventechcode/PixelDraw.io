import threading
import time

class Timer:
    def __init__(self, seconds):
        self.seconds = seconds
        self.finished = False
        self.countdown_thread = threading.Thread(target=self.countdown)
        self.countdown_thread.daemon = True

    def countdown(self):
        time.sleep(1)
        for i in range(0, self.seconds):
            self.seconds -= 1
            time.sleep(1)
        self.finished = True

    def start(self):
        self.finished = False
        self.countdown_thread.start()