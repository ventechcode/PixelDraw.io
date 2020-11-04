import socket
import pickle
from _thread import *
from player import Player
from game import Game
from client import Client
import uuid

host = '192.168.178.21'
port = 4444

lobbys = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((host, port))
    print('Started Server @' + host + ' on port ' + str(port))
except socket.error:
    pass

print('Waiting for clients to connect...')
s.listen()

def handle_request(conn):
    data = pickle.loads(conn.recv(2048))
    if isinstance(data, Client):
        player = Player.parse_client(data)
        if all(lobby.public is False for lobby in lobbys) or len(lobbys) < 1:
            lobby = Lobby(uuid.uuid4(), True)
            lobbys.append(lobby)
            lobby.add_player(conn, player)
        else:
            for lobby in lobbys:
                if lobby.public:
                    lobby.add_player(conn, player)
                    break
            return
    elif isinstance(data, dict):
        player = Player.parse_client(data['client'])
        key = data['key']
        for lobby in lobbys:
            if lobby.id == key:
                lobby.add_player(conn, player)
                return

    elif isinstance(data, tuple):
        client, lobby_key = data
        player = Player.parse_client(client)
        lobby = Lobby(lobby_key, False)
        lobbys.append(lobby)
        lobby.add_player(conn, player)
        print(f'{player.name} created a private Lobby #{lobby_key}.')

class Lobby:
    @staticmethod
    def receive(connection):
        buff_size = 4096
        data = bytearray()
        while True:
            chunk = connection.recv(buff_size)
            data += chunk
            if len(chunk) < buff_size:
                break
        return pickle.loads(data)

    def __init__(self, id, public):
        self.id = id
        self.public = public
        self.connections = []
        self.players = []
        self.max_players = 8 if public else 12
        self.game = None
        self.in_game = False

    def add_player(self, connection, player):
        print(f'{player.name} joined the lobby #{self.id}.')

        self.connections.append(connection)
        self.players.append(player)

        if self.in_game:  # join the game if its already on going
            connection.send(pickle.dumps('start'))
            player.set_game(self.game)

        start_new_thread(self.handle_player, (connection, player))  # start thread to handle communication
        self.broadcast(self.players_to_clients())  # send the updated player list to all clients

        if len(self.players) == self.max_players:  # lobby is full
            self.public = False

    def handle_player(self, connection, player):
        data = None
        send_msg = {}
        while True:
            try:
                try:
                    data = self.receive(connection)
                except:
                    pass
                if not self.in_game:  # lobby logic

                    if data == 'ready':
                        player.ready = True
                        self.broadcast(self.players_to_clients())

                    if self.all_players_ready():
                        self.broadcast('start')
                        self.game = Game(self.players)
                        for p in self.players:
                            p.set_game(self.game)
                        self.in_game = True

                elif self.in_game:  # in game logic
                    if player.game:

                        if isinstance(data, list):
                            player.game.grid.completely_update(data)
                        elif isinstance(data, dict):
                            player.game.make_player_guess(player, data['guess'])

                        if data == 'word':
                            send_msg['word'] = player.game.round.word
                        elif data == 'drawing':
                            player.drawing = player.game.round.player_drawing == player
                            if player.drawing:
                                send_msg['drawing'] = True
                            else:
                                send_msg['drawing'] = False
                        elif data == 'clients':
                            send_msg['clients'] = self.players_to_clients()
                        elif data == 'time':
                            send_msg['time'] = player.game.round.draw_time
                        elif data == 'grid':
                            send_msg['grid'] = player.game.grid.get_grid()
                        elif data == 'chat':
                            send_msg['chat'] = player.game.chat.messages
                        elif data == 'round':
                            send_msg['round'] = player.game.round_count

                        connection.send(pickle.dumps(send_msg))

                    else:
                        pass

            except socket.error:
                print(f'{player.name} disconnected.')
                player.game.player_disconnect(player)
                if player in self.players:
                    self.players.remove(player)
                if connection in self.connections:
                    self.connections.remove(connection)
                self.broadcast(self.players_to_clients())
                break

    def broadcast(self, data):
        for connection in self.connections:
            try:
                connection.send(pickle.dumps(data))
            except Exception as ex:
                print(ex)

    def players_to_clients(self):  # converts a list of players into a list of clients
        return [Client.parse_player(player) for player in self.players]

    def all_players_ready(self):  # start game if all players are ready
        if len(self.players) > 1:
            if all(player.ready for player in self.players):
                return True
        return False

while True:
    conn, addr = s.accept()
    print('Connected to', conn)
    handle_request(conn)