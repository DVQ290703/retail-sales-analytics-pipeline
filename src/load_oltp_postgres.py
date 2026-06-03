from pathlib import Path

import pandas as pd
import pg8000.dbapi

PROCESSED_PATH = Path("data/processed/cleaned_online_retail.csv")
POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "retail_oltp",
    "user": "retail",
    "password": "retail",
}


def execute_many(cursor, query, rows):
    if rows:
        cursor.executemany(query, rows)


def to_records(df, columns):
    records = []
    for row in df[columns].itertuples(index=False, name=None):
        normalized = []
        for value in row:
            if pd.isna(value):
                normalized.append(None)
            elif isinstance(value, pd.Timestamp):
                normalized.append(value.to_pydatetime())
            else:
                normalized.append(value.item() if hasattr(value, "item") else value)
        records.append(tuple(normalized))

    return records


def main(limit=10000):
    df = pd.read_csv(PROCESSED_PATH).head(limit)
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])

    customers = to_records(
        df.drop_duplicates("customer_id"),
        ["customer_id", "country"],
    )
    products = to_records(
        df.drop_duplicates("stock_code"),
        ["stock_code", "description"],
    )
    orders = to_records(
        df.drop_duplicates("invoice_no"),
        ["invoice_no", "customer_id", "invoice_date", "is_cancelled"],
    )
    order_lines = to_records(
        df.drop_duplicates(["invoice_no", "stock_code"]),
        ["invoice_no", "stock_code", "quantity", "unit_price"],
    )

    conn = pg8000.dbapi.connect(**POSTGRES_CONFIG)
    try:
        cursor = conn.cursor()
        execute_many(
            cursor,
            """
            INSERT INTO customers (customer_id, country)
            VALUES (%s, %s)
            ON CONFLICT (customer_id) DO UPDATE
            SET country = EXCLUDED.country
            """,
            customers,
        )
        execute_many(
            cursor,
            """
            INSERT INTO products (stock_code, description)
            VALUES (%s, %s)
            ON CONFLICT (stock_code) DO UPDATE
            SET description = EXCLUDED.description
            """,
            products,
        )
        execute_many(
            cursor,
            """
            INSERT INTO orders (invoice_no, customer_id, invoice_date, is_cancelled)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (invoice_no) DO UPDATE
            SET customer_id = EXCLUDED.customer_id,
                invoice_date = EXCLUDED.invoice_date,
                is_cancelled = EXCLUDED.is_cancelled
            """,
            orders,
        )
        execute_many(
            cursor,
            """
            INSERT INTO order_lines (invoice_no, stock_code, quantity, unit_price)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (invoice_no, stock_code) DO UPDATE
            SET quantity = EXCLUDED.quantity,
                unit_price = EXCLUDED.unit_price,
                updated_at = CURRENT_TIMESTAMP
            """,
            order_lines,
        )
        conn.commit()
    finally:
        conn.close()

    print(f"Loaded {len(df)} source rows into Postgres OLTP")


if __name__ == "__main__":
    main()
