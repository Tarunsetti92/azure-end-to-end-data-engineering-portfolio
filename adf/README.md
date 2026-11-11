# Azure Data Factory implementation notes

This directory holds practical ADF JSON examples for a retail data platform. The examples are intentionally structured to be reusable, parameterized, and aligned with Azure best practices.

## Example artifacts

- `pipelines/retail_master_pipeline.json` — master orchestration pipeline
- `datasets/raw_sales_dataset.json` — raw ingestion dataset
- `datasets/bronze_sales_dataset.json` — Bronze destination dataset

## Implementation principles

- Use parameterized pipelines for environment-specific paths and file paths.
- Prefer retries and failure handling over silent data loss.
- Add a separate orchestration layer for batch metadata and notifications.
- Use data quality gates and row counts before downstream processing.

## Data flow

1. Copy raw files from landing source to ADLS Gen2.
2. Trigger Databricks job(s) for Bronze processing.
3. Trigger Silver and Gold notebooks after successful completion.
4. Monitor run status and send alerting if validation fails.
