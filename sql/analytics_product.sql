CREATE OR REPLACE VIEW
`fourth-truck-506708-s5.ecommerce_analytics.v_product_analytics`
AS

SELECT
    product_id,

    COUNT(*) AS order_count,
    SUM(quantity) AS total_quantity,

    ROUND(SUM(gross_amount), 2) AS gross_sales,
    ROUND(SUM(discount), 2) AS total_discount,
    ROUND(SUM(net_amount), 2) AS net_sales,

    ROUND(
        SAFE_DIVIDE(SUM(net_amount), COUNT(*)),
        2
    ) AS average_order_value,

    ROUND(
        SAFE_DIVIDE(SUM(net_amount), SUM(quantity)),
        2
    ) AS revenue_per_unit

FROM
    `fourth-truck-506708-s5.ecommerce_analytics.fact_orders`

GROUP BY
    product_id;