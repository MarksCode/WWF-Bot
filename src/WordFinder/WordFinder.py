import asyncio

from utils import construct_board


def construct_el_id(row, col):
    return '#s_' + str(col) + '_' + str(row)


class WordFinder:
    def __init__(self, playwright_manager):
        self.playwright_manager = playwright_manager
        self.page = None
        self.board = None

    async def initialize(self):
        page = await self.playwright_manager.open_page('https://www.scrabulizer.com/')
        self.page = page

    async def initialize_board(self, board):
        page = self.page
        await self.reset_board()
        self.board = board
        await page.locator('#staticDesignSelect').select_option('wordsWithFriends')
        await page.wait_for_timeout(300)
        for i in range(15):
            for y in range(15):
                letter = board[i][y]
                if letter:
                    await page.click(construct_el_id(i, y))
                    await page.keyboard.type(letter)

    async def reset_board(self):
        page = self.page
        self.board = construct_board()
        page.on("dialog", lambda dialog: dialog.accept())
        try:
            await page.click('#clearBoardButton', timeout=5000)
        except (Exception,):
            pass
        try:
            await page.click('#clearRackBtn', timeout=5000)
        except (Exception,):
            pass

    def get_board(self):
        return self.board

    async def add_move(self, move):
        page = self.page
        try:
            await page.click('#move_0', timeout=2000)
        except (Exception,):
            pass
        [word, coords, vertical, *_] = move
        start_x = coords[0]
        start_y = coords[1]
        for i in range(len(word)):
            letter = word[i].upper()
            board_column = start_x + i if not vertical else start_x
            board_row = start_y + i if vertical else start_y
            self.board[board_row][board_column] = letter
            await page.click(construct_el_id(board_row, board_column))
            await page.keyboard.type(letter)

    async def find_moves(self, user_tiles):
        page = self.page
        try:
            await page.click('#clearRackBtn', timeout=2000)
        except (Exception,):
            pass
        for i in range(7):
            el_id = '#rack_' + str(i)
            try:
                letter = user_tiles[i]
                if letter:
                    await page.click(el_id)
                    if letter == '.':
                        await page.keyboard.press('Space')
                    else:
                        await page.keyboard.type(letter)
            except (Exception,):
                pass
        await page.wait_for_timeout(500)

        res = False
        while not res:
            try:
                res = await self.get_response()
            except (Exception,):
                await asyncio.sleep(2)
                pass

        if 'moves' in res:
            return res['moves']
        return []

    async def get_response(self):
        page = self.page
        async with page.expect_response(r'https://www.scrabulizer.com/solver/results', timeout=5000) as res:
            await page.click('button.get-solutions')
        response = await res.value
        response_json = await response.json()
        return response_json

