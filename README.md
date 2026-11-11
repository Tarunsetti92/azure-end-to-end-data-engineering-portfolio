from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("Retail_Data_Quality").getOrCreate()

dbutils.widgets.text("gold_path", "", "Gold Delta root path")
gold_path = dbutils.widgets.get("gold_path")

if not gold_path:
    raise ValueError("Set gold_path notebook parameter before running the quality gate.")

fact_table_path = f"{gold_path.rstrip('/')}/fact_sales"
fact_sales = spark.read.format("delta").load(fact_table_path)

required_columns = {"order_line_id", "order_id", "date_key", "customer_key", "product_key", "store_key", "quantity", "net_sales"}
missing_columns = required_columns - set(fact_sales.columns)
if missing_columns:
    raise ValueError(f"Required fact columns are missing: {sorted(missing_columns)}")

checks = {
    "fact has rows": fact_sales.limit(1).count() > 0,
    "unique order line": fact_sales.groupBy("order_line_id").count().filter(F.col("count") > 1).limit(1).count() == 0,
    "required keys populated": fact_sales.filter(
        F.col("date_key").isNull() |
        F.col("customer_key").isNull() |
        F.col("product_key").isNull() |
        F.col("store_key").isNull()
    ).limit(1).count() == 0,
    "non-negative sales": fact_sales.filter(F.col("net_sales") < 0).limit(1).count() == 0,
    "positive quantity": fact_sales.filter(F.col("quantity") <= 0).limit(1).count() == 0,
}

for name, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'}: {name}")

failed_checks = [name for name, passed in checks.items() if not passed]
if failed_checks:
    raise ValueError("Gold quality checks failed: " + ", ".join(failed_checks))

print("All Gold quality checks passed successfully.")
