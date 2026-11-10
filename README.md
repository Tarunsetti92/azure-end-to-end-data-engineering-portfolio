# Azure Retail Analytics Data Platform

A portfolio project demonstrating an end-to-end Azure data engineering and warehousing solution for retail analytics. It is designed around **Azure Data Factory (ADF), Azure Data Lake Storage Gen2 (ADLS Gen2), Azure Databricks, PySpark, Delta Lake, and Azure Synapse Analytics**.

> **Project status:** Initial repository scaffold. Implementation artifacts will be added iteratively. This repository does not claim that Azure resources have been deployed or workloads executed.

## Business scenario

Retail data arrives from operational systems as periodic files and change events. Analytics teams need a dependable way to ingest new data, validate and transform it, preserve history where required, and publish consistent dimensional data for reporting.

This project will build a medallion-style lakehouse-to-warehouse pipeline for sales analytics, with reusable orchestration, incremental processing, data-quality checks, and a star-schema serving layer.

## Architecture

```text
Source files / change feeds
          |
          v
Azure Data Factory ---- schedules, parameters, retries, monitoring
          |
          v
ADLS Gen2 landing -> Bronze Delta -> Silver Delta -> Gold dimensional model
                         Azure Databricks / PySpark / Spark SQL
                                                   |
                                                   v
                                      Azure Synapse Analytics
                                      SQL warehouse / reporting
```

### Data layers

- **Landing:** Immutable source extracts and ingestion metadata.
- **Bronze:** Raw, replayable data with source and ingestion audit columns.
- **Silver:** Validated, deduplicated, conformed data with explicit types and rejected-record handling.
- **Gold:** Business-ready facts and dimensions, published for warehouse queries.

## Planned warehouse model

The initial analytical model is a retail sales star schema:

- `fact_sales` — sales transaction grain, quantity, unit price, discount, and sales amount.
- `dim_date` — calendar attributes for reporting periods.
- `dim_customer` — customer profile and history.
- `dim_product` — product, category, and subcategory.
- `dim_store` — store and geographic attributes.

The model will document its grain, keys, and history strategy. Slowly changing dimensions (including a Type 2 example) and surrogate-key assignment are planned implementation topics.

## Skills demonstrated

| Area | Planned implementation |
| --- | --- |
| Azure Data Factory | Parameterized orchestration, metadata-driven ingestion, dependency handling, retries, and monitoring |
| ADLS Gen2 | Landing and medallion storage layout, partitioning conventions, and access guidance |
| Azure Databricks | Notebooks/jobs, PySpark and Spark SQL transformations, Delta Lake, and performance considerations |
| Data integration | Full and incremental load patterns, watermarks, idempotency, and CDC concepts |
| Data quality | Schema checks, required-field rules, duplicate checks, reconciliation, and quarantine patterns |
| Data warehousing | Dimensional modeling, star schema, facts/dimensions, surrogate keys, and SCD strategy |
| Synapse Analytics | Warehouse DDL, load patterns, distribution/indexing considerations, and analytical SQL |
| Engineering practices | Configuration separation, observability, testing, documentation, and secure secret handling |

## Repository structure

```text
.
├── README.md
├── adf/                    # ADF pipeline, dataset, linked-service templates
├── databricks/
│   ├── jobs/               # Job configuration examples
│   └── notebooks/          # Bronze, silver, gold, and quality notebooks
├── docs/                   # Architecture, data dictionary, operations/runbook
├── infra/                  # Optional infrastructure-as-code and deployment guidance
├── synapse/
│   ├── ddl/                # Schemas, dimensions, and fact-table DDL
│   └── queries/             # Demonstration analytical and tuning queries
├── src/                    # Shared Python utilities, if needed
└── tests/                  # Transformation and data-quality tests
```

See the README in each subdirectory for its purpose and contribution notes.

## Getting started

This scaffold contains design documentation only; executable pipelines and cloud resources are not yet included. The planned local development path is:

1. Review [the architecture](docs/architecture.md) and [the implementation roadmap](docs/roadmap.md).
2. Add small, synthetic sample datasets (never commit credentials or personal data).
3. Implement and test transformations locally where practical, then deploy notebooks to a development Databricks workspace.
4. Configure Azure resource names and secrets through workspace secret scopes, managed identities, or deployment variables—not source files.
5. Deploy ADF and Synapse artifacts into a non-production environment and validate pipeline runs before publishing results.

Required Azure services and estimated cost depend on the chosen region, SKU, and usage. Tear down or pause development resources when they are not in use.

## Reliability and design principles

- Make ingestion repeatable and transformations idempotent.
- Track batch/run identifiers, source file, ingestion time, and record counts.
- Use watermarks or source change tracking for incremental processing; define late-arriving data behavior.
- Quarantine invalid rows with actionable reason codes instead of silently dropping them.
- Validate schema and business rules before publishing gold data.
- Parameterize environments and avoid embedding credentials in notebooks, pipeline JSON, or SQL.
- Measure Spark and warehouse performance before tuning; document the workload and trade-offs.

## Security note

Do not commit Azure credentials, access keys, SAS tokens, service-principal secrets, production data, or sensitive identifiers. Use managed identity or a secret manager and provide only non-sensitive configuration examples in this repository.

## Roadmap

- [ ] Document source contracts, sample data, and business definitions.
- [ ] Add reusable ADF ingestion pipeline templates and parameter examples.
- [ ] Implement Bronze ingestion and audit metadata in Databricks.
- [ ] Implement Silver cleaning, deduplication, and quarantine handling.
- [ ] Build Gold dimensions/fact with incremental merge and an SCD example.
- [ ] Add data-quality and reconciliation tests.
- [ ] Add Synapse DDL, load examples, and analytical/tuning queries.
- [ ] Document deployment, monitoring, recovery, and cost controls.

## Reference

The project concept is inspired by the end-to-end Azure data engineering tutorial: [Azure End-To-End Data Engineering Project (Job Ready)](https://www.youtube.com/watch?v=6_hXeNg9TJ0). This repository is an independent portfolio scaffold, not a copy of the tutorial's source code.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE).
