CREATE OR REPLACE VIEW
`fourth-truck-506708-s5.ecommerce_analytics.v_status_analytics`
AS

SELECT
    order_status,

    COUNT(*) AS order_count,

    SUM(quantity) AS total_quantity,

    ROUND(SUM(gross_amount), 2) AS gross_sales,

    ROUND(SUM(gross_amount - net_amount), 2) AS total_discount,

    ROUND(SUM(net_amount), 2) AS net_sales,

    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (),
        2
    ) AS order_percentage,

    ROUND(
        SUM(net_amount) * 100.0 /
        SUM(SUM(net_amount)) OVER (),
        2
    ) AS sales_percentage

FROM
    `fourth-truck-506708-s5.ecommerce_analytics.fact_orders`

GROUP BY
    order_status

ORDER BY
    net_sales DESC;