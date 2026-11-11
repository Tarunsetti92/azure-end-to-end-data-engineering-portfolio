# Azure Retail Analytics Data Platform

A production-style Azure data engineering portfolio project designed to demonstrate hands-on experience with Azure Data Factory, ADLS Gen2, Databricks, PySpark, Spark SQL, Delta Lake, and Azure Synapse Analytics. This project follows a medallion architecture and a retail sales star schema to model a realistic enterprise analytics workflow.

## Business objective

Retail teams need trusted data for sales analysis, revenue monitoring, regional trends, customer insights, and product performance reporting. This project moves raw files from source systems into a governed lakehouse and then publishes a curated warehouse layer for BI and analytical workloads.

## Architecture overview

```text
Raw sources
  |
  v
Azure Data Factory (orchestration, scheduling, parameterization)
  |
  v
ADLS Gen2 Landing Zone
  |
  v
Bronze (raw + ingestion metadata)
  |
  v
Databricks / PySpark / Spark SQL
  -> Silver (clean + standardized + deduplicated)
  -> Gold (facts + dimensions)
  |
  v
Azure Synapse Analytics
  -> dim_date, dim_customer, dim_product, dim_store
  -> fact_sales
  |
  v
Power BI / downstream analytics
```

## Core cloud services

- Azure Data Factory (ADF)
- Azure Data Lake Storage Gen2 (ADLS Gen2)
- Azure Databricks
- PySpark and Spark SQL
- Delta Lake
- Azure Synapse Analytics
- SQL Server / T-SQL (for warehouse patterns and SQL tuning examples)

## Data model

### Fact table

- `fact_sales`
  - `order_id`
  - `customer_key`
  - `product_key`
  - `store_key`
  - `date_key`
  - `quantity`
  - `sales_amount`
  - `discount_amount`

### Dimension tables

- `dim_date`
- `dim_customer`
- `dim_product`
- `dim_store`

### Architecture pattern

This project is designed to follow a modern analytics pattern:

- Bronze: raw ingestion with minimal transformation
- Silver: cleaning, type correction, data quality validation, deduplication
- Gold: star schema publish-ready analytics tables

## Features implemented in this scaffold

- Parameterized ADF pipeline example
- Databricks Bronze/Silver/Gold notebook structure
- Gold layer dimensional modeling examples
- Synapse warehouse DDL and analytical queries
- Data quality validation patterns
- Incremental / watermark-based design for future CDC and ETL/ELT workflows

## Skills demonstrated

This repository is aligned to the following job requirements:

- Data Engineering
- Data Warehousing
- Azure Data Factory (ADF)
- Azure Databricks
- PySpark and Spark SQL
- Azure Synapse Analytics
- Star schema design / dimensional modeling
- Fact and Dimension modeling
- ETL/ELT patterns
- Incremental loads and CDC concepts
- ADLS Gen2 and Azure cloud data services
- SQL performance tuning and warehouse optimization

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── docs/
│   ├── architecture.md
│   ├── data-dictionary.md
│   └── roadmap.md
├── adf/
│   ├── README.md
│   ├── pipelines/
│   │   └── retail_master_pipeline.json
│   └── datasets/
│       ├── raw_sales_dataset.json
│       └── bronze_sales_dataset.json
├── databricks/
│   ├── README.md
│   ├── notebooks/
│   │   ├── 01_bronze_ingest.py
│   │   ├── 02_silver_transform.py
│   │   ├── 03_gold_dimensional_model.py
│   │   └── 04_data_quality_checks.py
│   └── jobs/
│       └── retail_pipeline_job.json
├── synapse/
│   ├── README.md
│   ├── ddl/
│   │   ├── 01_create_schema.sql
│   │   ├── 02_create_dimensions.sql
│   │   └── 03_create_fact_tables.sql
│   └── queries/
│       ├── 01_sales_by_region.sql
│       └── 02_top_products.sql
├── infra/
│   └── README.md
├── src/
│   └── README.md
├── tests/
│   └── README.md
└── LICENSE
```

## Project notes

This solution is intentionally scaffolded with realistic artifacts and patterns suitable for a professional portfolio. It is structured to show end-to-end thinking rather than just individual isolated scripts.

The repository focuses on design clarity, maintainability, and enterprise data-platform practices:

- robust data contracts
- explicit transformations in Databricks
- orchestrated workflow management in ADF
- analytical data model in Synapse
- operational visibility and data quality guardrails

## Next steps for full implementation

1. Create Azure resources in a dev/test subscription.
2. Configure ADLS Gen2 and mount points for Databricks.
3. Import or create the notebook code into Databricks.
4. Set up ADF pipeline parameters and linked services.
5. Load data into Synapse using a controlled load process.
6. Validate row counts, data quality, and downstream reports.

## Security and hygiene

- Do not commit secrets, access keys, or production connection strings.
- Use managed identity, RBAC, or Azure Key Vault where possible.
- Keep source data synthetic or de-identified.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
