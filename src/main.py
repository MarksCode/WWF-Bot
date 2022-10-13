from ImageProcessor.ImageProcessor import TextExtractor
from WordFinder.WordFinder import WordFinder
from Scraper.Scraper import GameScraper
from Player.Player import take_screenshot, play_move
from logger import Logger
import asyncio
import random

logger = Logger()


async def game_loop(word_finder, game_scraper, iteration):
    logger.log("~~~  Starting game loop: " + str(iteration) + "  ~~~")
    has_move_been_played = await game_scraper.check_if_move_played()
    if has_move_been_played:
        await play(word_finder, game_scraper)
        await game_loop(word_finder, game_scraper, iteration + 1)
    else:
        logger.log("No move played detected")
        await asyncio.sleep(10)
        await game_loop(word_finder, game_scraper, iteration + 1)


async def play(word_finder, game_scraper):
    board = await game_scraper.get_board()
    logger.log("Board: " + str(board))
    screenshot = take_screenshot()
    text_extractor = TextExtractor(screenshot, False, False)
    [user_tiles, tile_images] = text_extractor.extract_pieces()
    logger.log("User Tiles: " + str(user_tiles))
    print(user_tiles)
    moves = await word_finder.find_moves(user_tiles, board)
    move = random.choice(moves)
    logger.log("Move: " + str(move))
    print(move)
    play_move(move, user_tiles, board, tile_images)


async def main():
    screenshot = take_screenshot(True)
    word_finder = WordFinder()
    game_scraper = GameScraper()
    await word_finder.initialize()
    await game_scraper.initialize()
    await game_loop(word_finder, game_scraper, 0)


if __name__ == '__main__':
    logger.log("Starting Program")
    asyncio.run(main())

