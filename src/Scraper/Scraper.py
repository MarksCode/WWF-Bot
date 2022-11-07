import asyncio
import json5
from os import path
from playwright.async_api import Page
from datetime import datetime
from logger import logger
import constants as consts
import config

window_game_ids = '''
    () => {
        const games = window.wwf.game.Manager.getGames().filter(
            (g) => g._data?.users?.every(
                (u) => u._data.id == USER_ID_1 || u._data.id == USER_ID_2
            )
        )
        const ids = Object.fromEntries(
            games.map((g) => ([g._data.id, true]))
        );
        return JSON.stringify(ids);
    }
'''

window_game_id = '''
    () => {
        const games = window.wwf.game.Manager.getGames().filter(
            (g) => g._data?.users?.every(
                (u) => u._data.id == USER_ID_1 || u._data.id == USER_ID_2
            )
        )
        games.sort((a, b) => {
            createdAt1 = new Date(a._data.created_at);
            createdAt2 = new Date(b._data.created_at);
            return createdAt2 - createdAt1;
        })
        const game = games[0]
        const gameId = game['_data']['id']
        const bag = new wwf.Bag(game);
        const userTiles = wwf.utils.Shared.convertMovesToPulls(game, bag);
        const remainingTiles = [];
        while (true) {
            const nextTile = bag.pullLetter();
            if (nextTile) {
                remainingTiles.push(nextTile);
            } else {
                break;
            }
        }
        return JSON.stringify({ gameId, remainingTiles });
    }
'''

window_game = '''
    JSON.stringify(
        window.wwf.game.Manager.getGame(GAME_ID)
    )
'''

window_tiles = '''
    () => {
        const g = window.wwf.game.Manager.getGame(GAME_ID);
        const b = new wwf.Bag(g);
        const userTiles = wwf.utils.Shared.convertMovesToPulls(g, b);
        const user1Tiles = userTiles['USER_ID_1']
        const user2Tiles = userTiles['USER_ID_2']
        const user1Letters = user1Tiles.map((t) => t.letter);
        const user2Letters = user2Tiles.map((t) => t.letter);
        const letters = {
            'USER_ID_1': user1Letters,
            'USER_ID_2': user2Letters
        };
        return JSON.stringify(letters)
    }
'''

window_board = '''
    () => {
        const g = window.wwf.game.Manager.getGame(GAME_ID);
        const b = new wwf.Bag(g);
        const tiles = wwf.utils.Shared.convertMovesToTiles(g, b);
        return JSON.stringify(tiles)
    }
'''


def construct_board(board_letters=[]):
    board = [[False for _i in range(15)] for _j in range(15)]
    for tile in board_letters:
        index, letter = tile['index'], tile['letter']
        row, col = index // 15, index % 15
        board[row][col] = letter
    return board


def dump_json(obj):
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y-%H-%M")
    log_file_name = "logs/game_" + date_time + ".log"
    log_file_name = path.join(config.root, log_file_name)
    with open(log_file_name, 'w') as convert_file:
        convert_file.write(json5.dumps(obj, indent=4, quote_keys=True))


class GameScraper:
    def __init__(self, playwright_manager, user_1, user_2):
        self.playwright_manager = playwright_manager
        self.page = None
        self.user_id_1 = consts.user_ids[user_1]
        self.user_id_2 = consts.user_ids[user_2]
        self.player_1 = consts.player_nums[user_1]
        self.player_2 = consts.player_nums[user_2]
        self.move_index = 0
        self.game_ids = None
        self.game_id = None
        self.remaining_tiles = []
        self.num_games_played = 0

    async def initialize(self):
        page: Page = await self.playwright_manager.open_page('https://wordswithfriends.com/')
        self.page = page
        try:
            await page.click('button.play-now-btn', timeout=2000)
        except (Exception,):
            pass
        await page.pause()  # User Login
        await self.initialize_game(True)

    async def initialize_game(self, is_first_init=False):
        if is_first_init:
            game_ids = await self.get_game_ids()
            self.game_ids = game_ids
        else:
            new_game_id = False
            while not new_game_id:
                game_ids = await self.get_game_ids()
                for game_id in game_ids.keys():
                    if game_id not in self.game_ids:
                        new_game_id = game_id
                        self.game_ids[game_id] = True
                        break
                await asyncio.sleep(3)

        page = self.page
        frame = await page.query_selector('iframe[id=\"gameScreen\"]')
        content = await frame.content_frame()
        evaluate_game_id_fn = window_game_id\
            .replace('USER_ID_1', self.user_id_1)\
            .replace('USER_ID_2', self.user_id_2)
        game_data = await content.evaluate(evaluate_game_id_fn)
        game_data = json5.loads(game_data)
        game_id = game_data['gameId']
        remaining_tiles = game_data['remainingTiles']
        logger.log('Game ID: ' + str(game_id))
        self.remaining_tiles = remaining_tiles
        self.game_id = game_id

    def get_tiles(self, num_tiles):
        letters = []
        for i in range(num_tiles):
            if len(self.remaining_tiles) == 0:
                break
            else:
                tile = self.remaining_tiles.pop(0)
                letters.append(tile['letter'])
        return letters

    async def get_game_ids(self):
        page = self.page
        frame = await page.query_selector('iframe[id=\"gameScreen\"]')
        content = await frame.content_frame()
        evaluate_game_ids_fn = window_game_ids\
            .replace('USER_ID_1', self.user_id_1)\
            .replace('USER_ID_2', self.user_id_2)
        game_ids_json = await content.evaluate(evaluate_game_ids_fn)
        game_ids = json5.loads(game_ids_json)
        return game_ids

    async def get_game_data(self):
        page = self.page
        frame = await page.query_selector('iframe[id=\"gameScreen\"]')
        content = await frame.content_frame()
        evaluate_game_fn = window_game.replace('GAME_ID', self.game_id)
        evaluate_board_fn = window_board.replace('GAME_ID', self.game_id)
        evaluate_tiles_fn = window_tiles\
            .replace('USER_ID_1', self.user_id_1)\
            .replace('USER_ID_2', self.user_id_2)\
            .replace('GAME_ID', self.game_id)
        game = await content.evaluate(evaluate_game_fn)
        board_tiles = await content.evaluate(evaluate_board_fn)
        tiles = await content.evaluate(evaluate_tiles_fn)
        game_json = json5.loads(json5.loads(game))
        # try:
        #     dump_json(game_json)
        # except (Exception,):
        #     pass
        board_letters = json5.loads(board_tiles)
        tiles_json = json5.loads(tiles)
        return game_json, construct_board(board_letters), tiles_json

    async def check_whos_turn(self):
        game_data, _, _ = await self.get_game_data()
        last_move = game_data['data']['last_move']
        if last_move:
            user_id = str(last_move['user_id'])
            move_index = last_move['move_index']
            print(f'Current move: {self.move_index}. Last move: {str(move_index)}. User_id: {user_id} ')
            if move_index == 0 or move_index > self.move_index:
                self.move_index = move_index
                if user_id == self.user_id_1:
                    return self.player_2
                elif user_id == self.user_id_2:
                    return self.player_1
            return -1
        return -1
