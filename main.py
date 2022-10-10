from ImageProcessor.ImageProcessor import TextExtractor
from WordFinder.WordFinder import launch_playwright
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


async def main():
    text_extractor = TextExtractor(img_1, False, False)
    board_tiles = text_extractor.extract_board()
    user_tiles = text_extractor.extract_pieces()
    moves = await launch_playwright(board_tiles, user_tiles)
    print(moves)


if __name__ == '__main__':
    asyncio.run(main())

