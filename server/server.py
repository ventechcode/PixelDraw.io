import socket
import pickle
from _thread import *
from player import Player
from server_package import ServerPackage
from game import Game
from client import Client

host = '127.0.0.1'
port = 4444

players = []
connections = []
in_game = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((host, port))
    print('Started Server @' + host + ' on port ' + str(port))
except socket.error:
    pass

print('Waiting for players...')
s.listen(8)

def handle_player(connection):
    global players, connections, in_game
    connections.append(connection)  # add to connections
    client = pickle.loads(conn.recv(2048))  # receive client object
    player = Player.parse_client(client)  # create player object
    print(f'{player.name} joined the server.')
    players.append(player)  # add to connected players
    package = ServerPackage()
    broadcast(players_to_clients(players))  # send the updated list of connected players to all clients
    ready = False
    while True:
        try:
            client_info = pickle.loads(connection.recv(2048))
            if not all_players_ready():  # lobby logic
                if client_info.ready and not ready:
                    player.ready = True
                    print(f'{player.name} is ready!')
                    broadcast(players_to_clients(players))
                    ready = True
            if all_players_ready() and not in_game:
                in_game = True
            if in_game:
                if player.game:
                    package.time = player.game.round.draw_time  # get round time
                    if player.uid == player.game.round.player_drawing.uid:
                        package.is_drawing = True
                    else:
                        package.is_drawing = False

                    package.word = player.game.round.word
                    connection.send(pickle.dumps(package))

                    if package.is_drawing:
                        broadcast(client_info.grid_data)
                elif not player.game:
                    print('Game Ended!')

        except socket.error:
            print(f'{player.name} disconnected.')
            if player in players:
                players.remove(player)
            if connection in connections:
                connections.remove(connection)
            if player.game:
                player.game.player_disconnect(player)
            broadcast(players_to_clients(players))
            break

def broadcast(data):  # sends data to all connected clients
    for connection in connections:
        try:
            connection.send(pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL))
        except Exception as ex:
            print(ex)

def players_to_clients(_players):
    arr = []
    for player in _players:
        arr.append(Client.parse_player(player))
    return arr

def all_players_ready():  # start game if all players are ready
    if in_game:
        return True
    elif len(players) > 1:
        if all(player.ready for player in players):
            broadcast('start')
            game = Game(players)
            for player in players:
                player.set_game(game)
            return True
    return False

while True:
    conn, addr = s.accept()
    print('Connected to', conn)
    start_new_thread(handle_player, (conn, ))  # starting new thread for handling the lobby logic for the client
