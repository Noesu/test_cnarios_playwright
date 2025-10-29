# E-commerce Product Listing & Pagination

## Background

https://www.cnarios.com/challenges/product-listing-pagination#challenge

This challenge simulates an e-commerce storefront with multiple products displayed over several pages. Testers need to 
validate product data, pagination functionality, and filtering logic.

#### Objectives

- Navigate through paginated product listings
- Verify product counts by category
- Locate specific product across pages
- Identify highest-rated products in each category
- Find the most expensive product in each category

#### Requirements

- Automate navigation through all product pages
- Verify category-wise product counts match expected data
- Locate and highlight specific products
- Identify products by rating and price within each category
- Validate next/previous pagination buttons and number navigation

#### Acceptance Criteria

- Pagination works correctly with both number clicks and next/previous buttons
- Category-wise product counts are accurate
- Correct page number is identified for searched product
- Highest-rated and most expensive products are correctly identified in each category
- Automation follows best practices and uses proper waits

#### Hints

- Use loops to iterate through all pages when searching for a product
- Store product details in an array for category-wise analysis
- Use explicit waits for page content updates
- Consider dynamic selectors for products to avoid brittle locators

---

#### PLP_001	Count products in each category	 Counts match data source values

Verify total number of products in each category matches expected values

1. Navigate to product listing page
2. Iterate through all pages
3. Extract category for each product
4. Count products per category
5. Compare counts with expected values from product data file

---

#### PLP_002	Find specific product and identify its page	Product is found and correct page number is displayed

Locate a specific product in the listing and verify which page it is on

1. Navigate to product listing page
2. Iterate through pages until product is found
3. Verify product details match expected data
4. Record the page number where product was found

---

#### PLP_003	Find highest-rated product in each category	Highest-rated product is correctly identified in each category

Identify the highest-rated product within each category

1. Navigate through all product pages
2. Group products by category
3. Identify product(s) with maximum rating in each category
4. Verify ratings match expected data

---

#### PLP_004	Find most expensive product in each category	Most expensive product is correctly identified in each 
category

Identify the most expensive product in each category

1. Navigate through all product pages
2. Group products by category
3. Identify product with highest price in each category
4. Verify price matches expected data

---

#### PLP_005	Validate pagination controls	Products change according to the page clicked

Ensure pagination works correctly using next, previous, and page number clicks

1. Click page number 3 and verify products displayed belong to page 3
2. Click Next button and verify correct next page is loaded
3. Click Prev button and verify correct previous page is loaded
4. Navigate to first page using pagination
5. Navigate to last page using pagination

---

#### PLP_006	Verify product card details format	All product cards have complete details in correct format

Ensure each product card displays name, price, category, and rating

1. Navigate through all pages
2. Verify each card displays product name
3. Verify each card displays price with currency
4. Verify each card displays category text
5. Verify rating stars are visible and read-only