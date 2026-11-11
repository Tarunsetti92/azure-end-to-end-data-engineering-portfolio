CREATE SCHEMA IF NOT EXISTS retail;

CREATE TABLE retail.dim_date (
    date_key DATE NOT NULL,
    year_no INT NOT NULL,
    month_no INT NOT NULL,
    day_no INT NOT NULL,
    month_name VARCHAR(20),
    CONSTRAINT PK_dim_date PRIMARY KEY (date_key)
);
