# Cloud Storage and Table Formats

This project teaches cloud-storage and lakehouse concepts mostly through local files, with MinIO available as an optional S3-compatible lab.

## What the Project Actually Uses

| Storage/Form | Implemented? | Artifact |
| --- | --- | --- |
| Local Parquet | Yes | `src/lakehouse_pipeline.py`, `src/spark_lakehouse.py` |
| Delta Lake | Optional | `src/spark_delta_lakehouse.py` |
| MinIO / S3-compatible storage | Scaffolded | `docker-compose.yml`, `docker/trino/catalog/minio.properties` |
| Iceberg | No | Documented only |
| Hudi | No | Documented only |
| Real AWS S3 / GCS / ADLS | No | Not part of this local project |

## Object Storage Concepts

Object storage is not a normal filesystem.

Important ideas:

- Objects are immutable blobs addressed by keys.
- Folders are simulated through key prefixes.
- Listing many small objects can be slow and expensive.
- Partitioning helps query engines skip data.
- Lifecycle rules can expire or move old files.
- IAM/service accounts control access.

Local folders mirror object-storage prefixes:

```text
data/bronze/
data/silver/
data/gold/
data/spark_lakehouse/
data/delta_lakehouse/
```

## Table Formats

| Format | What It Provides | Project Status |
| --- | --- | --- |
| Parquet | Columnar files | Implemented |
| Delta Lake | ACID log, schema evolution, time travel | Optional script |
| Iceberg | Open table format, hidden partitioning, multi-engine support | Not implemented |
| Hudi | Upserts, incremental reads, compaction timeline | Not implemented |

## Partitioning Choice

The Spark Parquet job partitions by:

```text
year_month
```

Reason:

- Revenue reporting is month-based.
- Monthly partitions avoid too many small files.
- Query engines can prune partitions for month filters.

## Small Files Notes

The Spark jobs use:

- `spark.sql.shuffle.partitions=8`
- `spark.sql.adaptive.enabled=true`
- `repartition("year_month")`
- `coalesce(1)` for tiny Gold outputs

In production:

- Delta uses `OPTIMIZE`.
- Iceberg uses file rewrite actions.
- Hudi uses clustering and compaction.

## If You Want a Real Cloud-Style Upgrade

Next practical upgrade:

1. Write Spark output to MinIO with `s3a://retail-lakehouse/...`.
2. Add a Hive Metastore, Nessie, Glue, or Iceberg REST catalog.
3. Query lakehouse tables from Trino.
4. Add table-maintenance commands for compaction and cleanup.
