# Data dictionary and contracts

## Input: sales CSV

The canonical sample is [`../data/sample/sales.csv`](../data/sample/sales.csv). All identifiers are synthetic.

| Column | Type in Silver | Meaning / rule |
| --- | --- | --- |
| `order_id` | string | Order header identifier; can appear on multiple lines |
| `order_line_id` | string | Unique transaction-line identifier; required and used as fact grain |
| `order_date` | date | Date of sale; must parse as `yyyy-MM-dd` |
| `customer_id` | string | Source business key; required |
| `customer_name` | string | Customer display name; trim whitespace |
| `product_id` | string | Source business key; required |
| `product_name` | string | Product description; trim whitespace |
| `category` | string | Product category |
| `store_id` | string | Source business key; required |
| `store_name` | string | Store description |
| `region` | string | Store region; trimmed and normalized to uppercase |
| `quantity` | integer | Units sold; positive for this sample contract |
| `unit_price` | decimal | Per-unit price; non-negative |
| `discount_pct` | decimal | Fraction from 0 to 1; blank means zero |

`net_sales = quantity * unit_price * (1 - discount_pct)`, rounded to two decimal places. Currency is not specified in the sample and must be made explicit in a real project.

## Fact grain and keys

`fact_sales` has exactly one record per `order_line_id`. An order can contain multiple products and therefore multiple fact rows. Dimensions are customer, product, store, and date. The example creates SHA-256 hashes of source business keys as deterministic technical keys; hashing is a teaching choice, not a replacement for evaluating enterprise surrogate-key standards.

## Quality rules

- Required: order, line, date, customer, product, and store identifiers.
- Date must parse successfully.
- Quantity must be greater than zero; unit price must be non-negative.
- Discount must be between 0 and 1 inclusive.
- `order_line_id` must be unique within the processed dataset.
- Rejected records must be retained with a reason; do not drop them silently.

## Planned Gold tables

- `dim_date(date_key, full_date, year_no, quarter_no, month_no, month_name, day_no)`
- `dim_customer(customer_key, customer_id, customer_name)`
- `dim_product(product_key, product_id, product_name, category)`
- `dim_store(store_key, store_id, store_name, region)`
- `fact_sales(order_line_id, order_id, date_key, customer_key, product_key, store_key, quantity, unit_price, discount_pct, net_sales)`

A production extension should define SCD behavior (Type 1 overwrite or Type 2 history), unknown-member handling, currencies, late-arriving facts, and source deletion semantics.
