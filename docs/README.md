# Architecture and design

This directory contains solution design documents. The platform is planned as an Azure lakehouse and warehouse pipeline: ADF orchestrates ingestion and Databricks workloads; ADLS Gen2 stores landing and medallion layers; Synapse serves curated dimensional data.

## Documents

- [Architecture](architecture.md) — component responsibilities and data flow.
- [Roadmap](roadmap.md) — implementation sequence and acceptance goals.
- `data-dictionary.md` — planned source contracts and warehouse definitions.
- `runbook.md` — planned operations, reruns, and troubleshooting guidance.

Designs are illustrative until the corresponding implementation is added and tested in Azure.
