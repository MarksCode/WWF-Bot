from . import constants
import asyncio
import re
from playwright.async_api import async_playwright


async def launch_playwright(board_tiles, user_tiles):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        moves = await find_word(context, board_tiles, user_tiles)
        await context.close()
        await browser.close()
        return moves


async def find_word(context, board_tiles, user_tiles):
    page = await context.new_page()
    await page.goto('https://www.scrabulizer.com/')
    await page.wait_for_load_state("domcontentloaded")
    await page.locator('#staticDesignSelect').select_option('wordsWithFriends')
    await page.wait_for_timeout(300)
    await page.click('#s_0_0')
    for row in board_tiles:
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
                page.keyboard.type('Space')
            else:
                await page.keyboard.type(letter)

    async with page.expect_response(r'https://www.scrabulizer.com/solver/results') as response_info:
        await page.click('button.get-solutions')

    response = await response_info.value
    response_json = await response.json()
    return response_json['moves']

