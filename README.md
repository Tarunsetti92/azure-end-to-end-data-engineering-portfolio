# Azure Retail Analytics Data Engineering Portfolio

An end-to-end **batch data engineering portfolio project** that demonstrates how retail sales data can move from source files into analytics-ready warehouse tables using Azure data services.

The project is designed to showcase **Azure Data Factory (ADF), Azure Data Lake Storage Gen2 (ADLS Gen2), Azure Databricks, PySpark, Spark SQL, Delta Lake, and Azure Synapse Analytics**, along with data warehousing, dimensional modeling, data quality, and incremental-loading concepts.

> **Project status:** This repository contains learning-oriented code, templates, synthetic sample data, and design documentation. It is not a deployed or cloud-validated production system. Configure and test Azure resources in your own development environment before using the templates. The current workflow is batch, not real-time streaming.

## Project goal

Build a maintainable pipeline that ingests retail sales data, preserves raw records, validates and transforms the data, and prepares it for analytical reporting. The example uses a **Bronze → Silver → Gold** lakehouse flow and a **star-schema** warehouse model.

## Architecture at a glance

```text
Synthetic retail CSV
        |
        v
Azure Data Factory (orchestration template)
        |
        v
ADLS Gen2 landing zone
        |
        v
Azure Databricks + PySpark + Delta Lake
        |-- Bronze: raw records and ingestion metadata
        |-- Silver: typed, standardized, validated records + quarantine
        |-- Gold: sales fact and descriptive dimensions
        |
        v
Azure Synapse Analytics (warehouse DDL and SQL examples)
        |
        v
Reporting and analytics
```

### Layers

| Layer | Purpose | Example in this repository |
| --- | --- | --- |
| Landing | Keep the arriving source data for traceability and replay | Synthetic sales CSV and documented Azure path pattern |
| Bronze | Preserve raw values and add technical ingestion metadata | `databricks/notebooks/01_bronze_ingest.py` |
| Silver | Parse, standardize, validate, deduplicate, and quarantine invalid rows | `databricks/notebooks/02_silver_transform.py` |
| Gold | Publish analytics-ready fact and dimension tables | `databricks/notebooks/03_gold_dimensional_model.py` |
| Warehouse | Provide SQL table definitions and reporting query examples | `synapse/ddl/` and `synapse/queries/` |

## Data warehouse model

The model is a retail sales **star schema**:

- `fact_sales` — one row per **order line**, with quantity, price, discount, and net sales.
- `dim_date` — calendar attributes for reporting by day, month, quarter, and year.
- `dim_customer` ��� customer identifiers and descriptive attributes.
- `dim_product` — product and category attributes.
- `dim_store` — store and region attributes.

An order can contain multiple products, so `order_id` alone is not the fact grain. The sample uses `order_line_id` to identify each transaction line. See [`docs/data-dictionary.md`](docs/data-dictionary.md) for field definitions and validation rules.

## What you can explore

- ADF pipeline orchestration concepts and Databricks activity sequencing.
- ADLS Gen2 landing and medallion-zone organization.
- PySpark transformations and Delta table patterns.
- Required-field and business-rule checks, with rejected rows retained in quarantine.
- Fact/dimension modeling and star-schema reporting queries.
- Batch IDs, idempotency, watermark concepts, and CDC considerations.
- Operational, security, and deployment guidance for a development environment.

## Repository structure

```text
.
├── README.md
├── adf/
│   ├── pipelines/              # ADF orchestration example/template
│   └── datasets/               # Dataset examples
├── data/sample/                # Small synthetic sales CSV
├── databricks/notebooks/       # Bronze, Silver, Gold, and quality stages
├── docs/                       # Beginner guide, design, data dictionary, runbook
├── synapse/
│   ├── ddl/                    # Warehouse schema and table definitions
│   └── queries/                # Reporting query examples
├── tests/                      # Local sample-data contract checks
├── infra/                      # Infrastructure guidance
└── LICENSE
```

## Getting started

### 1. Learn the flow

Start with [`docs/getting-started.md`](docs/getting-started.md), then review [`docs/architecture.md`](docs/architecture.md) and [`docs/data-dictionary.md`](docs/data-dictionary.md). The sample data is synthetic and safe for learning.

### 2. Run the local sample-data test

With Python 3.10 or later, from the repository root run:

```bash
python -m unittest discover -s tests -v
```

This test checks the sample CSV contract only. It does **not** run Spark or connect to Azure.

### 3. Explore the Databricks notebooks

Read the notebooks in order: Bronze ingestion, Silver transformation, Gold modeling, and data-quality checks. They use Databricks-provided Spark and `dbutils`; configure the required paths and storage permissions in a Databricks workspace before running them. Do not put credentials in notebook code.

### 4. Configure Azure only when ready

Use the [`docs/deployment-checklist.md`](docs/deployment-checklist.md) and [`docs/runbook.md`](docs/runbook.md). The ADF files are examples, not a complete deployable factory package: create and validate linked services, datasets, workspace paths, and environment-specific parameters in Azure Data Factory. Validate the Synapse SQL against the specific Synapse SQL endpoint you choose.

## Incremental loads and real-time scope

The current example is **batch-oriented**. The documentation explains watermark and CDC concepts, but a production incremental pipeline still needs a source-specific change feed or watermark, a control/batch ledger, tested idempotent merge logic, delete handling, and replay policies. Real-time streaming would require a separate streaming source and design; it is not implemented here.

## Security and cost

- Use managed identity and least-privilege access where available.
- Store secrets in an approved secret manager; never commit keys, tokens, connection strings, or private data.
- Use synthetic or anonymized data only.
- Azure resources can incur charges. Use a development subscription, set budget alerts, and stop or remove resources when finished.

## Skills demonstrated

Azure Data Factory · ADLS Gen2 · Azure Databricks · PySpark · Spark SQL · Delta Lake · Azure Synapse Analytics · ETL/ELT · Data quality · Incremental-load and CDC concepts · Star schema · Fact and dimension modeling · Data warehousing · SQL analytics

## Reference

The project concept is inspired by the [Azure end-to-end data engineering tutorial](https://www.youtube.com/watch?v=6_hXeNg9TJ0). This repository is an independent educational implementation and does not contain the tutorial's original code.

## License

This project is distributed under the MIT License. See [`LICENSE`](LICENSE).
