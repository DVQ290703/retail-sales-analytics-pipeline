# Project Inventory

This file separates required project files from optional learning-lab files.

## Required Core

These files are needed for the main local portfolio demo.

| Path | Keep? | Reason |
| --- | --- | --- |
| `src/pipeline.py` | Yes | Main batch ETL entrypoint |
| `src/extract.py` | Yes | Reads raw Excel data |
| `src/transform.py` | Yes | Cleans and standardizes retail data |
| `src/load.py` | Yes | Loads `staging_sales` into DuckDB |
| `src/build_dw.py` | Yes | Builds dimensional OLAP tables |
| `src/check_dw.py` | Yes | Simple warehouse table check |
| `src/analytics_report.py` | Yes | Creates report CSV outputs |
| `src/lakehouse_pipeline.py` | Yes | Local Bronze/Silver/Gold Parquet demo |
| `src/query_gold.py` | Yes | Queries Gold Parquet files with DuckDB |
| `dbt_duckdb/` | Yes | dbt analytics engineering demo |
| `sql/data_vault.sql` | Yes | Data Vault Hub/Link/Satellite SQL |
| `src/build_data_vault.py` | Yes | Executes Data Vault SQL |
| `docs/level1_coverage.md` | Yes | Explains checklist coverage |

## Optional Advanced

These files are useful for deeper Level 1 coverage, but the core project can run without them.

| Path | Keep? | Reason |
| --- | --- | --- |
| `src/spark_lakehouse.py` | Optional | Spark execution and partitioning demo |
| `src/spark_delta_lakehouse.py` | Optional | Delta Lake transaction-log demo |
| `src/cdc_simulator.py` | Optional | No-Docker CDC event generator |
| `src/streaming_features.py` | Optional | Checkpointed streaming feature demo |
| `docker-compose.yml` | Optional | Real-system lab orchestration |
| `docker/` | Optional | Postgres and Trino service config |
| `debezium/` | Optional | Debezium connector config |
| `scripts/register_debezium_connector.ps1` | Optional | Helper for Kafka Connect REST API |
| `src/load_oltp_postgres.py` | Optional | Loads data into Docker Postgres |
| `docs/real_system_runbook.md` | Optional | Real-system lab guide |
| `docs/cloud_storage_and_table_formats.md` | Optional | Lakehouse theory notes |
| `docs/kafka_debezium_notes.md` | Optional | Streaming/CDC theory notes |

## Low-Value or Removable

These are not harmful, but they are not essential.

| Path | Recommendation | Reason |
| --- | --- | --- |
| `requirements-dev.txt` | Keep if using tests/lint | Development-only dependencies |

## Generated Artifacts

These should stay ignored by Git.

```text
data/raw/
data/processed/
data/bronze/
data/silver/
data/gold/
data/spark_lakehouse/
data/delta_lakehouse/
data/cdc/
reports/output/
retail_dw.duckdb
```
