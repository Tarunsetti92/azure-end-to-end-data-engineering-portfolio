-- Question: What are sales and units by store region?
SELECT
    s.region,
    SUM(f.net_sales) AS total_sales,
    SUM(f.quantity) AS total_units,
    COUNT(DISTINCT f.order_id) AS order_count
FROM retail.fact_sales AS f
JOIN retail.dim_store AS s ON s.store_key = f.store_key
GROUP BY s.region
ORDER BY total_sales DESC;
