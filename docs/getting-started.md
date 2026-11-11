# Beginner's guide: follow one sales row through the platform

Welcome! This guide explains what this project does and the order to learn it. You do not need an Azure account to understand the concepts or run the local contract test.

## 1. The simple idea

A business stores sales in files. A data engineer builds a repeatable process that copies those files, checks and cleans them, and organizes them so people can answer questions such as “Which products sold best last month?”

- **Pipeline:** connected steps that move and process data.
- **Orchestration:** deciding which step runs, when, and what happens on success/failure. ADF is used for this role.
- **Lake:** scalable file storage. ADLS Gen2 is the Azure storage service used here.
- **Transformation:** changing raw data into well-typed, useful records. Databricks and PySpark perform this role.
- **Warehouse:** structured tables designed for analytical queries. Synapse SQL is the planned serving layer.

## 2. Read the data

Open [`../data/sample/sales.csv`](../data/sample/sales.csv). It is tiny synthetic data, so you can inspect it safely. One row means one product line sold on an order. `order_id` can repeat when an order has multiple lines; `order_line_id` uniquely identifies a line. See the [data dictionary](data-dictionary.md) for all columns and rules.

## 3. Understand the four data zones

1. **Landing:** keep a copy of what arrived so you can trace or replay it.
2. **Bronze:** save source records with technical metadata such as file name, batch ID, and ingestion time. Avoid business interpretation at this stage.
3. **Silver:** parse dates and numbers, standardize text, detect invalid rows, and handle duplicates. Bad rows go to quarantine with a reason rather than disappearing.
4. **Gold:** arrange useful data into dimensions (descriptions) and facts (measures) for reporting.

These are logical layers; they do not have to be separate Azure accounts or databases.

## 4. Learn the star schema

A **fact** answers “what happened?” and stores measurable events. `fact_sales` stores quantity and sales amount at the order-line grain. **Dimensions** answer “by what?”: customer, product, store, and date. The star schema makes common reporting joins understandable.

## 5. Follow the files in order

1. `data/sample/sales.csv` — synthetic input.
2. `databricks/notebooks/01_bronze_ingest.py` — read source and retain metadata.
3. `databricks/notebooks/02_silver_transform.py` — validate and clean data.
4. `databricks/notebooks/03_gold_dimensional_model.py` — build the star-schema tables.
5. `databricks/notebooks/04_data_quality_checks.py` — fail a run when key checks fail.
6. `synapse/ddl/01_create_retail_schema.sql` — warehouse table design.
7. `synapse/queries/` — sample questions answered with SQL.
8. `adf/pipelines/retail_master_pipeline.json` — orchestration template; it needs environment-specific linked services and deployment validation.

## 6. Run locally or in Azure

### No Azure yet

Install Python 3.10+, then run from the repository root:

```bash
python -m unittest discover -s tests -v
```

This validates the sample file only. The PySpark notebooks need Spark and Delta Lake; the Synapse SQL needs a Synapse SQL environment.

### Azure practice

Create a non-production resource group and configure ADLS Gen2, ADF, Databricks, and (optionally) Synapse. Follow the [deployment checklist](deployment-checklist.md) and [runbook](runbook.md). Replace all `<...>` placeholders, configure managed identity/RBAC, and validate JSON/SQL in your own Azure environment. Never put secrets in Git.

## 7. Incremental loads and CDC in simple terms

- A **full load** processes all source rows every run.
- An **incremental load** processes only rows newer than a saved watermark, such as a source update timestamp.
- **CDC (change data capture)** supplies inserted, updated, or deleted changes from a source system.
- **Idempotency** means a retry of the same batch does not create duplicates or corrupt results.

A safe incremental process records its batch/watermark, processes a bounded range, validates output, publishes successfully, and only then advances the watermark. For a real CDC source, define delete handling, late events, and replay behavior with the source owner. See [incremental design](incremental-loads.md).

## 8. Suggested beginner milestones

- [ ] Explain the fact grain and why order ID alone is not unique.
- [ ] Describe the difference between Bronze, Silver, and Gold.
- [ ] Run the local sample-data test.
- [ ] Trace one invalid record to quarantine.
- [ ] Explain how ADF orchestrates Databricks without doing all transformations itself.
- [ ] Explain one data-quality rule and one recovery path.
- [ ] Run a reporting query and explain its joins.
- [ ] Only after understanding the basics, experiment with incremental processing and performance tuning.

## Glossary

| Term | Short definition |
| --- | --- |
| ADF | Azure service for data movement and pipeline orchestration |
| ADLS Gen2 | Azure Data Lake Storage, used for scalable file/data storage |
| Databricks | Spark-based platform for data engineering and analytics |
| PySpark | Python API for distributed Spark data processing |
| Delta Lake | Table/storage format with transaction and merge capabilities on a data lake |
| Synapse | Azure analytics service; this project focuses on its SQL warehouse concepts |
| CDC | Source-provided capture of inserts, updates, and deletes |
| Watermark | Persisted boundary indicating how far a successful load has processed |
| SCD | Slowly changing dimension strategy for keeping descriptive history |
