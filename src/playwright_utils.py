import os
from playwright.async_api import async_playwright

user_dirs = [
    os.path.join(os.getcwd(), 'tests\chromium_2'),
    os.path.join(os.getcwd(), 'tests\chromium'),
]


class PlaywrightManager:
    def __init__(self):
        self.browser = None
        self.p = None

    async def initialize(self):
        user_dir = user_dirs[0]
        p = await async_playwright().start()
        browser = await p.chromium.launch_persistent_context(
            user_dir,
            headless=False,
            # args=['--auto-open-devtools-for-tabs']
        )
        self.p = p
        self.browser = browser

    async def open_page(self, url):
        page = await self.browser.new_page()
        await page.goto(url, wait_until="domcontentloaded")
        await page.set_viewport_size({"width": 900, "height": 800})
        return page

