from decimal import Decimal
from playwright.sync_api import Page, Locator

from pages import BasePage


class FilterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.category_filter = page.get_by_role("combobox", name="Category")
        self.filtered_products = page.locator("//div[contains(@class, 'MuiBox-root')]/div[contains(@class, 'border')]")
        self.category_list = page.get_by_role("listbox")
        self.slider_inputs = page.locator("input[type='range']")
        self.price_range_left_slider = page.locator(
            "//span[contains(@class, 'MuiSlider-root')]/span[contains(@class, 'MuiSlider-thumb')][1]")
        self.price_range_right_slider = page.locator(
            "//span[contains(@class, 'MuiSlider-root')]/span[contains(@class, 'MuiSlider-thumb')][2]")
        self.star_selector = page.locator(f'span.MuiRating-visuallyHidden')

    def navigate_to_filter(self):
        self.open("product-filtering")

    def filter_products_by_category(self, category_name: str) -> None:
        self.category_filter.click()
        self.category_list.get_by_role("option", name=category_name).click()
        self.page.wait_for_load_state()

    def collect_products(self):
        products = []
        cards: list[Locator] = self.filtered_products.all()
        for card in cards:
            products.append(self._parse_product(card))
        return products

    def _parse_product(self, card: Locator) -> dict:
        category, full_price, full_rating = card.locator("p").nth(1).text_content().split(" • ")
        rating = full_rating[-1]
        currency, price = full_price[0], Decimal(full_price[1:])
        product_dict = {
            'name': card.locator("p").first.text_content().strip(),
            'category': category,
            'currency': currency,
            'price': price,
            'rating': int(rating),
            'in_stock': card.locator("span").text_content().strip() == "In Stock"
        }
        return product_dict

    def move_left_slider_to(self, value: int):
        self._adjust_slider(self.price_range_left_slider, value, is_left=True)

    def move_right_slider_to(self, value: int):
        self._adjust_slider(self.price_range_right_slider, value, is_left=False)

    def _adjust_slider(self, slider_locator: Locator, value: int, is_left: bool) -> None:
        """Перемещает указанный ползунок (slider) слайдера на заданное значение."""
        page = slider_locator.page
        input_elem = (
            self.slider_inputs.first if is_left else self.slider_inputs.nth(1)
        )

        # Получаем min/max диапазона
        min_value = int(input_elem.get_attribute("min"))
        max_value = int(input_elem.get_attribute("max"))

        # Считываем текущее положение обоих ползунков
        left_value = int(self.slider_inputs.first.get_attribute("value"))
        right_value = int(self.slider_inputs.nth(1).get_attribute("value"))

        # Предотвращаем пересечение
        if is_left:
            if value >= right_value:
                value = right_value - 1000  # шаг зависит от step в HTML
        else:
            if value <= left_value:
                value = left_value + 1000

        # Ограничиваем значение в пределах min/max
        value = max(min(value, max_value), min_value)

        # Рассчитываем долю перемещения
        ratio = (value - min_value) / (max_value - min_value)

        # Берём родительский контейнер слайдера
        slider_track = slider_locator.locator("xpath=ancestor::span[contains(@class, 'MuiSlider-root')]")
        box = slider_track.bounding_box()
        if not box:
            raise ValueError("Не удалось определить координаты слайдера")

        # Вычисляем целевые координаты (по оси X, середина по Y)
        target_x = box["x"] + box["width"] * ratio
        target_y = box["y"] + box["height"] / 2

        # Двигаем ползунок
        slider_locator.hover()
        page.mouse.down()
        page.mouse.move(target_x, target_y, steps=5)
        page.mouse.up()

        self.page.wait_for_load_state()

    def get_slider_values(self) -> tuple[int, int]:
        left_slider_value = int(self.slider_inputs.first.get_attribute("value"))
        right_slider_value = int(self.slider_inputs.nth(1).get_attribute("value"))
        return left_slider_value, right_slider_value

    def set_rating(self, value: int):
        self.star_selector.nth(value * 2).click(force=True)