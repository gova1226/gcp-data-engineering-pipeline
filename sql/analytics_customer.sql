CREATE OR REPLACE VIEW
`fourth-truck-506708-s5.ecommerce_analytics.v_customer_analytics`
AS

SELECT
    customer_id,

    COUNT(*) AS order_count,
    SUM(quantity) AS total_quantity,

    ROUND(SUM(gross_amount), 2) AS gross_spend,
    ROUND(SUM(discount), 2) AS total_discount,
    ROUND(SUM(net_amount), 2) AS total_spend,

    ROUND(
        SAFE_DIVIDE(SUM(net_amount), COUNT(*)),
        2
    ) AS average_order_value,

    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date

FROM
    `fourth-truck-506708-s5.ecommerce_analytics.fact_orders`

GROUP BY
    customer_id;