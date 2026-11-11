# Azure Databricks transformation notebooks

This directory contains the core lakehouse pipeline for business-ready retail datasets:

- 01_bronze_ingest.py: copy raw files into Bronze and attach ingestion metadata
- 02_silver_transform.py: normalize, validate, and deduplicate records
- 03_gold_dimensional_model.py: build gold dimensions and fact tables
- 04_data_quality_checks.py: enforce row and business-rule validation checks

The code is designed for Databricks Delta tables but can also be adapted to other Spark-enabled environments.
