CREATE TABLE retail.dim_customer (
    customer_key INT NOT NULL,
    customer_name VARCHAR(200),
    region VARCHAR(100),
    CONSTRAINT PK_dim_customer PRIMARY KEY (customer_key)
);

CREATE TABLE retail.dim_product (
    product_key INT NOT NULL,
    product_name VARCHAR(200),
    category VARCHAR(100),
    CONSTRAINT PK_dim_product PRIMARY KEY (product_key)
);

CREATE TABLE retail.dim_store (
    store_key INT NOT NULL,
    store_name VARCHAR(200),
    region VARCHAR(100),
    CONSTRAINT PK_dim_store PRIMARY KEY (store_key)
);
