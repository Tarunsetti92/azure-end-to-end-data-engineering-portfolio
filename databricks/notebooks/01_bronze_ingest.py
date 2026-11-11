# This sample file contains synthetic data only. Replace placeholders before using Azure.
# Configure storage paths with Databricks job parameters or widgets; never embed credentials.

from pyspark.sql import functions as F

# Databricks notebook parameters. ADF/job orchestration can pass these values.
dbutils.widgets.text("source_path", "", "Landing CSV path")
dbutils.widgets.text("bronze_path", "", "Bronze Delta path")
dbutils.widgets.text("batch_id", "manual-local-demo", "Batch/run ID")
source_path = dbutils.widgets.get("source_path")
bronze_path = dbutils.widgets.get("bronze_path")
batch_id = dbutils.widgets.get("batch_id")

if not source_path or not bronze_path:
    raise ValueError("Set source_path and bronze_path notebook parameters before running.")

# Read strings first: explicit parsing belongs in Silver, not schema inference.
source_df = (
    spark.read.option("header", True)
    .option("mode", "PERMISSIVE")
    .csv(source_path)
)

bronze_df = (
    source_df
    .withColumn("source_file", F.input_file_name())
    .withColumn("batch_id", F.lit(batch_id))
    .withColumn("ingested_at", F.current_timestamp())
)

# Append preserves the raw history. In a production rerun design, isolate batches
# and make retry behavior explicit (for example, replace only the same batch).
bronze_df.write.format("delta").mode("append").save(bronze_path)

print(f"Bronze write complete. batch_id={batch_id}")
