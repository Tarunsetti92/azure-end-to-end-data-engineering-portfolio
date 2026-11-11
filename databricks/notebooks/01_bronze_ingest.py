from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit, input_file_name

spark = SparkSession.builder.appName("Retail_Bronze_Ingest").getOrCreate()

source_path = spark.conf.get("spark.databricks.delta.source_path", "abfss://landing@<storage_account>.dfs.core.windows.net/sales/")
bronze_path = spark.conf.get("spark.databricks.delta.bronze_path", "abfss://bronze@<storage_account>.dfs.core.windows.net/sales/")

raw_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .option("mode", "FAILFAST")
    .csv(source_path)
)

raw_df = (
    raw_df
    .withColumn("source_file", input_file_name())
    .withColumn("ingested_at", current_timestamp())
    .withColumn("source_system", lit("retail_sales"))
)

raw_df.write.mode("append").format("delta").save(bronze_path)

print(f"Bronze ingest complete: rows={raw_df.count()}")
