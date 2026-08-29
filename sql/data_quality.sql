-- ============================================================
-- DATA QUALITY CHECKS
-- ============================================================

-- Check 1: Null order IDs
SELECT
    'NULL_ORDER_ID' AS check_name,
    COUNT(*) AS failed_records
FROM `fourth-truck-506708-s5.ecommerce_clean.clean_orders`
WHERE order_id IS NULL

UNION ALL

-- Check 2: Null customer IDs
SELECT
    'NULL_CUSTOMER_ID' AS check_name,
    COUNT(*) AS failed_records
FROM `fourth-truck-506708-s5.ecommerce_clean.clean_orders`
WHERE customer_id IS NULL

UNION ALL

-- Check 3: Invalid quantity
SELECT
    'INVALID_QUANTITY' AS check_name,
    COUNT(*) AS failed_records
FROM `fourth-truck-506708-s5.ecommerce_clean.clean_orders`
WHERE quantity <= 0

UNION ALL

-- Check 4: Negative unit price
SELECT
    'NEGATIVE_UNIT_PRICE' AS check_name,
    COUNT(*) AS failed_records
FROM `fourth-truck-506708-s5.ecommerce_clean.clean_orders`
WHERE unit_price < 0

UNION ALL

-- Check 5: Duplicate order IDs
SELECT
    'DUPLICATE_ORDER_ID' AS check_name,
    COUNT(*) - COUNT(DISTINCT order_id) AS failed_records
FROM `fourth-truck-506708-s5.ecommerce_clean.clean_orders`

UNION ALL

-- Check 6: Invalid order status
SELECT
    'INVALID_ORDER_STATUS' AS check_name,
    COUNT(*) AS failed_records
FROM `fourth-truck-506708-s5.ecommerce_clean.clean_orders`
WHERE order_status NOT IN (
    'PLACED',
    'SHIPPED',
    'DELIVERED',
    'CANCELLED',
    'RETURNED'
);