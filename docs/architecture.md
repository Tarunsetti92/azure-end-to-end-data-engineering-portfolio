# Architecture

## Component responsibilities

- **Azure Data Factory:** Parameterized orchestration, source-to-lake ingestion, dependency management, retries, and run-level monitoring.
- **ADLS Gen2:** Durable landing storage and Bronze/Silver/Gold data zones. Organize paths by source, entity, and ingestion date where appropriate.
- **Azure Databricks:** PySpark and Spark SQL transformations over Delta tables, data-quality enforcement, and dimensional model preparation.
- **Azure Synapse Analytics:** SQL warehouse tables and analytical access to curated Gold data.

## Data flow

1. ADF starts a batch and records its run identifier and configured watermark.
2. Source data is copied to an immutable or replayable landing location.
3. Databricks validates the input and writes raw records with ingestion metadata to Bronze.
4. Silver processing applies explicit schema, normalization, deduplication, and quarantine rules.
5. Gold processing builds dimensions and facts, applies incremental merge/history rules, and performs reconciliation.
6. Curated data is loaded or exposed in Synapse for analytical queries.
7. ADF and the compute jobs expose status, row counts, and failure context for operations.

## Cross-cutting requirements

- **Idempotency:** Reprocessing the same batch should not create duplicate business records.
- **Incremental processing:** Persist a source-appropriate watermark or change token; advance it only after successful publication.
- **Data quality:** Preserve rejected records and reason codes; fail publication on critical contract violations.
- **Observability:** Emit run/batch IDs, source and target counts, durations, and error summaries.
- **Security:** Prefer managed identity and secret scopes; keep secrets and real customer data out of Git.
- **Performance:** Choose Delta partitioning, Spark sizing, Synapse distribution, and indexing based on measured query patterns rather than defaults.

## Model

The planned star schema has `fact_sales` at the transaction-line grain, joined to date, customer, product, and store dimensions. Exact source keys, late-arriving dimension behavior, and SCD rules will be specified in the data dictionary before implementation.
