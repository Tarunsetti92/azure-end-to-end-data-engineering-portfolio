from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("Retail_Silver_Transform").getOrCreate()

bronze_path = "abfss://bronze@<storage_account>.dfs.core.windows.net/sales/"
silver_path = "abfss://silver@<storage_account>.dfs.core.windows.net/sales/"

sales_df = spark.read.format("delta").load(bronze_path)

sales_df = (
    sales_df
    .withColumn("order_id", F.col("order_id").cast("string"))
    .withColumn("customer_id", F.col("customer_id").cast("int"))
    .withColumn("product_id", F.col("product_id").cast("int"))
    .withColumn("store_id", F.col("store_id").cast("int"))
    .withColumn("quantity", F.col("quantity").cast("int"))
    .withColumn("unit_price", F.col("unit_price").cast("double"))
    .withColumn("discount_pct", F.coalesce(F.col("discount_pct").cast("double"), F.lit(0.0)))
    .withColumn("order_date", F.to_date(F.col("order_date"), "yyyy-MM-dd"))
    .withColumn("customer_name", F.trim(F.col("customer_name")))
    .withColumn("product_name", F.trim(F.col("product_name")))
    .withColumn("region", F.upper(F.trim(F.col("region"))))
    .withColumn("sales_amount", F.round(F.col("quantity") * F.col("unit_price") * (1 - F.col("discount_pct")), 2))
    .withColumn("is_valid_record", F.when(
        (F.col("order_id").isNotNull()) &
        (F.col("customer_id").isNotNull()) &
        (F.col("product_id").isNotNull()) &
        (F.col("store_id").isNotNull()) &
        (F.col("order_date").isNotNull()),
        F.lit(True)
    ).otherwise(F.lit(False)))
)

valid_df = sales_df.filter(F.col("is_valid_record") == True)
invalid_df = sales_df.filter(F.col("is_valid_record") == False)

valid_df.write.mode("overwrite").format("delta").save(silver_path)
invalid_df.write.mode("overwrite").format("delta").save(silver_path + "_quarantine")

print(f"Silver layer complete: valid_rows={valid_df.count()}, invalid_rows={invalid_df.count()}")
