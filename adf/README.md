# ADF artifacts

This directory is reserved for Azure Data Factory templates and examples, organized by artifact type (for example `pipelines/`, `datasets/`, `linkedServices/`, and `triggers/`). Add exported or source-controlled JSON only after validating it against the target ADF schema.

Use parameterized environment settings and managed identity where supported. Do not commit credentials, account keys, SAS tokens, or production endpoints. The initial pipeline design is described in the root [README](../README.md) and [architecture document](../docs/architecture.md).
