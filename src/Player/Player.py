import pyautogui as gui
import pywinctl as pwc
from datetime import datetime
from pyscreeze import Box

import constants as consts

board = consts.board_mac
pieces = consts.pieces_mac
app_path = f'/Applications/Words 2.app'
app_title = 'Words 2'
scale_factor = 2


def open_app():
    windows = pwc.getWindowsWithTitle(app_title)
    game_window = windows[0]
    game_window.activate()
    return game_window


def take_screenshot():
    game_window = open_app()
    left, top = game_window.left, game_window.top
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y-%H-%M")
    screenshot = gui.screenshot(region=(
        left * scale_factor,
        top * scale_factor,
        game_window.width * scale_factor,
        game_window.height * scale_factor
    ), imageFilename="src/tests/screen_" + date_time + ".png")
    return screenshot


def drag_tile_to_board(window, tile_image, board_x, board_y, pieces_region):
    tile: Box = gui.locateOnScreen(tile_image, confidence=0.9, region=pieces_region)
    left, top = round(tile.left / 2) + 20, round(tile.top / 2) + 20
    tile_x = window.left + round(board['offset_x'] / 2) + board_x * round((board['tile_width'] + board['spacer']) / 2) + 16
    tile_y = window.top + round(board['offset_y'] / 2) + board_y * round((board['tile_width'] + board['spacer']) / 2) + 16
    gui.moveTo(left, top, duration=0.1)
    gui.dragTo(tile_x, tile_y, duration=0.1, button='left')


def play_move(move, user_tiles, board_tiles, tile_images):
    window = open_app()
    pieces_left = window.left + pieces['offset_x']
    pieces_top = window.top + pieces['offset_y']
    pieces_width = pieces_left + pieces['num_tiles'] * (pieces['tile_width'] + pieces['spacer'])
    pieces_height = pieces_top + pieces['num_tiles'] * pieces['tile_height']
    pieces_region = (pieces_left, pieces_top, pieces_width, pieces_height)
    [word, coords, vertical, *_] = move
    start_x = coords[0] + 1
    start_y = coords[1] + 1
    for i in range(len(word)):
        character = word[i]
        board_x = start_x + i if not vertical else start_x
        board_y = start_y + i if vertical else start_y
        try:
            piece_index = user_tiles.index(character)
        except ValueError:
            continue
        print(character)
        tile_image = tile_images[piece_index]
        user_tiles[piece_index] = False
        drag_tile_to_board(window, tile_image, board_x, board_y, pieces_region)
