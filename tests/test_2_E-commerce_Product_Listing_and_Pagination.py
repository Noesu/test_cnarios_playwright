import allure
import pandas as pd
from pandas import DataFrame
from playwright.sync_api import Page
import time

from pages.Ecommerce_Product_Listing_and_Pagination import ProductsPage
from data.Ecommerce_Product_Listing_and_Pagination import desired_product, highest_rated_products, \
    most_expensive_products
from utils.allure import attach_screenshot, attach_html, attach_json


@allure.id("PLP_001")
@allure.severity("high")
@allure.tag("positive")
@allure.title("All displayed products have price within selected range")
def test_count_products(page: Page):
    expected_categories = 5
    expected_goods = 50

    with allure.step("Navigate to product listing page"):
        products_page = ProductsPage(page)
        products_page.navigate_to_catalog()
        attach_screenshot(page)

    with allure.step("Iterate through all pages and extract category for each product"):
        df = pd.DataFrame(products_page.collect_all_products())
        attach_html(df)
        assert not df.empty, "DataFrame is empty"
        assert 'category' in df.columns, "Column 'category' not found"

    with allure.step("Count products per category"):
        category_counts = df.groupby('category').size().reset_index(name='count')
        attach_html(category_counts, "Products per category")

    with allure.step("Compare counts with expected values from product data file"):
        assert (df['category'].nunique() == expected_categories), (f"Incorrect category count: "
                                                                   f"Expected: {expected_categories}, "
                                                                   f"Actual: {df['category'].nunique()}")
        assert (len(df) == expected_goods), (f"Incorrect product count: "
                                             f"Expected: {expected_goods}, "
                                             f"Actual: {len(df)}")


@allure.id("PLP_002")
@allure.severity("high")
@allure.tag("positive")
@allure.title("Find specific product and identify its page")
def test_find_product(page: Page):
    with allure.step("Navigate to product listing page"):
        products_page = ProductsPage(page)
        products_page.navigate_to_catalog()
        attach_screenshot(page)

    with allure.step("Iterate through pages until product is found and record the page number where product was found"):
        attach_json(desired_product, "desired product")
        founded_product = products_page.find_product(desired_product)
        attach_json(founded_product, "founded product")
        assert founded_product, f"Product: {desired_product['name']} not found"

    with allure.step("Verify product details match expected data"):
        assert founded_product['category'] == desired_product['category'], (
            f"Wrong category for {desired_product['name']}\n"
            f"Expected category: {desired_product['category']}, "
            f"Actual category: {founded_product['category']}")
        assert founded_product['price'] == desired_product['price'], (
            f"Wrong price for {desired_product['name']}\n"
            f"Expected price: {desired_product['price']}, "
            f"Actual price: {founded_product['price']}")
        assert founded_product['rating'] == desired_product['rating'], (
            f"Wrong rating for {desired_product['name']}\n"
            f"Expected rating: {desired_product['rating']}, "
            f"Actual rating: {founded_product['rating']}")


@allure.id("PLP_003")
@allure.severity("medium")
@allure.tag("positive")
@allure.title("Find highest-rated product in each category")
def test_find_highest_rated_products(page: Page):
    with allure.step("Navigate through all product pages and group products by category"):
        products_page = ProductsPage(page)
        products_page.navigate_to_catalog()
        df = pd.DataFrame(products_page.collect_all_products())
        assert not df.empty, "DataFrame is empty"

        attach_html(df.sort_values(['category', "rating"], ascending=[True, False]))

    with allure.step("Identify product(s) with maximum rating in each category"):
        max_ratings = df.groupby('category')['rating'].transform('max')
        most_rated = df[df['rating'] == max_ratings]
        attach_html(most_rated, "Highest-rated products")

    with allure.step("Verify ratings match expected data"):
        for index, row in most_rated.iterrows():
            category = row['category']
            product = row['name']
            assert product in highest_rated_products[category], (
                f"Product '{product}' does not have maximal rating in category '{category}'!"
            )


@allure.id("PLP_004")
@allure.severity("medium")
@allure.tag("positive")
@allure.title("Find most expensive product in each category")
def test_find_most_expensive_products(page: Page):
    with allure.step("Navigate through all product pages and group products by category"):
        products_page = ProductsPage(page)
        products_page.navigate_to_catalog()
        df = pd.DataFrame(products_page.collect_all_products())
        assert not df.empty, "DataFrame is empty"
        attach_html(df.sort_values(['category', 'price'], ascending=[True, False]))

    with allure.step("Identify product with highest price in each category"):
        idx = df.groupby('category')['price'].idxmax()
        most_expensive: DataFrame = df.loc[idx]
        attach_html(most_expensive, "Most expensive products")

    with allure.step("Verify price matches expected data"):
        for index, row in most_expensive.iterrows():
            category = row['category']
            product = row['name']
            assert product in most_expensive_products[category], (
                f"Product '{product}' is not most expensive in category '{category}'!"
            )


@allure.id("PLP_005")
@allure.severity("high")
@allure.tag("positive")
def test_pagination_controls(page: Page):
    test_page_number = 3

    with allure.step("Collect all products from catalog"):
        products_page = ProductsPage(page)
        products_page.navigate_to_catalog()
        df = pd.DataFrame(products_page.collect_all_products())
        attach_html(df, "all products")

    with allure.step(f"Navigate to page {test_page_number} and check active page number"):
        products_page.navigate_to_page_number(test_page_number)

        time.sleep(1)
        attach_screenshot(page)

        current_page_number = products_page.get_active_page_number()
        assert current_page_number == test_page_number, (
            f"Incorrect actual page number!\nExpected: {test_page_number}. Actual: {current_page_number}")

    with allure.step(f"Collect products from page {test_page_number}"):
        df3 = pd.DataFrame(products_page.collect_products_from_page())
        attach_html(df3, "page 3 products")
        merged = df.merge(df3, how='inner')                 # INNER JOIN по совпадению ВСЕХ столбцов объектов DataFrame
        assert len(merged) == len(df3), (                   # Проверка полного вхождения df3 в df
            f"Incorrect products on page {test_page_number}")

    with allure.step(f"Navigate to page {test_page_number + 1} using Next page button"):
        products_page.navigate_to_next_page()

        time.sleep(1)
        attach_screenshot(page)

        current_page_number = products_page.get_active_page_number()
        assert current_page_number == test_page_number + 1, (
            f"Incorrect actual page number!\nExpected: {test_page_number + 1}. Actual: {current_page_number}")

    with allure.step(f"Navigate to page {test_page_number} using Prev page button"):
        products_page.navigate_to_prev_page()

        time.sleep(1)
        attach_screenshot(page)

        current_page_number = products_page.get_active_page_number()
        assert current_page_number == test_page_number, (
            f"Incorrect actual page number!\nExpected: {test_page_number}. Actual: {current_page_number}")

    with allure.step(f"Navigate to first page using numeric button"):
        first_page_number = products_page.get_first_page_number()
        products_page.navigate_to_page_number(first_page_number)

        time.sleep(1)
        attach_screenshot(page)

        current_page_number = products_page.get_active_page_number()
        assert current_page_number == first_page_number, (
            f"Incorrect actual page number!\nExpected: {first_page_number}. Actual: {current_page_number}")

    with allure.step(f"Navigate to last page using numeric button"):
        last_page_number = products_page.get_last_page_number()
        products_page.navigate_to_page_number(last_page_number)

        time.sleep(1)
        attach_screenshot(page)

        current_page_number = products_page.get_active_page_number()
        assert current_page_number == last_page_number, (
            f"Incorrect actual page number!\nExpected: {last_page_number}. Actual: {current_page_number}")


@allure.id("PLP_006")
@allure.severity("medium")
@allure.tag("negative")
@allure.title("Ensure each product card displays name, price, category, and rating")
def test_all_product_cards(page: Page):
    products_page = ProductsPage(page)
    products_page.navigate_to_catalog()

    for page_number in range(1, products_page.get_last_page_number() + 1):
        with allure.step(f"Verify each card displays product name, price with currency, category text and rating stars"
                         f" are visible and read-only on page number {page_number}"):
            products_page.navigate_to_page_number(page_number)

            for product_locator in products_page.collect_product_locators_from_page():
                product_name = products_page.get_product_name(product_locator)

                with allure.step(f"Verifying {product_name}"):
                    assert product_name.strip(), "Name not displayed"

                    product_price = products_page.get_product_price(product_locator)
                    assert product_price.startswith("$"), "USD currency sign '$' is not shown in fron of price"

                    category = products_page.get_product_category(product_locator)
                    assert category.strip(), "Category not displayed"

                    product_stars = products_page.get_product_star_locators(product_locator)
                    for star in product_stars:
                        assert products_page.is_star_not_interactive(star), "Star is not visible or clickable"
