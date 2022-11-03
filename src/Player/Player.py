from os import path, system
import subprocess
from random import randrange
import pyautogui as gui
import pywinctl as pwc
from datetime import datetime
from logger import logger
from time import sleep
from PIL import Image
import psutil
import constants as consts
import config


board = consts.board_win if consts.is_windows else consts.board_mac
pieces = consts.pieces_win if consts.is_windows else consts.pieces_mac
app_path_mac = f'/Applications/Words 2.app'
app_title_mac = 'Words 2'
app_titles_win = [
    'BlueStacks App Player 1',
    'BlueStacks App Player'
]
app_paths_win = [
    r"C:\\Users\\sendm\\Desktop\\Words2_2.lnk",
    r"C:\\Users\\sendm\\Desktop\\Words2_1.lnk"
]


class Player:
    def __init__(self, player_num, starting_tiles=[]):
        self.tiles = starting_tiles
        self.opponent = consts.opponents[player_num]
        self.player_num = player_num
        self.window = None
        self.available_moves = None
        self.current_move_pool = None
        self.centerX, self.centerY, self.left, self.top, self.right, self.bottom, self.width, self.height =\
            None, None, None, None, None, None, None, None
        self.pieces_region = None
        self.init_game_window()

    def init_game_window(self):
        title = app_titles_win[self.player_num]
        all_windows = pwc.getAllWindows()
        game_window = None
        for window in all_windows:
            if window.title == title:
                game_window = window
                break

        self.window = game_window
        self.centerX = round(window.centerx * consts.scale_factor)
        self.centerY = round(window.centery * consts.scale_factor)
        self.left = round(game_window.left * consts.scale_factor)
        self.top = round(game_window.top * consts.scale_factor)
        self.right = round(game_window.right * consts.scale_factor)
        self.bottom = round(game_window.bottom * consts.scale_factor)
        self.width = round(game_window.width * consts.scale_factor)
        self.height = round(game_window.height * consts.scale_factor)
        pieces_left = round(round(self.left / consts.scale_factor) + pieces['offset_x'] - 30)
        pieces_top = round(round(self.top / consts.scale_factor) + pieces['offset_y'] - 30)
        pieces_width = round(pieces_left + pieces['num_tiles'] * (pieces['tile_width'] + pieces['spacer']) + 30)
        pieces_height = round(pieces_top + pieces['num_tiles'] * pieces['tile_height'] + 30)
        pieces_region = (pieces_left, pieces_top, pieces_width, pieces_height)
        self.pieces_region = pieces_region

    def add_tiles(self, letters):
        for letter in letters:
            self.tiles.append(letter)
        return self.tiles

    def set_tiles(self, letters):
        self.tiles = letters

    def get_tiles(self):
        return self.tiles

    def activate_app(self):
        if consts.is_windows:
            pass
        else:
            self.window.activate()

    def open_app(self):
        if consts.is_windows:
            app_path = app_paths_win[self.player_num]
            subprocess.call(app_path, shell=True)
            sleep(1)
        else:
            system("open \"{}\"".format(app_path_mac))
            sleep(4)

    def move(self):
        gui.moveTo(self.centerX, self.top + 570, duration=0.3)

    def check_if_game_loaded(self):
        gui.moveTo(self.left + 10, self.top + 400, duration=0.2)
        sleep(0.3)
        gui.doubleClick(button="left", interval=0.5)
        img = path.join(config.root, 'images/lobby.png')
        try:
            gui.locateOnScreen(img, confidence=0.9, grayscale=True, region=(
                self.centerX - 120,
                self.bottom - 140,
                160,
                130
            ))
            print('Game loaded')
            return True
        except(Exception,):
            print('Game not loaded')
            return False

    @staticmethod
    def quit_app():
        if consts.is_windows:
            gui.hotkey('ctrl', 'shift', '5')
            sleep(0.5)
            gui.press('delete', 2, 0.5)
        else:
            for proc in psutil.process_iter():
                try:
                    if proc.name() == 'Words3':
                        proc.terminate()
                except psutil.NoSuchProcess:
                    pass

    def open_game(self):
        print('Opening game')
        gui.moveTo(self.left + 10, self.top + 400, duration=0.2)
        gui.click(button="left")
        gui.moveTo(self.centerX, self.centerY, duration=0.2)
        img = path.join(
            config.root,
            consts.profile_imgs[self.player_num]
        )
        retries = 0
        while retries < 10:
            try:
                x, y = gui.locateCenterOnScreen(
                    img,
                    confidence=0.95,
                    region=(self.left, self.top + 400, 400, 1400)
                )
                gui.moveTo(x, y, duration=0.3)
                sleep(0.2)
                gui.doubleClick(interval=0.5, button="left")
                sleep(0.5)
                return
            except (Exception,):
                retries += 1
                gui.scroll(-40)
                sleep(2)
        self.restart_app(True)
        self.open_game()

    def restart_app(self, sleep_after=False):
        sleep(0.5)
        self.quit_app()
        sleep(1)
        self.open_app()
        if sleep_after:
            sleep(12)

    def start_new_game(self):
        print('Starting New Game')
        opponent_user_name = consts.opponent_user_names[self.player_num]
        gui.moveTo(self.right - 150, self.bottom - 200, duration=0.3)
        sleep(0.5)
        gui.doubleClick(interval=0.5, button='left')
        sleep(1.4)
        gui.moveTo(self.right - 150, self.bottom - 650, duration=0.3)
        sleep(0.5)
        gui.click(button='left')
        sleep(0.5)
        gui.write(opponent_user_name, interval=0.2)
        sleep(0.5)
        gui.moveTo(
            self.centerX - 75,
            self.centerY + 180,
            duration=0.2
        )
        sleep(0.5)
        gui.doubleClick(interval=0.5, button='left')
        sleep(1)
        confirm_img = 'images/new_game_confirm.png'
        region = (self.centerX - 320, self.centerY + 250, 600, 200)
        while True:
            try:
                x, y = gui.locateCenterOnScreen(
                    confirm_img,
                    confidence=0.9,
                    region=region
                )
                gui.click(x, y, button="left")
                break
            except (Exception,):
                sleep(3)

    def press_accept_challenge(self):
        confirm_img = 'images/accept_challenge.png'
        region = (self.centerX - 320, self.bottom - 300, 600, 200)
        while True:
            try:
                x, y = gui.locateCenterOnScreen(
                    confirm_img,
                    confidence=0.9,
                    region=region
                )
                gui.moveTo(x, y, duration=0.3)
                gui.click(button="left")
                break
            except (Exception,):
                sleep(1)
                pass

    def take_screenshot(self, save_screenshot=False):
        now = datetime.now()
        date_time = now.strftime("%m-%d-%Y-%H-%M")
        file_name = "tests/screen_" + date_time + ".png"
        file_name = path.join(config.root, file_name) if save_screenshot else None
        screenshot = gui.screenshot(region=(
            self.left,
            self.top,
            self.width,
            self.height
        ), imageFilename=file_name)
        # region = (286, 1906, 787, 2256)
        # screen = gui.screenshot()
        # draw = ImageDraw.Draw(screen)
        # draw.rectangle(region, outline='red')
        # screen.show()
        return screenshot

    def press_recall(self):
        gui.moveTo(self.right - 150, self.bottom - 50, duration=0.4)
        gui.click()
        sleep(2)

    def press_play_button(self):
        button_x = self.centerX - 50
        button_y = self.bottom - 50
        gui.moveTo(button_x, button_y, duration=0.4)
        sleep(0.2)
        # gui.moveTo(self.centerX - 20, self.bottom - 50, duration=0.3)
        gui.click(button='left')

    def press_confirm_move(self):
        image = f'images\confirm_move_button_{consts.platform}.png'
        x, y = gui.locateCenterOnScreen(path.join(config.root, image), confidence=0.9, grayscale=True, region=(
            self.centerX - 350,
            self.centerY - 100,
            650,
            350
        ))
        button_x = round(x / consts.scale_factor)
        button_y = round(y / consts.scale_factor)
        gui.moveTo(button_x, button_y, duration=0.3)
        # gui.moveTo(self.centerX, self.centerY + 50, duration=0.3)
        gui.click(button='left')

    def press_pass_move(self):
        print('Passing move')
        gui.moveTo(self.centerX - 310, self.bottom - 60, duration=0.4)
        sleep(0.5)
        gui.doubleClick(interval=0.5, button='left')
        sleep(2)
        image = f'images\confirm_pass_move.png'
        x, y = gui.locateCenterOnScreen(
            path.join(config.root, image),
            confidence=0.9,
            region=(self.centerX - 350, self.centerY - 100, 650, 350))
        gui.moveTo(x, y, duration=0.3)
        gui.doubleClick(interval=0.5, button='left')

    @staticmethod
    def press_ok_button():
        gui.press('Escape')

    def press_blank_tile_letter(self, letter):
        spacer = 80
        base_x = self.centerX - 230
        base_y = self.top + 480
        cols = 6
        index = consts.letters.index(letter.upper())
        row = index // cols
        col = index % cols
        gui.moveTo(base_x + col * spacer, base_y + row * spacer, duration=0.4)
        sleep(0.2)
        gui.click(button="left")

    def drag_tile_to_board(self, character, tile_image, board_x, board_y, is_blank=False):
        try:
            piece_x, piece_y = gui.locateCenterOnScreen(tile_image, confidence=0.98, region=self.pieces_region)
            left, top = round(piece_x / consts.scale_factor), round(piece_y / consts.scale_factor)
            gui.moveTo(left, top, duration=0.2)
        except (Exception,):
            pass
        tile_x = round(self.left / consts.scale_factor) + round(board['offset_x'] / consts.scale_factor) +\
                 board_x * round((board['tile_width'] + board['spacer']) / consts.scale_factor) + 20
        tile_y = round(self.top / consts.scale_factor) + round(board['offset_y'] / consts.scale_factor) +\
                 board_y * round((board['tile_width'] + board['spacer']) / consts.scale_factor) + 20
        if consts.is_windows:
            gui.mouseDown()
            gui.moveTo(tile_x, tile_y, duration=0.5)
            sleep(0.3)
            gui.mouseUp()
        else:
            gui.dragTo(tile_x, tile_y, duration=0.5, button="left")

        if is_blank:
            sleep(1)
            self.press_blank_tile_letter(character)

    def start_play_move(self, moves, board_tiles, tile_images):
        self.available_moves = moves
        self.current_move_pool = moves[:5]
        return self.play_move(board_tiles, tile_images)

    def choose_move(self):
        if len(self.current_move_pool) == 0:
            if len(self.available_moves) == 0:
                return False
            self.current_move_pool = self.available_moves[:5]
            self.available_moves = self.available_moves[5:]

        rand_index = randrange(len(self.current_move_pool))
        move = self.current_move_pool[rand_index]
        self.current_move_pool.pop(rand_index)
        return move

    def play_move(self, board_tiles, tile_images):
        move = self.choose_move()
        logger.log("Playing move: " + str(move))
        print('Playing move: ', move)
        if move is False:
            self.press_pass_move()
            return False, 0
            return False, 0
        tiles_copy = self.tiles.copy()
        letters_played = 0
        [word, coords, vertical, *_] = move
        start_x = coords[0]
        start_y = coords[1]
        for i in range(len(word)):
            character = word[i].upper()
            board_x = start_x + i if not vertical else start_x
            board_y = start_y + i if vertical else start_y
            existing_tile = board_tiles[board_y][board_x]
            if existing_tile:
                continue
            is_blank = False
            try:
                piece_index = tiles_copy.index(character)
            except ValueError:
                piece_index = tiles_copy.index('.')
                is_blank = True
            tile_image = tile_images[piece_index]
            tiles_copy[piece_index] = False
            self.drag_tile_to_board(character, tile_image, board_x, board_y, is_blank)
            letters_played += 1
            sleep(1)
        sleep(0.2)
        try:
            print('Pressing play')
            self.press_play_button()
        except (Exception,):
            self.take_screenshot(True)
            print('Error pressing play button')
            logger.log('Error pressing play button')
        sleep(0.5)
        try:
            print('Confirming move')
            self.press_confirm_move()
            new_tiles = []
            for tile in tiles_copy:
                if tile:
                    new_tiles.append(tile)
            self.tiles = new_tiles
            return move, letters_played
        except (Exception,):  # Invalid move played, try new move
            print('Error pressing confirm')
            logger.log('Error pressing confirm move button')
            self.press_ok_button()
            self.press_recall()
            sleep(0.5)
            return self.play_move(board_tiles, tile_images)
