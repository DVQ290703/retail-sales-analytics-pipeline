# Level 1 Data Engineering Coverage

This document maps the project to the requested **Level 1 Data Engineering Core** checklist.

Status labels:

- **Covered**: implemented and runnable in the local core project.
- **Demo**: implemented as a simplified local learning demo.
- **Optional Lab**: implemented through Docker or heavier dependencies.
- **Not Implemented**: documented only, not built as a running component.

## Overall Verdict

The project is strong enough for a **Level 1 learning portfolio**.

It has:

- Batch ETL.
- DuckDB warehouse.
- Dimensional modeling.
- Data Vault demo.
- dbt project.
- Bronze/Silver/Gold lakehouse folders.
- Spark Parquet job.
- Delta Lake optional job.
- CDC and streaming feature demo.
- Optional Docker lab for Postgres, Kafka, Debezium, MinIO, and Trino.

It does **not** fully implement:

- A true HTAP database.
- Production Kafka exactly-once transactions.
- Real Iceberg or Hudi tables.
- Production cloud storage on AWS/GCP/Azure.

## 2. Data Modeling & Analytics Engineering

| Topic | Status | Project Artifact | Notes |
| --- | --- | --- | --- |
| 2.1 OLTP vs OLAP | Covered | `sql/oltp_schema.sql`, `docker/postgres/init/01_schema.sql`, `src/load.py`, `src/build_dw.py` | OLTP is modeled as normalized tables; OLAP is DuckDB staging + fact/dim tables |
| 2.1 HTAP | Not Implemented | Docs only | True HTAP needs an engine such as TiDB, SingleStore, or similar |
| 2.2 Dimensional Modeling | Covered | `src/build_dw.py`, `dbt_duckdb/models/marts/` | Builds `fact_sales` and dimension tables |
| 2.2 Data Vault | Demo | `sql/data_vault.sql`, `src/build_data_vault.py` | Builds Hub, Link, and Satellite tables from `staging_sales` |
| 2.3 dbt | Covered | `dbt_duckdb/dbt_project.yml`, `dbt_duckdb/models/` | Includes sources, staging, marts, and basic tests |

Recommended improvement:

- Move the handwritten warehouse SQL in `src/build_dw.py` fully into dbt models if you want a cleaner analytics-engineering story.

## 3. Modern Data Stack & Lakehouse Architecture

| Topic | Status | Project Artifact | Notes |
| --- | --- | --- | --- |
| 3.1 Cloud Storage Internals | Demo / Optional Lab | `data/bronze/`, `data/silver/`, `data/gold/`, MinIO in `docker-compose.yml` | Local folders mimic object prefixes; MinIO provides S3-compatible local storage |
| 3.2 Delta Lake | Optional Lab | `src/spark_delta_lakehouse.py` | Creates Delta tables with `_delta_log` when Delta dependencies are installed |
| 3.2 Iceberg | Not Implemented | `docs/cloud_storage_and_table_formats.md` | Explained only |
| 3.2 Hudi | Not Implemented | `docs/cloud_storage_and_table_formats.md` | Explained only |
| 3.3 Spark Execution Model | Demo | `src/spark_lakehouse.py`, `src/spark_delta_lakehouse.py` | Uses partitioning, repartitioning, and adaptive execution config |
| 3.4 DuckDB | Covered | `src/query_gold.py`, `src/analytics_report.py` | Queries DuckDB tables and Parquet files |
| 3.4 Trino | Optional Lab | `docker-compose.yml`, `docker/trino/catalog/` | Service and catalog config are provided; user must run Docker to verify |
| 3.4 Presto | Not Implemented | None | Trino is the modern fork used for the lab |

Recommended improvement:

- If you want this to be fully cloud-native, write Spark output directly to MinIO (`s3a://...`) instead of local `data/` folders.

## 4. Streaming & Change Data Capture

| Topic | Status | Project Artifact | Notes |
| --- | --- | --- | --- |
| 4.1 Kafka Internals | Optional Lab | `docker-compose.yml`, `docs/kafka_debezium_notes.md` | Kafka service exists; internals are documented |
| 4.2 Debezium & CDC Patterns | Optional Lab + Demo | `debezium/register-postgres-connector.json`, `src/cdc_simulator.py` | Docker lab uses real Debezium; simulator is no-Docker fallback |
| 4.3 Exactly-Once Semantics | Demo | `src/streaming_features.py` | Demonstrates checkpoint + dedup + aggregate state, not Kafka transactions |
| 4.4 Streaming Feature Generation | Demo | `src/streaming_features.py` | Builds customer-level features from CDC-style events |

Recommended improvement:

- Add a real Kafka consumer that reads `retail.public.order_lines` and writes features to DuckDB or Delta with idempotent upserts.

## What Is Needed vs Optional

For a clean Level 1 project submission, run and show:

1. `python src/pipeline.py`
2. `python src/build_dw.py`
3. `python src/analytics_report.py`
4. `python src/lakehouse_pipeline.py`
5. `python src/build_data_vault.py`
6. `dbt run --profiles-dir .` inside `dbt_duckdb`
7. `python src/cdc_simulator.py`
8. `python src/streaming_features.py`

Optional extras:

1. `python src/spark_lakehouse.py`
2. `python src/spark_delta_lakehouse.py`
3. Docker lab in `docs/real_system_runbook.md`

Not necessary unless the evaluator asks:

- Real HTAP system.
- Presto in addition to Trino.
- Iceberg/Hudi running tables.
- Cloud provider deployment.
