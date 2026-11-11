# Data dictionary

## Source data contract

The raw sales dataset is expected to contain at least these fields:

- `order_id`
- `order_date`
- `customer_id`
- `customer_name`
- `product_id`
- `product_name`
- `category`
- `store_id`
- `store_name`
- `region`
- `quantity`
- `unit_price`
- `discount_pct`

## Business rules

- `order_id` must be unique for the fact grain.
- `customer_id`, `product_id`, and `store_id` must be non-null in Silver and Gold layers.
- `order_date` must parse cleanly into a valid date.
- `sales_amount` should be `quantity * unit_price * (1 - discount_pct)` and should not be negative.
- Invalid/late or incomplete rows should be quarantined and reviewed.

## Warehouse grain

The gold `fact_sales` table is at the order-transaction grain. Each row represents a unique order or order line, as defined by the data contract and source system.

## Historical handling

Historical dimensions should use a surrogate-key pattern and, where needed, a Type 2 SCD strategy for explicit customer, product, or store history tracking.
