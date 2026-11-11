# Incremental loading and CDC patterns

This document explains the ideas behind incremental pipelines. The sample CSV and basic notebooks are educational batch examples; they are not a complete CDC implementation.

## Full versus incremental

A full load reads all available source records. It is simple but can become expensive. An incremental load reads only the changes since the last successful boundary (watermark), for example `updated_at > last_successful_watermark`.

## Safe watermark sequence

1. Read the last **successfully committed** watermark.
2. Capture an upper bound for this run, so the input range is fixed.
3. Read changes in `(previous_watermark, upper_bound]` (include a tie-breaker if timestamps can collide).
4. Validate and transform the batch.
5. Merge/publish idempotently using a stable business key and source change ordering.
6. Reconcile counts and quality checks.
7. Advance the watermark only after publish and validation succeed.

If a step fails before step 7, rerun the same bounded range. A batch ledger should record run ID, range, counts, status, and errors. Consider late-arriving updates and timestamp precision.

## CDC questions to answer with the source owner

- Are inserts, updates, and deletes provided?
- Is there a monotonically ordered version/LSN, or only an update timestamp?
- How are deletes represented and retained?
- Can events arrive late or out of order?
- What is the unique business key, and how are duplicate events resolved?
- How long can a batch be replayed?

## Delta merge concept

Delta Lake supports `MERGE INTO` to upsert changes by business key. Use a source sequence/version so an older event cannot overwrite a newer target row. Handle deletes explicitly. A simplified merge is not a full CDC solution without those rules, a reliable source feed, and tests.

## ADF orchestration concept

ADF can pass a batch ID and watermark range to a Databricks job, then update the control record only when all required stages complete. The actual control table, linked services, retries, and secure access must be implemented for the deployment; placeholders in this repository are not production credentials or configuration.
