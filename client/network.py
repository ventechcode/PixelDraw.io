import socket
import pickle
import pygame

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '192.168.178.21'
        self.port = 4444
        self.addr = (self.host, self.port)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return True
        except socket.error as e:
            print(e)
            return False

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except Exception as ex:
            print(ex)

    def receive(self):  # returns incoming data
        try:
            buff_size = 4096
            data = bytearray()
            while True:
                chunk = self.client.recv(buff_size)
                data += chunk
                if len(chunk) < buff_size:
                    break
            return pickle.loads(data)
        except Exception as ex:
            print(ex)

    def get(self, data):  # returns the response for the request
        try:
            self.client.send(pickle.dumps(data))
            buff_size = 4096
            data = bytearray()
            while True:
                chunk = self.client.recv(buff_size)
                data += chunk
                if len(chunk) < buff_size:
                    break
            return pickle.loads(data)
        except Exception as e:
            print(e)

    def disconnect(self):
        self.client.shutdown(2)
        self.client.close()

    @staticmethod
    def draw_error_message(win, msg, x, y):
        font = pygame.font.SysFont('arialblack', 16)
        text_surface = font.render(msg, True, (232, 9, 32))
        win.blit(text_surface, (x // 2 - text_surface.get_width() // 2, y))