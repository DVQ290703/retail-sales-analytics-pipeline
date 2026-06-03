# Real-System Lab Runbook

This runbook is optional. It is for learning how the local project would connect to real infrastructure components.

The lab provides:

- Postgres as an OLTP database.
- Kafka as the event log.
- Debezium Connect as the CDC service.
- MinIO as local S3-compatible object storage.
- Trino as a distributed SQL query engine.

The lab does **not** currently include:

- A production-ready Kafka cluster.
- A real Kafka consumer writing features to DuckDB/Delta.
- Iceberg or Hudi catalogs.
- Cloud deployment on AWS/GCP/Azure.

## Architecture

```text
Online Retail CSV
  -> src/load_oltp_postgres.py
  -> Postgres OLTP
  -> Debezium PostgreSQL connector
  -> Kafka topics

Local files
  -> Pandas/Spark
  -> Parquet or Delta lakehouse folders
  -> DuckDB queries

Trino
  -> PostgreSQL catalog
  -> MinIO catalog placeholder for object-storage learning
```

## Start Services

Make sure the local virtual environment has the latest dependencies:

```powershell
pip install -r requirements.txt
```

The Postgres loader uses `pg8000`, a pure-Python driver, so it does not require local `libpq` installation on Windows.

```powershell
docker compose up -d postgres zookeeper kafka connect minio trino
```

Endpoints:

- Postgres: `localhost:5432`
- Kafka broker: `localhost:9092`
- Kafka Connect: `http://localhost:8083`
- MinIO API: `http://localhost:9000`
- MinIO console: `http://localhost:9001`
- Trino: `http://localhost:8080`

MinIO login:

```text
user: minio
password: minio123
```

## Seed Postgres OLTP

Run the local pipeline first:

```powershell
python src/pipeline.py
```

Then load a sample into Postgres:

```powershell
python src/load_oltp_postgres.py
```

The loader reads:

```text
data/processed/cleaned_online_retail.csv
```

and writes to:

```text
customers
products
orders
order_lines
```

## Register Debezium Connector

```powershell
.\scripts\register_debezium_connector.ps1
```

Check status:

```powershell
Invoke-RestMethod http://localhost:8083/connectors/retail-postgres-connector/status
```

Expected Kafka topics:

```text
retail.public.customers
retail.public.products
retail.public.orders
retail.public.order_lines
```

## Query Postgres with Trino

Use Trino CLI, a JDBC client, or the Trino Web UI.

Example SQL:

```sql
SHOW CATALOGS;
SHOW SCHEMAS FROM postgres;
SHOW TABLES FROM postgres.public;
SELECT COUNT(*) FROM postgres.public.order_lines;
```

## About the MinIO Catalog

`docker/trino/catalog/minio.properties` is included to show how a query engine can be configured against S3-compatible storage.

Current limitation:

- The Spark scripts write to local `data/` paths, not directly to `s3a://retail-lakehouse/`.
- The MinIO catalog is therefore a learning scaffold, not the main query path.

To make MinIO fully active, add Spark S3A configuration and write lakehouse tables to MinIO.

## Delta Lake

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run:

```powershell
python src/spark_delta_lakehouse.py
```

Expected result:

```text
data/delta_lakehouse/
```

Delta table folders should contain:

```text
_delta_log/
```

## Stop Services

```powershell
docker compose down
```
