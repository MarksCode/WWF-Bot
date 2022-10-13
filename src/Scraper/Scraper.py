import json5
from playwright.async_api import Page
from typing import Callable
from playwright_utils import launch_playwright


window_game = '''
    JSON.stringify(
        window.wwf.game.Manager.getGames().filter(
            (g) => g._data.users.some(
                (u) => u._data.id === 260794988
            )
        )[0]
    )
'''

window_game_2 = '''
    window.wwf.game.Manager.getGames().filter(
        (g) => g._data.users.some(
            (u) => u._data.id === 260794988
        )
    )[0]
'''


def construct_board(game_data):
    data = game_data['data']
    moves = data['moves']
    board = [[' ' for _i in range(15)] for _j in range(15)]
    for move in moves:
        words, from_x, from_y, to_x, to_y = move['words'], move['from_x'], move['from_y'], move['to_x'], move[
            'to_y']
        word, start_x, start_y, end_x, end_y = words[0].upper(), from_x, from_y, to_x, to_y
        for i in range(len(word)):
            x = start_x + i if start_x != end_x else start_x
            y = start_y + i if start_y != end_y else start_y
            board[y][x] = word[i]
    return board


class GameScraper:
    def __init__(self):
        self.page = None
        self.cleanup_fn = None
        self.num_moves = 0

    async def initialize(self):
        page: Page
        cleanup_fn: Callable
        [page, cleanup_fn] = await launch_playwright('https://wordswithfriends.com/')
        await page.pause()  # User Login
        await page.wait_for_selector('iframe[id=\"gameScreen\"]')
        self.page = page
        self.cleanup_fn = cleanup_fn

    async def get_game_data(self):
        page = self.page
        frame = await page.query_selector('iframe[id=\"gameScreen\"]')
        content = await frame.content_frame()
        game = await content.evaluate(window_game)
        game_json = json5.loads(json5.loads(game))
        return game_json

    async def get_board(self):
        game_data = await self.get_game_data()
        return construct_board(game_data)

    async def check_if_move_played(self):
        game_data = await self.get_game_data()
        moves = game_data['data']['moves']
        if len(moves) > self.num_moves + 1 or self.num_moves == 0:
            self.num_moves = len(moves)
            return True
        return False
