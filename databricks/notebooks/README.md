# Databricks notebooks

Planned notebooks:

1. `01_bronze_ingest` — ingest raw input, attach batch/source metadata, and write Bronze Delta.
2. `02_silver_transform` — validate, standardize, deduplicate, and quarantine invalid rows.
3. `03_gold_model` — incrementally build dimensions and the sales fact.
4. `04_data_quality` — execute quality and reconciliation checks.

No executable notebooks are present yet. Add them as implementation progresses, with parameters and expected schemas documented.
