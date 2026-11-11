from pyspark.sql import functions as F

# Set this parameter to the Gold Delta root path.
dbutils.widgets.text("gold_path", "", "Gold Delta root path")
gold_path = dbutils.widgets.get("gold_path")
if not gold_path:
    raise ValueError("Set gold_path notebook parameter.")

fact = spark.read.format("delta").load(f"{gold_path.rstrip('/')}/fact_sales")
checks = {
    "fact has rows": fact.limit(1).count() > 0,
    "unique order line": fact.groupBy("order_line_id").count().filter(F.col("count") > 1).limit(1).count() == 0,
    "required keys populated": fact.filter(
        F.col("date_key").isNull() | F.col("customer_key").isNull() |
        F.col("product_key").isNull() | F.col("store_key").isNull()
    ).limit(1).count() == 0,
    "non-negative sales": fact.filter(F.col("net_sales") < 0).limit(1).count() == 0,
}

for name, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'}: {name}")
failed = [name for name, passed in checks.items() if not passed]
if failed:
    raise ValueError("Gold quality gate failed: " + ", ".join(failed))
print("All Gold checks passed.")
