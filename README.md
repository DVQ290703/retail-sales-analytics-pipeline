# Retail Data Pipeline

Portfolio project for **Level 1 Data Engineering Core**.

The project has two layers:

1. **Core local pipeline**: runs with Python, DuckDB, dbt, Parquet, and optional Spark.
2. **Optional real-system lab**: runs with Docker services for Postgres, Kafka, Debezium, MinIO, and Trino.

Use the core pipeline first. The Docker lab is useful for learning CDC and query-engine architecture, but it is not required for the basic project demo.

## Project Scope

### Core files to keep

- `src/pipeline.py`: batch ETL entrypoint.
- `src/extract.py`, `src/transform.py`, `src/load.py`: extract, clean, and load data.
- `src/build_dw.py`: dimensional warehouse tables in DuckDB.
- `src/analytics_report.py`: analytics CSV outputs.
- `src/lakehouse_pipeline.py`: local Bronze/Silver/Gold Parquet demo.
- `src/query_gold.py`: DuckDB query over Parquet gold files.
- `dbt_duckdb/`: dbt analytics engineering project.
- `sql/data_vault.sql` and `src/build_data_vault.py`: Data Vault demo.
- `docs/level1_coverage.md`: checklist mapping.

### Optional advanced files

- `src/spark_lakehouse.py`: Spark Parquet lakehouse demo.
- `src/spark_delta_lakehouse.py`: Delta Lake demo.
- `src/cdc_simulator.py` and `src/streaming_features.py`: no-Docker CDC and streaming feature demo.
- `docker-compose.yml`, `docker/`, `debezium/`, `scripts/`: real-system lab.
- `src/load_oltp_postgres.py`: loads processed data into Docker Postgres.

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Place the Online Retail dataset here:

```text
data/raw/online_retail.xlsx
```

## 1. Core Batch ETL + DuckDB Warehouse

Run:

```bash
python src/pipeline.py
python src/build_dw.py
python src/check_dw.py
python src/analytics_report.py
```

Outputs:

```text
data/processed/cleaned_online_retail.csv
retail_dw.duckdb
reports/output/
```

This covers:

- Batch ETL.
- OLAP warehouse.
- Dimensional modeling.
- DuckDB query engine.

## 2. Local Lakehouse Demo

Pandas + Parquet:

```bash
python src/lakehouse_pipeline.py
python src/query_gold.py
```

Outputs:

```text
data/bronze/
data/silver/
data/gold/
```

Optional Spark + Parquet:

```bash
python src/spark_lakehouse.py
```

Optional Spark + Delta Lake:

```bash
python src/spark_delta_lakehouse.py
```

Delta output should include `_delta_log` folders under:

```text
data/delta_lakehouse/
```

## 3. dbt Analytics Engineering

Requirement: `retail_dw.duckdb` must already contain `staging_sales`, so run `python src/pipeline.py` first.

```bash
cd dbt_duckdb
dbt debug --profiles-dir .
dbt run --profiles-dir .
dbt test --profiles-dir .
dbt docs generate --profiles-dir .
cd ..
```

Main folders:

```text
dbt_duckdb/models/staging/
dbt_duckdb/models/marts/
```

## 4. Data Vault Demo

Requirement: run `python src/pipeline.py` first.

```bash
python src/build_data_vault.py
```

Main SQL:

```text
sql/data_vault.sql
```

This creates Hub, Link, and Satellite tables in `retail_dw.duckdb`.

## 5. No-Docker CDC + Streaming Features

This is a lightweight fallback for learning CDC concepts without Kafka.

```bash
python src/cdc_simulator.py
python src/streaming_features.py
```

Outputs:

```text
data/cdc/events.jsonl
data/cdc/checkpoint.json
data/cdc/customer_feature_state.json
data/gold/customer_streaming_features.csv
```

This covers:

- Debezium-like event envelope.
- Event IDs.
- Checkpointing.
- Deduplication.
- Customer feature aggregation.

## 6. Optional Real-System Lab

Use this only if Docker is available and you want real Kafka/Debezium/Trino services.

Start services:

```bash
docker compose up -d postgres zookeeper kafka connect minio trino
```

Seed Postgres OLTP:

```bash
python src/pipeline.py
python src/load_oltp_postgres.py
```

Register Debezium connector:

```powershell
.\scripts\register_debezium_connector.ps1
```

Read the full runbook:

```text
docs/real_system_runbook.md
```

Stop services:

```bash
docker compose down
```

## Documentation

- `docs/level1_coverage.md`: exact Level 1 checklist status.
- `docs/project_inventory.md`: what is required, optional, or removable.
- `docs/cloud_storage_and_table_formats.md`: object storage and table format notes.
- `docs/kafka_debezium_notes.md`: Kafka, Debezium, exactly-once, and streaming notes.
- `docs/real_system_runbook.md`: Docker lab commands.
