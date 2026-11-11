# Architecture

## Purpose

Ingest synthetic retail sales records, preserve a traceable raw layer, clean and validate them, build a star schema, and expose SQL examples. This is a learning architecture, not a claim that Azure has been deployed.

## Components and responsibilities

- **ADF:** schedules and orchestrates copy and Databricks activities, passes non-secret parameters, handles dependency/retry behavior, and exposes pipeline run status.
- **ADLS Gen2:** stores landing files and Bronze/Silver/Gold Delta data. In production, use containers, RBAC, lifecycle policy, and environment separation appropriate to the organization.
- **Databricks:** uses Spark/PySpark and Delta to process the larger-than-memory workloads. Notebooks are numbered to make the flow easy to follow.
- **Synapse SQL:** holds a warehouse-oriented star schema and sample reporting queries. Loading/publishing into Synapse must be configured for the chosen Synapse deployment and is not automated by the starter ADF template.

## Flow

```text
CSV source
  -> ADF copy/orchestration
  -> ADLS landing
  -> Notebook 01: Bronze + run metadata
  -> Notebook 02: Silver validation + quarantine
  -> Notebook 03: Gold dimensions + fact
  -> Notebook 04: publish checks
  -> Synapse warehouse tables / SQL reporting
```

## Layer contracts

- **Landing:** original source file is retained; file path and arrival/batch identity are tracked.
- **Bronze:** source columns are retained with `source_file`, `batch_id`, and `ingested_at`. Do not silently overwrite prior batches.
- **Silver:** parseable and valid rows have explicit types. Invalid rows include a `reject_reason` and are stored separately. Duplicate order lines are resolved deterministically or rejected.
- **Gold:** one fact row per `order_line_id`; dimension references use stable demo hash keys, and `date_key` is `YYYYMMDD`.
- **Synapse:** warehouse table definitions reflect the Gold grain and key types. Distribution/index design is a workload-driven decision, not a universal rule.

## Reliability, monitoring, and security

Every production run should have a run/batch ID, start/end timestamps, input/output/reject counts, status, and actionable error detail. Retries must be idempotent. Validate data before advancing a watermark or publishing Gold. Use managed identity and least privilege; store secrets in a managed secret service. See the [runbook](runbook.md).

## Performance approach

First measure file sizes, Spark stage metrics, skew, shuffle, and query patterns. Avoid partitioning tiny datasets. In Synapse, compare distribution and storage choices with representative workloads. Record before/after metrics and test conditions; do not make unsupported performance claims.
