from pyspark.sql import SparkSession, functions as F
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("Retail_Gold_Model").getOrCreate()

silver_path = "abfss://silver@<storage_account>.dfs.core.windows.net/sales/"
gold_path = "abfss://gold@<storage_account>.dfs.core.windows.net/"

sales_df = spark.read.format("delta").load(silver_path)

# Build dimensions

dim_customer = (
    sales_df.select(
        F.col("customer_id").alias("customer_key"),
        F.col("customer_name").alias("customer_name"),
        F.col("region").alias("region")
    )
    .dropDuplicates()
)

dim_product = (
    sales_df.select(
        F.col("product_id").alias("product_key"),
        F.col("product_name").alias("product_name"),
        F.col("category").alias("category")
    )
    .dropDuplicates()
)

dim_store = (
    sales_df.select(
        F.col("store_id").alias("store_key"),
        F.col("store_name").alias("store_name"),
        F.col("region").alias("region")
    )
    .dropDuplicates()
)

dim_date = (
    sales_df.select(F.to_date(F.col("order_date")).alias("date_key"))
    .distinct()
    .withColumn("year", F.year("date_key"))
    .withColumn("month", F.month("date_key"))
    .withColumn("day", F.dayofmonth("date_key"))
    .withColumn("month_name", F.date_format("date_key", "MMMM"))
)

fact_sales = (
    sales_df.select(
        F.col("order_id").alias("order_id"),
        F.col("customer_id").alias("customer_key"),
        F.col("product_id").alias("product_key"),
        F.col("store_id").alias("store_key"),
        F.to_date(F.col("order_date")).alias("date_key"),
        F.col("quantity").alias("quantity"),
        F.col("sales_amount").alias("sales_amount"),
        F.col("discount_pct").alias("discount_pct")
    )
)

# Write curated tables

dim_customer.write.mode("overwrite").format("delta").save(f"{gold_path}dim_customer")
dim_product.write.mode("overwrite").format("delta").save(f"{gold_path}dim_product")
dim_store.write.mode("overwrite").format("delta").save(f"{gold_path}dim_store")
dim_date.write.mode("overwrite").format("delta").save(f"{gold_path}dim_date")
fact_sales.write.mode("overwrite").format("delta").save(f"{gold_path}fact_sales")

print("Gold dimensional model created successfully.")
