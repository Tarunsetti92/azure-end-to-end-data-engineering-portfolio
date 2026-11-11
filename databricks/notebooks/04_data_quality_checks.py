from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("Retail_Data_Quality").getOrCreate()

gold_path = "abfss://gold@<storage_account>.dfs.core.windows.net/"

fact_sales = spark.read.format("delta").load(f"{gold_path}fact_sales")

duplicate_check = fact_sales.groupBy("order_id").count().filter(F.col("count") > 1)
null_customer = fact_sales.filter(F.col("customer_key").isNull()).count()
null_product = fact_sales.filter(F.col("product_key").isNull()).count()
null_store = fact_sales.filter(F.col("store_key").isNull()).count()
negative_sales = fact_sales.filter(F.col("sales_amount") < 0).count()

if duplicate_check.count() > 0:
    raise ValueError(f"Duplicate order IDs detected in fact_sales: {duplicate_check.count()}")

if null_customer > 0 or null_product > 0 or null_store > 0:
    raise ValueError(f"Critical dimension keys missing: customer={null_customer}, product={null_product}, store={null_store}")

if negative_sales > 0:
    raise ValueError(f"Negative sales detected: {negative_sales}")

print("Data quality checks passed.")
