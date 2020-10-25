import socket
import pickle
from _thread import *
from player import Player
from game import Game
from client import Client

host = '192.168.178.21'
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

def handle_player(connection):
    global players, connections, in_game
    connections.append(connection)  # add to connections
    client = pickle.loads(conn.recv(2048))  # receive client object
    player = Player.parse_client(client)  # create player object
    print(f'{player.name} joined the server.')
    players.append(player)  # add to connected players
    broadcast(players_to_clients(players))
    data = None
    send_msg = {}
    while True:
        try:
            try:
                data = recvall(connection)
            except:
                pass
            if not in_game:  # lobby logic

                if data == 'ready':
                    player.ready = True
                    broadcast(players_to_clients(players))

                if all_players_ready():
                    broadcast('start')
                    game = Game(players)
                    for p in players:
                        p.set_game(game)
                    in_game = True

            elif in_game:  # in game logic
                if player.game:

                    if isinstance(data, list):
                        player.game.grid.completely_update(data)

                    if data == 'word':
                        send_msg['word'] = player.game.round.word
                    elif data == 'drawing':
                        player.drawing = player.game.round.player_drawing == player
                        if player.drawing:
                            send_msg['drawing'] = True
                        else:
                            send_msg['drawing'] = False
                    elif data == 'clients':
                        send_msg['clients'] = players_to_clients(players)
                    elif data == 'time':
                        send_msg['time'] = player.game.round.draw_time
                    elif data == 'grid':
                        send_msg['grid'] = player.game.grid.get_grid()
                    elif data == 'chat':
                        send_msg['chat'] = player.game.round.chat.messages

                    if isinstance(data, dict):
                        try:
                            if isinstance(data['guess'], str):
                                player.game.make_player_guess(player, data['guess'])

                            if isinstance(data['grid_data'], tuple):
                                player.game.grid.update(data['grid_data'])
                            elif isinstance(data['grid_data'], str):
                                if data['grid_data'] == 'clear':
                                    player.game.grid.new_empty_grid()
                        except KeyError:
                            pass

                    connection.send(pickle.dumps(send_msg))

                else:
                    pass

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
            connection.send(pickle.dumps(data))
        except Exception as ex:
            print(ex)

def recvall(connection):
    buff_size = 4096
    data = bytearray()
    while True:
        chunk = connection.recv(buff_size)
        data += chunk
        if len(chunk) < buff_size:
            break
    return pickle.loads(data)


def players_to_clients(list):  # converts a list of players into a list of clients
    return [Client.parse_player(player) for player in list]

def all_players_ready():  # start game if all players are ready
    if len(players) > 1:
        if all(player.ready for player in players):
            return True
    return False

if not in_game:
    print('Waiting for players...')
    s.listen(8)

    while True:
        conn, addr = s.accept()
        print('Connected to', conn)
        start_new_thread(handle_player, (conn, ))  # starting new thread for handling the lobby logic for the client