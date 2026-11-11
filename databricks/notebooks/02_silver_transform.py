from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Supply paths through Databricks job parameters; no credentials belong in code.
dbutils.widgets.text("bronze_path", "", "Bronze Delta path")
dbutils.widgets.text("silver_path", "", "Silver Delta path")
dbutils.widgets.text("quarantine_path", "", "Quarantine Delta path")
bronze_path = dbutils.widgets.get("bronze_path")
silver_path = dbutils.widgets.get("silver_path")
quarantine_path = dbutils.widgets.get("quarantine_path")
if not all([bronze_path, silver_path, quarantine_path]):
    raise ValueError("Set bronze_path, silver_path, and quarantine_path parameters.")

raw = spark.read.format("delta").load(bronze_path)

# Explicit parsing and trimming make the output contract understandable.
clean = (
    raw.withColumn("order_id", F.trim("order_id"))
    .withColumn("order_line_id", F.trim("order_line_id"))
    .withColumn("order_date", F.to_date("order_date", "yyyy-MM-dd"))
    .withColumn("customer_id", F.trim("customer_id"))
    .withColumn("customer_name", F.trim("customer_name"))
    .withColumn("product_id", F.trim("product_id"))
    .withColumn("product_name", F.trim("product_name"))
    .withColumn("category", F.trim("category"))
    .withColumn("store_id", F.trim("store_id"))
    .withColumn("store_name", F.trim("store_name"))
    .withColumn("region", F.upper(F.trim("region")))
    .withColumn("quantity", F.col("quantity").cast("int"))
    .withColumn("unit_price", F.col("unit_price").cast("decimal(18,2)"))
    .withColumn("discount_pct", F.coalesce(F.col("discount_pct").cast("decimal(8,4)"), F.lit(0).cast("decimal(8,4)")))
)

reason = F.when(F.col("order_id").isNull() | (F.col("order_id") == ""), "missing_order_id")
reason = reason.when(F.col("order_line_id").isNull() | (F.col("order_line_id") == ""), "missing_order_line_id")
reason = reason.when(F.col("order_date").isNull(), "invalid_order_date")
reason = reason.when(F.col("customer_id").isNull() | (F.col("customer_id") == ""), "missing_customer_id")
reason = reason.when(F.col("product_id").isNull() | (F.col("product_id") == ""), "missing_product_id")
reason = reason.when(F.col("store_id").isNull() | (F.col("store_id") == ""), "missing_store_id")
reason = reason.when(F.col("quantity").isNull() | (F.col("quantity") <= 0), "invalid_quantity")
reason = reason.when(F.col("unit_price").isNull() | (F.col("unit_price") < 0), "invalid_unit_price")
reason = reason.when((F.col("discount_pct") < 0) | (F.col("discount_pct") > 1), "invalid_discount_pct")

clean = clean.withColumn("reject_reason", reason)

# Keep the latest ingested copy for a repeated line ID; production should use a
# source version/sequence where available instead of ingestion time.
window = Window.partitionBy("order_line_id").orderBy(F.col("ingested_at").desc_nulls_last())
ranked = clean.withColumn("_row_num", F.row_number().over(window))
ranked = ranked.withColumn(
    "reject_reason",
    F.when((F.col("_row_num") > 1) & F.col("reject_reason").isNull(), "duplicate_order_line_id")
     .otherwise(F.col("reject_reason"))
)

valid = ranked.filter(F.col("reject_reason").isNull()).drop("_row_num", "reject_reason")
rejected = ranked.filter(F.col("reject_reason").isNotNull()).drop("_row_num")

valid.write.format("delta").mode("overwrite").save(silver_path)
rejected.write.format("delta").mode("overwrite").save(quarantine_path)
print(f"Silver complete. valid={valid.count()}, rejected={rejected.count()}")
