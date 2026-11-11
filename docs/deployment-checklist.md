# Deployment checklist (development only)

This is a learning checklist, not a one-click deployment. Azure resources may incur charges. Use a dedicated development subscription/resource group, set budget alerts, and clean up when finished.

## Before creating resources

- [ ] Confirm subscription access, region, naming rules, and cost limits.
- [ ] Choose whether Synapse is needed for the learning milestone; its dedicated SQL pool can incur significant cost while active.
- [ ] Review the data contract and use synthetic data only.
- [ ] Keep credentials and environment-specific values out of Git.

## Configure Azure services

- [ ] Create ADLS Gen2 with hierarchical namespace enabled; create landing/bronze/silver/gold filesystems or agreed directory layout.
- [ ] Create ADF and configure a managed identity.
- [ ] Create/configure Databricks and secure storage access using managed identity/access connector or approved secret management.
- [ ] Grant least-privilege RBAC/ACLs to the required identities; verify access without embedding account keys.
- [ ] If using Synapse, configure workspace/network/access controls and an appropriate SQL pool or serverless option for the exercise.

## Import and validate

- [ ] Replace `<...>` placeholders in templates with non-secret environment values.
- [ ] Create and test ADF linked services and datasets in the ADF authoring experience.
- [ ] Validate ADF pipeline JSON against the target service; the repository pipeline is a template, not a ready-to-import ARM deployment package.
- [ ] Install/run notebooks in sequence and verify expected output schemas and counts.
- [ ] Run Synapse DDL and queries in the selected SQL environment; adjust syntax and distribution options for that target.
- [ ] Test retries, reruns, invalid input, and empty input before scheduling.
- [ ] Record real results and screenshots only after successful runs; remove account IDs and sensitive details from screenshots.

## Finish safely

- [ ] Stop/delete paid compute and pools when not in use.
- [ ] Remove temporary data and credentials according to your security policy.
- [ ] Update docs with the date, configuration scope, and genuinely observed results.
