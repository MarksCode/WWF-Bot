from playwright_utils import launch_playwright


class WordFinder:
    def __init__(self):
        self.page = None
        self.cleanup_fn = None

    async def initialize(self):
        [page, cleanup_fn] = await launch_playwright('https://www.scrabulizer.com/')
        self.page = page
        self.cleanup_fn = cleanup_fn

    async def find_moves(self, user_tiles, board):
        page = self.page
        await page.locator('#staticDesignSelect').select_option('wordsWithFriends')
        await page.wait_for_timeout(300)
        await page.click('#s_0_0')
        for row in board:
            for i in range(len(row)):
                letter = row[i]
                if letter and letter.strip():
                    await page.keyboard.type(letter)
                elif i != len(row) - 1:
                    await page.keyboard.press('Tab')
            await page.keyboard.press('Tab')

        for letter in user_tiles:
            if letter:
                if letter == '?':
                    await page.keyboard.type('Space')
                else:
                    await page.keyboard.type(letter)

        async with page.expect_response(r'https://www.scrabulizer.com/solver/results') as response_info:
            await page.click('button.get-solutions')

        response = await response_info.value
        response_json = await response.json()
        return response_json['moves']

