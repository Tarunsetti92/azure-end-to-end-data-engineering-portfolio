# Databricks notebooks

Run in order after configuring the notebook parameters and storage access:

1. `01_bronze_ingest.py` — source CSV to append-only Bronze Delta with batch metadata.
2. `02_silver_transform.py` — type conversion, validation, deterministic duplicate handling, and quarantine.
3. `03_gold_dimensional_model.py` — date/customer/product/store dimensions and order-line fact.
4. `04_data_quality_checks.py` — quality gate for Gold output.

The notebooks rely on Databricks-provided `spark` and `dbutils`. They are examples requiring workspace validation, not local Python scripts. Read [the beginner guide](../../docs/getting-started.md) and [runbook](../../docs/runbook.md) before running.
