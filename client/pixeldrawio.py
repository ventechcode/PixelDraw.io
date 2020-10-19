import pygame
import sys
from color_palette import ColorPalette
from client_package import ClientPackage
from server_package import ServerPackage
from top_bar import TopBar
from colors import Colors
from grid import Grid
from button import Button
from network import Network
from client import Client
from tool import Tool
from _thread import *

pygame.init()
pygame.font.init()

SIZE = (1400, 960)
MENU_SIZE = (600, 600)
screen = pygame.display.set_mode(MENU_SIZE)
pygame.display.set_caption('PixelDraw.io')
clock = pygame.time.Clock()

# custom recursion limit for the flood fill algorithm to prevent game crashes
sys.setrecursionlimit(10000)

# global variables
client = None
connected_clients = []
server_info = ServerPackage()
package = ClientPackage()
start = False

network = Network()

X_OFF = 316
Y_OFF = 90
grid = Grid(x_cells=64, y_cells=64, cell_size=12, x_off=X_OFF, y_off=Y_OFF, color=Colors.WHITE)
grid_on_icon = pygame.image.load('assets/icons/grid_on.png')
grid_off_icon = pygame.image.load('assets/icons/grid_off.png')

toggle_btn = Button(Colors.WHITE, X_OFF, Y_OFF + (grid.yCells * grid.cellSize) + 25, 50, 50, text=None, icon=grid_on_icon)
palette = ColorPalette()
selected_color_surface = pygame.Surface((50, 49))

topbar = TopBar(15, 15, 1370, 60)

# load icons & initiate drawing tools
brush_icon = pygame.image.load('assets/icons/brush.png')
brush = Tool('brush', brush_icon, (727, Y_OFF + (grid.yCells * grid.cellSize) + 25))
eraser_icon = pygame.image.load('assets/icons/eraser.png')
eraser = Tool('eraser', eraser_icon, (782, Y_OFF + (grid.yCells * grid.cellSize) + 25))
eyedropper_icon = pygame.image.load('assets/icons/eyedropper.png')
eyedropper = Tool('eyedropper', eyedropper_icon, (837, Y_OFF + (grid.yCells * grid.cellSize) + 25))
fill_icon = pygame.image.load('assets/icons/fill.png')
fill = Tool('fill', fill_icon, (892, Y_OFF + (grid.yCells * grid.cellSize) + 25))
delete_icon = pygame.image.load('assets/icons/delete.png')
delete = Tool('delete', delete_icon, (947, Y_OFF + (grid.yCells * grid.cellSize) + 25))

def repaint():
    screen.fill((36, 81, 149))  # draw blue background
    grid.draw(screen)  # draw grid

    if grid.showLines:
        grid.draw_lines(screen)

    if server_info.is_drawing:  # only draw bottom bar if player is drawing
        topbar.is_drawing = True

        toggle_btn.draw(screen, None, None, None, None)

        if toggle_btn.hover(pygame.mouse.get_pos()):
            toggle_btn.color = Colors.HOVER
        else:
            toggle_btn.color = Colors.WHITE

        selected_color_surface.fill(palette.selected_color)
        screen.blit(selected_color_surface, (grid.xOff + toggle_btn.width + 12, Y_OFF + (grid.yCells * grid.cellSize) + 25))
        pygame.draw.rect(screen, Colors.WHITE, (grid.xOff + toggle_btn.width + 12, Y_OFF + (grid.yCells * grid.cellSize) + 25, 49, 49), 2)

        palette.draw_palette(screen)  # draw color palette

        for tool in Tool.tools:  # draw tools
            tool.draw(screen)
            if Tool.selected == tool.name:
                tool.surface.fill((150, 97, 205))  # set selected color
            else:
                tool.surface.fill(Colors.WHITE)
            if tool.hover(pygame.mouse.get_pos()) and Tool.selected != tool.name:  # hover effect
                tool.surface.fill(Colors.HOVER)
            elif Tool.selected != tool.name:
                tool.surface.fill(Colors.WHITE)

    for i, c in enumerate(connected_clients):  # draw scoreboard
        if i % 2 == 0:
            c.draw_game_widget(screen, 15, grid.yOff + i * 55, (238, 237, 239), c.uid == client.uid)
        else:
            c.draw_game_widget(screen, 15, grid.yOff + i * 55, Colors.WHITE, c.uid == client.uid)

    topbar.time = server_info.time
    if topbar.word == '' or topbar.word != server_info.word:
        topbar.word = server_info.word
    topbar.draw(screen)

def flood_fill(col, row, target_color, replacement_color):  # recursive flood fill algorithm
    if target_color == replacement_color:
        return
    elif grid.grid[col][row].color != target_color:
        return
    else:
        grid.grid[col][row].set_color(replacement_color)

        if row < 63:
            flood_fill(col, row + 1, target_color, replacement_color)
        if row > 0:
            flood_fill(col, row - 1, target_color, replacement_color)
        if col < 63:
            flood_fill(col + 1, row, target_color, replacement_color)
        if col > 0:
            flood_fill(col - 1, row, target_color, replacement_color)

    return

def main():
    while True:
        clock.tick(60)  # set fps to 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:  # clicked left mouse button
                pos = pygame.mouse.get_pos()
                if grid.xOff < pos[0] < grid.xOff + (grid.xCells * grid.cellSize) and grid.yOff < pos[1] < grid.yOff + (grid.yCells * grid.cellSize) and server_info.is_drawing:  # clicked inside the grid
                    col = (pos[0] - grid.xOff) // grid.cellSize
                    row = (pos[1] - grid.yOff) // grid.cellSize

                    if Tool.selected == 'brush':
                        grid.set_color(row, col, palette.selected_color)
                        package.grid_data = (palette.selected_color, row, col)
                        network.send(package)
                    elif Tool.selected == 'eraser':
                        grid.set_color(row, col, grid.color)
                    elif Tool.selected == 'fill':
                        flood_fill(col, row, grid.grid[col][row].color, palette.selected_color)
                    elif Tool.selected == 'eyedropper':
                        palette.selected_color = grid.grid[col][row].color

                if toggle_btn.hover(pos):  # clicked grid toggle button
                    grid.showLines = not grid.showLines
                    if grid.showLines:
                        toggle_btn.icon = grid_off_icon
                    else:
                        toggle_btn.icon = grid_on_icon

                for i in range(0, len(palette.color_cells)):
                    if palette.color_cells[i].subsurface.get_rect(topleft=palette.positions[i]).collidepoint(pos):  # clicked at a color cell from the palette
                        palette.selected_color = palette.color_cells[i].color

                if delete.hover(pos):  # clicked delete tool
                    grid.clear()
                elif brush.hover(pos):  # clicked brush tool
                    brush.set_selected()
                elif eraser.hover(pos):  # clicked eraser tool
                    eraser.set_selected()
                elif fill.hover(pos):  # clicked fill tool
                    fill.set_selected()
                elif eyedropper.hover(pos):  # clicked eyedropper tool
                    eyedropper.set_selected()

        repaint()
        pygame.display.update()

def draw_menu_title(title, color, y):
    font = pygame.font.Font('assets/fonts/pixelfont.ttf', 69)
    text_surface = font.render(title, True, color)
    screen.blit(text_surface, (MENU_SIZE[0] // 2 - text_surface.get_width() // 2, y))

def main_menu():
    global client
    username = ''
    hint_text = 'Enter your name'
    font = pygame.font.Font('assets/fonts/pixelfont.ttf', 25)
    input_rect = pygame.Rect(100, 280, 400, 44)
    color_unselected = Colors.WHITE
    color_selected = (187, 187, 187)
    selected = False
    play_button = Button((92, 184, 92), 100, 370, 400, 55, text='Play!')
    network_error = False
    run = True
    while run:
        screen.fill((36, 81, 149))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if selected:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:- 1]
                    elif event.key == pygame.K_RETURN:
                        selected = False
                    elif len(username) <= 17:
                        username += event.unicode
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                if input_rect.collidepoint(x, y):
                    selected = True
                else:
                    selected = False

                if play_button.hover((x, y)) and len(username.strip()) >= 1:  # clicked play
                    username = username.strip()
                    client = Client(username)
                    if network.connect():
                        network.send(client)
                        lobby_menu()
                    else:
                        network_error = True

        draw_menu_title('PixelDraw.io', (199, 9, 237), 150)

        play_button.draw(screen, Colors.WHITE, 'pixelfont', 31, False)
        if len(username.strip()) >= 1:
            if play_button.hover(pygame.mouse.get_pos()):
                play_button.color = (68, 157, 68)
            else:
                play_button.color = (92, 184, 92)
        else:
            play_button.color = (25, 25, 25)

        if selected:
            pygame.draw.rect(screen, color_selected, input_rect, 2)  # selected input field border
            text_surface = font.render(username, True, Colors.WHITE)
            screen.blit(text_surface, (112, 280 + 10))
        else:
            pygame.draw.rect(screen, color_unselected, input_rect, 2)  # unselected input field border
            if username.strip() == '':
                text_surface = font.render(hint_text, True, Colors.WHITE)
                screen.blit(text_surface, (112, 280 + 10))
            else:
                text_surface = font.render(username, True, Colors.WHITE)
                screen.blit(text_surface, (112, 280 + 10))

        if network_error:
            Network.draw_error_message(screen, '[NetworkError] Can\'t connect to Game-Server.', 600, 455)

        pygame.display.update()
    pygame.quit()
    sys.exit()

def handle_data():
    global server_info, connected_clients, client, start, grid
    while True:
        data = network.receive()
        if isinstance(data, list):
            connected_clients = data
            print('updated clients')
            for c in connected_clients:  # get current client
                if c.uid == client.uid:
                    client = c
        if isinstance(data, tuple) and not server_info.is_drawing:  # get grid data
            grid.grid[data[2]][data[1]].set_color(data[0])
        if isinstance(data, ServerPackage):
            server_info = data
        if data == 'start':
            start = True
        network.send(package)

def draw_lobby_title(title, x, y):
    font = pygame.font.Font('assets/fonts/pixelfont.ttf', 44)
    text_surface = font.render(title, True, (255, 255, 255))
    if title == 'Settings':
        screen.blit(text_surface, (x // 2 - text_surface.get_width() // 2, y))
    else:
        screen.blit(text_surface, (x + 150 - text_surface.get_width() // 2, y))

def lobby_menu():
    global client, connected_clients, server_info
    start_new_thread(handle_data, ())
    ready_button = Button((92, 184, 92), 100, 255 + 8 * 31, 400, 55, text='Ready?')
    while True:
        screen.fill((36, 81, 149))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:
                if ready_button.hover(pygame.mouse.get_pos()) and not client.ready:
                    package.ready = True
                    network.send(package)
                    ready_button.text = 'Ready!'

        if start:
            pygame.display.set_mode(SIZE)
            main()

        draw_menu_title('Lobby', (199, 9, 237), 36)
        draw_lobby_title('Settings', 300, 150)
        draw_lobby_title('Players', 300, 150)
        
        pygame.draw.line(screen, Colors.WHITE, (300, 155), (300, 210 + 8 * 31), 3)  # draw separator

        for i in range(0, len(connected_clients)):   # draw connected players
            if connected_clients[i].uid == client.uid:
                connected_clients[i].draw_lobby_widget(screen, 324, 208 + i * 35, True)
            else:
                connected_clients[i].draw_lobby_widget(screen, 324, 208 + i * 35, False)

        if client.ready:
            ready_button.draw(screen, (68, 157, 68), 'pixelfont', 31)
        else:
            ready_button.draw(screen, (255, 255, 255), 'pixelfont', 31)
            
        if ready_button.hover(pygame.mouse.get_pos()) and not client.ready:
            ready_button.color = (68, 157, 68)
        else:
            ready_button.color = (92, 184, 92)

        pygame.display.update()

main_menu()