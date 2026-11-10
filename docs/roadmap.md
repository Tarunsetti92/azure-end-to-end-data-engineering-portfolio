# Implementation roadmap

This roadmap keeps design, code, and validation explicit. Check items off only after the artifacts exist and have been validated.

1. **Contracts and data** — define source schemas, grain, business keys, synthetic fixtures, and expected quality rules.
2. **Landing and orchestration** — parameterize ADF ingestion, batch metadata, retries, and safe reruns.
3. **Bronze** — ingest source files with audit columns and schema evolution policy.
4. **Silver** — cast and standardize fields, deduplicate deterministically, validate records, and quarantine invalid rows.
5. **Gold** — implement dimensions, surrogate keys, a Type 2 history example, and the sales fact at a documented grain.
6. **Warehouse** — add Synapse DDL and a repeatable publish/load approach, plus representative analytical SQL.
7. **Quality and operations** — test counts and business rules; document monitoring, reruns, failure handling, and cost controls.

## Definition of done for a pipeline stage

- Input/output contract documented.
- Repeatable execution behavior and failure behavior documented.
- Tests or validation queries included.
- No secrets or real personal data committed.
- Operational metrics and recovery approach described.
