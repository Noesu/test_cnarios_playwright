# E-commerce Product Filtering & Search

## Background

https://www.cnarios.com/challenges/product-filtering

This challenge simulates an e-commerce storefront with various filtering options. Testers must validate that the filters
work independently and in combination, and that resetting filters restores the full product list.

#### Objectives

- Filter products by category
- Filter products by price range
- Filter products by minimum rating
- Show only in-stock products
- Reset filters and verify product list resets

#### Requirements

- Automate category-based filtering
- Automate price range slider filtering
- Automate rating filter selection
- Automate stock availability filter
- Verify reset functionality clears all filters

#### Acceptance Criteria

- All filters correctly update the displayed product list
- Filters work both individually and in combination
- Reset clears all filters and restores default product list
- Automation follows best practices with proper waits

#### Hints

- Use data attributes or accessible labels to select filter components
- Verify filter results match expected product data
- Test combinations of filters to ensure no conflicts
- Check that product counts update dynamically with filters applied

---

#### PF_001	Filter products by category	

Displayed products belong only to the selected category
Select a category and verify only products from that category are shown

1. Navigate to product listing page
2. Select category 'Electronics' from filter
3. Verify all displayed products belong to 'Electronics'

---

#### PF_002	Filter products by price range	

All displayed products have price within selected range	
Adjust price range slider and verify products displayed are within range

1. Navigate to product listing page
2. Adjust price range slider to ₹5,000 – ₹50,000
3. Verify all displayed products fall within selected price range

---

#### PF_003	Filter products by minimum rating	

All displayed products have rating greater than or equal to selected rating	
Select minimum rating and verify products meet or exceed that rating

1. Navigate to product listing page
2. Set minimum rating filter to 4 stars
3. Verify all displayed products have rating >= 4

---

#### PF_004	Show only in-stock products	

Only in-stock products are displayed
Enable 'In Stock Only' filter and verify out-of-stock items are hidden

1. Navigate to product listing page
2. Enable 'In Stock Only' filter
3. Verify all displayed products are in stock

---

#### PF_005	Reset filters

All filters are cleared and default product list is displayed	
Apply multiple filters, reset them, and verify the full product list is shown

1. Navigate to product listing page
2. Apply category, price, and stock filters
3. Click reset button
4. Verify all filters are cleared
5. Verify full default product list is restored

---

#### PF_006	Verify product card details format after filtering

All product cards display name, price, category, and rating in correct format	
Ensure that even after filtering, each product card shows complete details

1. Navigate to product listing page
2. Apply category filter
3. Verify each product card displays name
4. Verify price is shown with currency symbol
5. Verify category label is present
6. Verify rating stars are visible and read-only