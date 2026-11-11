from pyspark.sql import functions as F

# Paths are set by the job/ADF environment; use managed identity for storage access.
dbutils.widgets.text("silver_path", "", "Silver Delta path")
dbutils.widgets.text("gold_path", "", "Gold Delta root path")
silver_path = dbutils.widgets.get("silver_path")
gold_path = dbutils.widgets.get("gold_path")
if not silver_path or not gold_path:
    raise ValueError("Set silver_path and gold_path notebook parameters.")

sales = spark.read.format("delta").load(silver_path)

def stable_key(column_name):
    # Deterministic demo key derived from a natural key. Review enterprise key
    # standards before adopting hash keys in a real warehouse.
    return F.sha2(F.col(column_name).cast("string"), 256)

dim_customer = (
    sales.select("customer_id", "customer_name").dropDuplicates(["customer_id"])
    .withColumn("customer_key", stable_key("customer_id"))
    .select("customer_key", "customer_id", "customer_name")
)
dim_product = (
    sales.select("product_id", "product_name", "category").dropDuplicates(["product_id"])
    .withColumn("product_key", stable_key("product_id"))
    .select("product_key", "product_id", "product_name", "category")
)
dim_store = (
    sales.select("store_id", "store_name", "region").dropDuplicates(["store_id"])
    .withColumn("store_key", stable_key("store_id"))
    .select("store_key", "store_id", "store_name", "region")
)
dim_date = (
    sales.select(F.to_date("order_date").alias("full_date")).distinct()
    .withColumn("date_key", F.date_format("full_date", "yyyyMMdd").cast("int"))
    .withColumn("year_no", F.year("full_date"))
    .withColumn("quarter_no", F.quarter("full_date"))
    .withColumn("month_no", F.month("full_date"))
    .withColumn("month_name", F.date_format("full_date", "MMMM"))
    .withColumn("day_no", F.dayofmonth("full_date"))
)

facts = (
    sales.withColumn("date_key", F.date_format("order_date", "yyyyMMdd").cast("int"))
    .withColumn("customer_key", stable_key("customer_id"))
    .withColumn("product_key", stable_key("product_id"))
    .withColumn("store_key", stable_key("store_id"))
    .withColumn("net_sales", F.round(F.col("quantity") * F.col("unit_price") * (1 - F.col("discount_pct")), 2).cast("decimal(18,2)"))
    .select("order_line_id", "order_id", "date_key", "customer_key", "product_key", "store_key", "quantity", "unit_price", "discount_pct", "net_sales")
)

# Each write replaces this demo's complete output. For incremental production
# publishing, use Delta MERGE with a documented change key and delete policy.
for frame, name in [
    (dim_date, "dim_date"), (dim_customer, "dim_customer"),
    (dim_product, "dim_product"), (dim_store, "dim_store"), (facts, "fact_sales")
]:
    frame.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{gold_path.rstrip('/')}/{name}")

print("Gold star-schema tables written.")
