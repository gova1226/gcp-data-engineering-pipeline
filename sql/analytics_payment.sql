CREATE OR REPLACE VIEW
`fourth-truck-506708-s5.ecommerce_analytics.v_payment_analytics`
AS

SELECT
    payment_method,
    COUNT(*) AS order_count,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(gross_amount), 2) AS gross_sales,
    ROUND(SUM(discount), 2) AS total_discount,
    ROUND(SUM(net_amount), 2) AS net_sales,
    ROUND(AVG(net_amount), 2) AS average_order_value

FROM `fourth-truck-506708-s5.ecommerce_analytics.fact_orders`

GROUP BY payment_method
ORDER BY net_sales DESC;