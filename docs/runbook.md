# Operations runbook

## Expected stages

ADF orchestration -> Bronze ingest -> Silver validation -> Gold model -> quality gate -> optional Synapse publish.

## Before a run

- Confirm source file/schema and batch identity.
- Confirm target paths and available storage/compute.
- Confirm credentials are supplied through managed identity or approved secret storage.
- Ensure the batch has not already been published, or use the documented idempotent rerun strategy.

## On success

Record the ADF/Databricks run IDs, source files, input/valid/rejected counts, output tables, and watermark range. Check that the Gold fact row count matches accepted unique order lines.

## On failure

1. Identify the failed ADF activity or Databricks task and capture the run ID/error.
2. Do not advance the watermark or mark the batch complete.
3. Inspect source/schema errors and quarantine reason counts.
4. Fix the issue and rerun the same batch/range, not a new unbounded range.
5. Reconcile counts and check for duplicate keys before publishing.

## Common learning issues

- `abfss://` access fails: check filesystem/container name, identity role/ACLs, and workspace configuration. Do not fix it by committing an account key.
- Column not found: compare the input header with the [data contract](data-dictionary.md).
- Date parse failures: verify the source format is `yyyy-MM-dd`; invalid records should be quarantined.
- Duplicate line IDs: inspect source duplicates and the deterministic deduplication rule; do not assume `order_id` is unique.
- Synapse DDL errors: confirm the selected SQL pool/endpoint and its supported syntax before adapting scripts.

## Recovery and cleanup

Keep landing data immutable enough to replay. Remove or overwrite derived outputs only when the stage is designed for it and batch isolation is understood. Stop development compute and delete temporary cloud resources when the exercise ends.
