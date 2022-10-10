import pyautogui as gui
import os
import pywinctl as pwc
from PIL import ImageGrab
import constants as consts
board = consts.board
pieces = consts.pieces
app_path = f'/Applications/Words 2.app'
app_title = 'Words 2'

window = pwc.getWindowsWithTitle(app_title)[0]


def open_app():
    os.system("open \"{}\"".format(app_path))


def get_app():
    windows = pwc.getWindowsWithTitle(app_title)
    return windows[0]


def take_screenshot():
    open_app()
    screenshot = ImageGrab.grab(bbox=(window.left, window.top, window.right, window.bottom))
    return screenshot


def get_piece_coords(index):
    x = window.left + pieces['offset_x'] + index * (pieces['tile_width'] + pieces['spacer']) + 5
    y = window.top + pieces['offset_y'] + 5
    gui.moveTo(x + 8, y + 8, duration=0.2)


def drag_to_tile(x, y):
    tile_x = window.left + board['offset_x'] + x * (board['tile_width'] + board['spacer']) + 4
    tile_y = window.top + board['offset_y'] + y * (board['tile_width'] + board['spacer']) + 4
    gui.dragTo(tile_x, tile_y, duration=0.2, button='left')


# ['TERM', [8, 14], 0, ['AT']]
def play_move(move, user_tiles, board_tiles):
    open_app()
    [word, coords, vertical, *_] = move
    [start_x, start_y] = coords
    for i in range(0, len(word)):
        character = word[i]
        piece_index = user_tiles.index(character)
        user_tiles[piece_index] = False
        x = start_x + i if not vertical else start_x
        y = start_y + i if vertical else start_y
        get_piece_coords(piece_index)
        drag_to_tile(x, y)
