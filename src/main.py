from ImageProcessor.ImageProcessor import TextExtractor
from WordFinder.WordFinder import WordFinder
from Scraper.Scraper import GameScraper
from Player.Player import take_screenshot, play_move
import asyncio


async def main():
    word_finder = WordFinder()
    game_scraper = GameScraper()
    await word_finder.initialize()
    await game_scraper.initialize()
    board = await game_scraper.get_game_data()
    screenshot = take_screenshot()
    text_extractor = TextExtractor(screenshot, False, False)
    [user_tiles, tile_images] = text_extractor.extract_pieces()
    print(user_tiles)
    moves = await word_finder.find_moves(user_tiles, board)
    play_move(moves[0], user_tiles, board, tile_images)


if __name__ == '__main__':
    asyncio.run(main())

