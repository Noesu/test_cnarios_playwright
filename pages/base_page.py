from playwright.sync_api import Page

from config import settings

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.page.set_default_timeout(3000)

    def open(self, url_suffix=""):
        self.page.goto(f"{settings.BASE_URL}{url_suffix}")


