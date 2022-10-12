from ImageProcessor.ImageProcessor import TextExtractor
from WordFinder.WordFinder import WordFinder
from Scraper.Scraper import GameScraper, construct_board
from Player.Player import take_screenshot, play_move
from Scraper.data import game_data
import asyncio

img = r'tests/screen_10-12-2022-14-24.png'


async def main():
    word_finder = WordFinder()
    game_scraper = GameScraper()
    await word_finder.initialize()
    await game_scraper.initialize()
    board = await game_scraper.get_game_data()
    screenshot = take_screenshot()
    text_extractor = TextExtractor(screenshot, False, False)
    [user_tiles, tile_images] = text_extractor.extract_pieces()
    moves = await word_finder.find_moves(user_tiles, board)
    play_move(moves[0], user_tiles, board, tile_images)


if __name__ == '__main__':
    asyncio.run(main())

