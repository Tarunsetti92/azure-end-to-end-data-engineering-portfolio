CREATE TABLE retail.fact_sales (
    order_id VARCHAR(50) NOT NULL,
    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    store_key INT NOT NULL,
    date_key DATE NOT NULL,
    quantity INT NOT NULL,
    sales_amount DECIMAL(18,2) NOT NULL,
    discount_pct DECIMAL(10,4) DEFAULT 0,
    CONSTRAINT PK_fact_sales PRIMARY KEY (order_id)
)
WITH (
    DISTRIBUTION = HASH(order_id),
    CLUSTERED COLUMNSTORE INDEX
);

CREATE INDEX IX_fact_sales_date_key ON retail.fact_sales (date_key);
CREATE INDEX IX_fact_sales_customer_key ON retail.fact_sales (customer_key);
CREATE INDEX IX_fact_sales_product_key ON retail.fact_sales (product_key);
