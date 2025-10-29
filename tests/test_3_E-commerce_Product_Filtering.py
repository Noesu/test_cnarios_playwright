import allure
import pandas as pd
from pandas import DataFrame
from playwright.sync_api import Page

from pages.Ecommerce_Product_Filtering import FilterPage
from utils.allure import attach_screenshot, attach_text, attach_html


@allure.id("PF_001")
@allure.severity("high")
@allure.tag("positive")
@allure.title("Displayed products belong only to the selected category")
def test_selecting_products_by_category(page: Page):
    test_category = "Electronics"

    with allure.step("Navigate to product listing page"):
        filter_page = FilterPage(page)
        filter_page.navigate_to_filter()
        attach_screenshot(page)

    with allure.step(f"Select category {test_category} from filter"):
        filter_page.filter_products_by_category(test_category)
        attach_screenshot(page)

    with allure.step(f"Verify all displayed products belong to {test_category}"):
        df: DataFrame = pd.DataFrame(filter_page.collect_products())
        assert not df.empty, "DataFrame is empty"
        attach_html(df, f"Filtered products from category {test_category}")
        all_match = df["category"].eq(test_category).all()
        assert all_match, f"Not all products belong to {test_category}"


@allure.id("PF_002")
@allure.severity("high")
@allure.tag("positive")
@allure.title("Filter products by price range")
def test_selecting_products_by_price_range(page: Page):
    price_range_from = 5000
    price_range_to = 50000

    with allure.step("Navigate to product listing page"):
        filter_page = FilterPage(page)
        filter_page.navigate_to_filter()
        attach_screenshot(page)

    with allure.step(f"Adjust price range slider from {price_range_from} to {price_range_to}"):
        filter_page.move_left_slider_to(price_range_from)
        filter_page.move_right_slider_to(price_range_to)
        attach_screenshot(page)
        left_slider_value, right_slider_value = filter_page.get_slider_values()
        assert (left_slider_value, right_slider_value) == (price_range_from, price_range_to), (
            f"Unexpected price range slider values.\n"
            f"Expected: left: {price_range_from}, right: {price_range_to}\n"
            f"Actual: left: {left_slider_value}, right: {right_slider_value}"
        )

    with allure.step("Verify all displayed products fall within selected price range"):
        df: DataFrame = pd.DataFrame(filter_page.collect_products())
        attach_html(df, f"Filtered products within price range: {price_range_from}-{price_range_to}")
        if df.empty:
            attach_text(f"No products found within price range {price_range_from}-{price_range_to}")
        else:
            all_match = df["price"].between(price_range_from, price_range_to).all()
            assert all_match, f"Some products fall outside price range {price_range_from}-{price_range_to}"


@allure.id("PF_003")
@allure.severity("medium")
@allure.tag("positive")
@allure.title("Filter products by minimum rating")
def test_selecting_products_by_rating(page: Page):
    test_rating = 4

    with allure.step("Navigate to product listing page"):
        filter_page = FilterPage(page)
        filter_page.navigate_to_filter()
        attach_screenshot(page)

    with allure.step("Set minimum rating filter to 4 stars"):
        filter_page.set_rating(test_rating)
        attach_screenshot(page)

    with allure.step(f"Verify all displayed products have rating >= {test_rating}"):
        df: DataFrame = pd.DataFrame(filter_page.collect_products())
        attach_html(df, f"Filtered products within rating range: {test_rating} and above")
        if df.empty:
            attach_text(f"No products found within price range: {test_rating} and above")
        else:
            all_match = df["rating"].ge(test_rating).all()
            assert all_match, f"Some products fall outside rating range: {test_rating} and above"

