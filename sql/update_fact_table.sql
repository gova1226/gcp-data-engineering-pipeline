-- ============================================================
-- CREATE / UPDATE ANALYTICS FACT TABLE
-- ============================================================

DROP TABLE IF EXISTS
`fourth-truck-506708-s5.ecommerce_analytics.fact_orders`;

CREATE TABLE
`fourth-truck-506708-s5.ecommerce_analytics.fact_orders`

PARTITION BY order_date

CLUSTER BY customer_id, product_id, order_status

AS

SELECT
    order_id,
    customer_id,

    -- Convert STRING order_date to DATE
    SAFE_CAST(order_date AS DATE) AS order_date,

    product_id,

    quantity,
    unit_price,
    discount,
    payment_method,
    order_status,
    country,

    gross_amount,
    net_amount,

    order_year,
    order_month,
    order_month_name,

    is_completed,
    is_cancelled,
    is_returned

FROM
`fourth-truck-506708-s5.ecommerce_clean.clean_orders`;