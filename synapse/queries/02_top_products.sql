-- Question: Which products generated the most revenue?
SELECT TOP (10)
    p.product_name,
    p.category,
    SUM(f.net_sales) AS total_sales,
    SUM(f.quantity) AS total_units
FROM retail.fact_sales AS f
JOIN retail.dim_product AS p ON p.product_key = f.product_key
GROUP BY p.product_name, p.category
ORDER BY total_sales DESC;
