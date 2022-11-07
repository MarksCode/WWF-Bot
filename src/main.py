import os
import time
from playwright_utils import PlaywrightManager
from ImageProcessor.ImageProcessor import extract_pieces, extract_board
from WordFinder.WordFinder import WordFinder
from Scraper.Scraper import GameScraper
from Player.Player import Player
from logger import logger
import asyncio
import pyautogui as gui
import constants as consts


async def game_loop(
        whos_turn,
        player_1,
        player_2,
        word_finder,
        game_scraper,
        iteration,
        pass_count=0,
        start_new_game=False
):
    logger.log("~~~  Starting game loop: " + str(iteration) + "  ~~~")
    print('whos_turn', whos_turn)
    if start_new_game:
        await initialize_new_game(whos_turn)
        await game_scraper.initialize_game()
        await word_finder.reset_board()
        _, board, user_tiles = await game_scraper.get_game_data()
        tiles_1 = user_tiles[consts.user_ids[consts.player_A]]
        tiles_2 = user_tiles[consts.user_ids[consts.player_B]]
        player_1.set_tiles(tiles_1)
        player_2.set_tiles(tiles_2)
    move_result = {}
    if whos_turn == consts.player_nums[consts.player_A]:
        move_result = await play(player_1, word_finder, game_scraper, iteration)
        whos_turn = consts.player_nums[consts.player_B]
    elif whos_turn == consts.player_nums[consts.player_B]:
        move_result = await play(player_2, word_finder, game_scraper, iteration)
        whos_turn = consts.player_nums[consts.player_A]
    else:
        logger.log("No move played detected")
    did_pass = move_result['did_pass']
    if did_pass:
        pass_count += 1
    else:
        pass_count = 0
    is_over = move_result['is_over']
    if pass_count > 2:
        pass_count = 0
        is_over = True
    await asyncio.sleep(3)
    await game_loop(
        whos_turn,
        player_1,
        player_2,
        word_finder,
        game_scraper,
        iteration + 1,
        pass_count,
        is_over
    )


async def play(player, word_finder, game_scraper, iteration):
    # await asyncio.sleep(1)
    tiles = player.get_tiles()
    board = word_finder.get_board()
    logger.log("User Tiles: " + str(tiles))
    print('User Tiles: ', tiles)
    moves = await word_finder.find_moves(tiles)
    screenshot = player.take_screenshot()
    tile_images = extract_pieces(screenshot)
    move = player.start_play_move(moves, board, tile_images)
    letters_played = move['letters_played']
    move_played = move['move']
    did_pass = move['did_pass']
    await asyncio.sleep(1)
    if move_played is False:
        if did_pass:
            return {'did_play': False, 'did_pass': True, 'is_over': False}
        else:
            player.restart_app(True)
            player.open_game()
            await asyncio.sleep(3)
            return await play(player, word_finder, game_scraper, iteration)
    await word_finder.add_move(move_played)
    new_letters = game_scraper.get_tiles(letters_played)
    player_tiles = player.add_tiles(new_letters)
    if len(player_tiles) == 0:
        return {'did_play': True, 'did_pass': False, 'is_over': True}
    return {'did_play': True, 'did_pass': False, 'is_over': False}


async def initialize_new_game(whos_turn=consts.player_nums[consts.player_A]):
    player_1 = Player(consts.player_nums[consts.player_A])
    player_2 = Player(consts.player_nums[consts.player_B])
    player_to_start_new_game = player_1 if whos_turn == consts.player_nums[consts.player_A] else player_2
    player_to_accept_game = player_2 if whos_turn == consts.player_nums[consts.player_A] else player_1
    await asyncio.sleep(3)
    player_to_accept_game.restart_app()
    player_to_start_new_game.click_screen()
    player_to_start_new_game.restart_app(True)
    player_to_start_new_game.start_new_game()
    await asyncio.sleep(8)
    player_to_start_new_game.press_pass_move()
    player_to_accept_game.open_game()
    player_to_accept_game.press_accept_challenge()
    await asyncio.sleep(5)
    player_to_accept_game.press_pass_move()


async def start_game(game_scraper, word_finder):
    _, board, user_tiles = await game_scraper.get_game_data()
    player_1_tiles = user_tiles[consts.user_ids[consts.player_A]]
    player_2_tiles = user_tiles[consts.user_ids[consts.player_B]]
    player_1 = Player(
        consts.player_nums[consts.player_A],
        player_1_tiles,
    )
    player_2 = Player(
        consts.player_nums[consts.player_B],
        player_2_tiles
    )
    await word_finder.initialize_board(board)
    whos_turn = await game_scraper.check_whos_turn()
    await game_loop(whos_turn, player_1, player_2, word_finder, game_scraper, 0)


async def main():
    # playwright_manager = PlaywrightManager()
    # await playwright_manager.initialize()
    # word_finder = WordFinder(playwright_manager)
    # game_scraper = GameScraper(playwright_manager, consts.player_A, consts.player_B)
    # # await initialize_new_game()
    # await word_finder.initialize()
    # await game_scraper.initialize()
    # await asyncio.sleep(2)
    # await start_game(game_scraper, word_finder)

    # await asyncio.sleep(2)
    # player_1 = Player(consts.player_nums[consts.player_A])
    # player_1.move()
    player_2 = Player(consts.player_nums[consts.player_B])
    # player_2.refresh_lobby()
    player_2.take_screenshot(True)
    # player_2.press_blank_tile_letter('S')
    # player_1.press_play_button()


if __name__ == '__main__':
    logger.log("Starting Program")
    asyncio.run(main())

