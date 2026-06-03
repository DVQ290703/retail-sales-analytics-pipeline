# Kafka, Debezium, and Streaming Notes

This project has two CDC paths:

1. **No-Docker demo**: `src/cdc_simulator.py` writes JSONL events, and `src/streaming_features.py` consumes them.
2. **Optional Docker lab**: Postgres, Kafka, and Debezium are configured, but no real Kafka consumer is implemented yet.

## Kafka Internals

Core concepts:

- Topic: named stream of records.
- Partition: ordered log shard inside a topic.
- Offset: record position inside a partition.
- Consumer group: distributes partitions across consumers.
- Retention: controls how long records stay available.
- Replication: copies partitions across brokers for fault tolerance.

Project status:

- Kafka broker exists in `docker-compose.yml`.
- The project does not yet include a Python/Spark consumer that reads Kafka topics.

## Debezium CDC Pattern

Debezium reads database transaction logs instead of polling tables.

For this project:

- Postgres logical replication is enabled in `docker-compose.yml`.
- Source tables are initialized in `docker/postgres/init/01_schema.sql`.
- Connector config is in `debezium/register-postgres-connector.json`.
- Registration helper is `scripts/register_debezium_connector.ps1`.

Expected Debezium topics:

```text
retail.public.customers
retail.public.products
retail.public.orders
retail.public.order_lines
```

## Debezium Event Shape

Typical event envelope:

```json
{
  "before": {},
  "after": {},
  "op": "c",
  "source": {},
  "ts_ms": 1710000000000
}
```

Operations:

- `c`: create
- `u`: update
- `d`: delete
- `r`: snapshot read

## Exactly-Once Semantics

The local demo approximates exactly-once output using:

- Stable event IDs.
- Checkpoint offset.
- Processed-event deduplication.
- Customer aggregate state.

Files:

```text
src/streaming_features.py
data/cdc/checkpoint.json
data/cdc/customer_feature_state.json
```

This is not the same as Kafka transactional exactly-once.

Production-style exactly-once usually needs:

- Deterministic processing.
- Idempotent or transactional sink writes.
- Offset commits only after successful sink writes.
- Replay-safe event keys.

## Streaming Feature Generation

Current local features:

- `order_count`
- `line_count`
- `lifetime_revenue`
- `avg_line_value`
- `last_invoice_date`

Output:

```text
data/gold/customer_streaming_features.csv
```

Recommended next implementation:

- Add `src/kafka_feature_consumer.py`.
- Read `retail.public.order_lines`.
- Upsert features into DuckDB or Delta.
- Commit Kafka offsets after the upsert succeeds.
