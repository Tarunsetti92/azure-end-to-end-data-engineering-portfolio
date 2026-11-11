-- Learning-oriented dedicated SQL pool example. Validate supported syntax/SKU before use.
CREATE SCHEMA retail;
GO

CREATE TABLE retail.dim_date (
    date_key INT NOT NULL,
    full_date DATE NOT NULL,
    year_no SMALLINT NOT NULL,
    quarter_no TINYINT NOT NULL,
    month_no TINYINT NOT NULL,
    month_name VARCHAR(12) NOT NULL,
    day_no TINYINT NOT NULL
)
WITH (DISTRIBUTION = REPLICATE, HEAP);
GO

CREATE TABLE retail.dim_customer (
    customer_key CHAR(64) NOT NULL,
    customer_id VARCHAR(40) NOT NULL,
    customer_name VARCHAR(200) NOT NULL
)
WITH (DISTRIBUTION = REPLICATE, HEAP);
GO

CREATE TABLE retail.dim_product (
    product_key CHAR(64) NOT NULL,
    product_id VARCHAR(40) NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(100)
)
WITH (DISTRIBUTION = REPLICATE, HEAP);
GO

CREATE TABLE retail.dim_store (
    store_key CHAR(64) NOT NULL,
    store_id VARCHAR(40) NOT NULL,
    store_name VARCHAR(200) NOT NULL,
    region VARCHAR(100)
)
WITH (DISTRIBUTION = REPLICATE, HEAP);
GO

CREATE TABLE retail.fact_sales (
    order_line_id VARCHAR(50) NOT NULL,
    order_id VARCHAR(50) NOT NULL,
    date_key INT NOT NULL,
    customer_key CHAR(64) NOT NULL,
    product_key CHAR(64) NOT NULL,
    store_key CHAR(64) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(18,2) NOT NULL,
    discount_pct DECIMAL(8,4) NOT NULL,
    net_sales DECIMAL(18,2) NOT NULL
)
WITH (DISTRIBUTION = HASH(order_line_id), CLUSTERED COLUMNSTORE INDEX);
GO

-- Synapse dedicated SQL pool constraints may be informational. Validate data
-- quality and referential integrity in pipeline checks as well.
