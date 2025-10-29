from decimal import Decimal
from playwright.sync_api import Page, Locator, expect
from typing import Optional

from pages import BasePage


class ProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.pagination_block = self.page.locator(".MuiPagination-ul")
        self.prev_button = page.get_by_role("button", name="Prev", exact=True)
        self.next_button = page.get_by_role("button", name="Next", exact=True)

    def element_operable(self, element: Locator) -> bool:
        if not element.is_visible():
            return False
        return not element.is_disabled()

    def _parse_rating(self, rating_locator: Locator) -> int:
        label = rating_locator.get_attribute('aria-label')
        return int(label.split(' ')[0])

    def _get_available_page_numbers(self) -> list[int]:
        page_numbers = []
        buttons = self.pagination_block.locator('.MuiPaginationItem-page').all()
        for button in buttons:
            button_text = button.text_content().strip()
            if button_text.isdigit():
                page_numbers.append(int(button_text))
        return page_numbers

    def get_active_page_number(self) -> int:
        return int(self.pagination_block.locator('[aria-current="page"]').text_content().strip())

    def get_first_page_number(self) -> int:
        return min(self._get_available_page_numbers())

    def get_last_page_number(self) -> int:
        return max(self._get_available_page_numbers())

    def navigate_to_catalog(self) -> None:
        self.open("product-listing-pagination")

    def navigate_to_next_page(self) -> bool:
        if self.element_operable(self.next_button):
            current_page = self.get_active_page_number()
            self.next_button.click()
            self.page.wait_for_load_state()
            expect(self.pagination_block.locator('[aria-current="page"]')).to_have_text(str(current_page + 1))
            return True
        return False

    def navigate_to_prev_page(self) -> bool:
        if self.element_operable(self.prev_button):
            current_page = self.get_active_page_number()
            self.prev_button.click()
            self.page.wait_for_load_state()
            expect(self.pagination_block.locator('[aria-current="page"]')).to_have_text(str(current_page - 1))
            return True
        return False

    def navigate_to_page_number(self, destination: int):
        page_btn = self.pagination_block.get_by_role("button", name=str(destination))
        if page_btn.is_visible():
            page_btn.click()
            self.page.wait_for_load_state()
            expect(self.pagination_block.locator('[aria-current="page"]')).to_have_text(str(destination))
            return True
        return False

    def collect_all_products(self) -> list[dict]:
        all_products = self.collect_products_from_page()
        while self.navigate_to_next_page():
            page_products = self.collect_products_from_page()
            all_products.extend(page_products)
        return all_products

    def collect_products_from_page(self) -> list[dict]:
        products = []
        cards: list[Locator] = self.page.locator(".MuiCardContent-root").all()
        page_number = self.get_active_page_number()
        for card in cards:
            products.append(self._parse_product(card, page_number))
        return products

    def collect_product_locators_from_page(self) -> list[Locator]:
        return self.page.locator(".MuiCardContent-root").all()

    def get_product_name(self, product_locator: Locator) -> str:
        return product_locator.locator("h6").first.text_content()

    def get_product_price(self, product_locator: Locator) -> str:
        return product_locator.locator("h6").nth(1).text_content().replace('Category: ', '').strip()

    def get_product_category(self, product_locator: Locator) -> str:
        return product_locator.locator("p").text_content()

    def get_product_star_locators(self, product_locator: Locator) -> list[Locator]:
        return product_locator.locator("xpath=.//svg[@class='MuiRating-icon']").all()

    def is_star_not_interactive(self, star: Locator) -> bool:
        return all([
            star.is_visible(),
            star.get_attribute("aria-hidden") == "true",
            star.get_attribute("focusable") in (None, "false"),
            star.get_attribute("role") is None,
            star.get_attribute("tabindex") is None
        ])



    def _parse_product(self, card: Locator, page_number: int) -> dict:
        product_dict = {
            'name': card.locator("h6").first.text_content().strip(),
            'category': card.locator("p").text_content().replace('Category: ', '').strip(),
            'price': Decimal(card.locator("h6").nth(1).text_content().replace('$', '')),
            'rating': self._parse_rating(card.locator('[aria-label*="Stars"]')),
            'page': page_number
        }
        return product_dict

    def find_product(self, desired_product: dict) -> Optional[dict]:
        while True:
            page_products = self.collect_products_from_page()
            for product in page_products:
                if desired_product["name"] == product["name"]:
                    return product
            if not self.navigate_to_next_page():
                break



