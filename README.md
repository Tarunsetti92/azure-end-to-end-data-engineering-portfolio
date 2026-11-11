# Azure Retail Analytics — beginner-friendly data engineering portfolio

An educational, end-to-end project that follows retail sales data from CSV files to analytics-ready warehouse tables. It demonstrates the core ideas behind **Azure Data Factory (ADF), ADLS Gen2, Azure Databricks, PySpark, Delta Lake, Synapse SQL, incremental processing, data quality, and dimensional modeling**.

> **Status and honesty:** This repository contains learning-oriented templates and example code. It does not include deployed Azure resources, credentials, or verified cloud execution. Azure JSON artifacts use placeholders and must be configured and validated in your own subscription before deployment. Do not present cloud runs or performance results as completed unless you have actually run and measured them.

## Start here

If you are new to data engineering, follow [the beginner's guide](docs/getting-started.md) first. It explains the project in order, defines the key terms, and shows what can be practiced locally before Azure is set up.

## What the project does

1. A sales CSV arrives in a landing area.
2. ADF is the planned orchestrator: it copies/identifies input and starts the processing stages.
3. Databricks with PySpark reads the file and writes a raw Bronze Delta table.
4. Silver processing parses types, checks business rules, removes duplicate line records, and separates invalid records.
5. Gold processing creates a sales fact and date/customer/product/store dimensions.
6. Synapse SQL provides the warehouse schema and example analytical queries.

```text
Synthetic CSV -> ADF orchestration -> ADLS Gen2 landing
                                  -> Databricks / PySpark
                                     Bronze -> Silver + quarantine -> Gold
                                  -> Synapse warehouse -> reporting queries
```

This is a **batch** learning project. CDC and watermark concepts are explained and a Delta `MERGE` example is provided as a pattern; the starter pipeline does not claim to implement a source-system CDC feed.

## Layers in plain language

| Layer | What it means | Example in this project |
| --- | --- | --- |
| Source / landing | Original input, kept for traceability | `data/sample/sales.csv` locally; landing container in Azure |
| Bronze | Raw copy plus ingestion metadata | Preserve source values and add batch/file metadata |
| Silver | Clean, typed, checked records | Valid sales lines and a separate quarantine output |
| Gold | Business-ready tables | Fact sales joined to descriptive dimensions |
| Warehouse | SQL-serving layer for analysis | Synapse DDL and reporting queries |

## Skills shown

- **ADF:** orchestration concepts, pipeline JSON template, parameters and dependencies.
- **ADLS Gen2:** landing and medallion storage layout.
- **Databricks / PySpark / Spark SQL:** staged transformations and Delta tables.
- **Data warehousing:** declared fact grain, dimensions, star schema, and analytical SQL.
- **ETL/ELT:** ingestion, transformations, validation, and curated publishing.
- **Incremental processing:** batch IDs, watermarks, idempotency, and a Delta merge pattern in the docs.
- **Reliability:** quarantine, validation gates, run metadata, and troubleshooting notes.
- **Performance:** tuning guidance based on measuring Spark and Synapse workloads, not unsupported claims.

## Repository map

```text
adf/                         ADF pipeline template and setup notes
 data/sample/sales.csv       Tiny synthetic input for learning
 databricks/notebooks/       Bronze -> Silver -> Gold -> quality examples
 docs/                       Beginner guide, design, data dictionary, operations
 synapse/ddl/                 Warehouse table definitions
 synapse/queries/             Reporting SQL examples
 tests/                       Lightweight data-contract tests
```

## Quick start

### Learn the design without Azure

- Read [`docs/getting-started.md`](docs/getting-started.md).
- Inspect the synthetic input and the [data dictionary](docs/data-dictionary.md).
- Read the notebooks in numeric order. Their storage paths are placeholders until configured in Databricks.

### Run the PySpark examples

These notebooks require a Spark environment with Delta Lake support (for example, Azure Databricks). Configure the notebook parameters and storage access for your workspace as described in the getting-started guide. Do not paste storage keys into code.

### Run the basic local test

Python 3.10+:

```bash
python -m unittest discover -s tests -v
```

The local test checks the sample CSV contract; it does not run Spark or connect to Azure.

## Important modeling decision

The fact grain is **one row per order line**, identified by `order_line_id` (not one row per order). This allows an order to contain multiple products. Gold dimensions use SHA-256 business-key hashes as stable example surrogate keys; date uses integer `YYYYMMDD`. These choices are educational and should be reviewed against the target warehouse's governance and key-management standards.

## Security and cost

Use managed identity or a secret manager for Azure access. Never commit secrets, customer data, access tokens, or production endpoints. Azure services can incur charges; use a development subscription, small workloads, budgets/alerts, and delete or pause resources when finished. See [the runbook](docs/runbook.md).

## Reference

The learning concept is inspired by the end-to-end Azure data engineering tutorial at [YouTube](https://www.youtube.com/watch?v=6_hXeNg9TJ0). This repository is an independent educational implementation and does not include the tutorial's original code.

## License

MIT. See [`LICENSE`](LICENSE).
