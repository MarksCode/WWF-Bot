from typing import Callable

from playwright.async_api import async_playwright, Page
import asyncio


async def launch_playwright(url):
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=False)
    page = await browser.new_page()
    await page.goto(url)
    await page.wait_for_load_state("domcontentloaded")

    def cleanup_fn():
        asyncio.run(cleanup(p, browser))
    return [page, cleanup_fn]


async def cleanup(p, browser):
    p.stop()
    await browser.close()
