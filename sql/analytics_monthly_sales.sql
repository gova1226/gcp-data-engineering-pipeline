CREATE OR REPLACE VIEW
`fourth-truck-506708-s5.ecommerce_analytics.v_monthly_sales`
AS

SELECT
    order_year,
    order_month,
    order_month_name,

    COUNT(*) AS order_count,
    SUM(quantity) AS total_quantity,

    ROUND(SUM(gross_amount), 2) AS gross_sales,
    ROUND(SUM(discount), 2) AS total_discount,
    ROUND(SUM(net_amount), 2) AS net_sales,

    ROUND(
        SAFE_DIVIDE(SUM(net_amount), COUNT(*)),
        2
    ) AS average_order_value

FROM
    `fourth-truck-506708-s5.ecommerce_analytics.fact_orders`

GROUP BY
    order_year,
    order_month,
    order_month_name

ORDER BY
    order_year,
    order_month;