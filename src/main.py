from ImageProcessor.ImageProcessor import TextExtractor
from WordFinder.WordFinder import launch_playwright
from Player.Player import take_screenshot, play_move
import asyncio

img = r'tests/screenshot.png'
# C D '' S T V T
img_empty = r'tests/screenshot_empty.png'
# R W N A D A E
img_wildcard = r'tests/s_wildcard.png'
# R S ? E I I A
img_1 = r'tests/s_1.png'
# T T V C M R E
img_2 = r'tests/s_2.png'
# I E F I A R I
img_3 = r'tests/s_3.png'
img_4 = r'tests/s_4.png'
img_5 = r'tests/s_5.png'
img_PIL_1 = r'tests/PIL_Screen_1.png'
img_PIL_Empty = r'tests/PIL_Screen_Empty.png'
img_PIL_2 = r'tests/PIL_Screen_2.png'


async def main():
    screenshot = take_screenshot()
    text_extractor = TextExtractor(screenshot, False, False)
    board_tiles = text_extractor.extract_board()
    user_tiles = text_extractor.extract_pieces()
    moves = await launch_playwright(board_tiles, user_tiles)
    # print(user_tiles)
    # move = ['TERM', [8, 14], 0, ['AT']]
    board_tiles = []
    play_move(moves[0], user_tiles, board_tiles)
    # print(moves)


if __name__ == '__main__':
    asyncio.run(main())

