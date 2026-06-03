from pathlib import Path

import pandas as pd
import psycopg

PROCESSED_PATH = Path("data/processed/cleaned_online_retail.csv")
POSTGRES_DSN = "postgresql://retail:retail@localhost:5432/retail_oltp"


def execute_many(cursor, query, rows):
    if rows:
        cursor.executemany(query, rows)


def main(limit=10000):
    df = pd.read_csv(PROCESSED_PATH).head(limit)
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])

    customers = (
        df[["customer_id", "country"]]
        .drop_duplicates("customer_id")
        .itertuples(index=False, name=None)
    )
    products = (
        df[["stock_code", "description"]]
        .drop_duplicates("stock_code")
        .itertuples(index=False, name=None)
    )
    orders = (
        df[["invoice_no", "customer_id", "invoice_date", "is_cancelled"]]
        .drop_duplicates("invoice_no")
        .itertuples(index=False, name=None)
    )
    order_lines = (
        df[["invoice_no", "stock_code", "quantity", "unit_price"]]
        .drop_duplicates(["invoice_no", "stock_code"])
        .itertuples(index=False, name=None)
    )

    with psycopg.connect(POSTGRES_DSN) as conn:
        with conn.cursor() as cursor:
            execute_many(
                cursor,
                """
                INSERT INTO customers (customer_id, country)
                VALUES (%s, %s)
                ON CONFLICT (customer_id) DO UPDATE
                SET country = EXCLUDED.country
                """,
                list(customers),
            )
            execute_many(
                cursor,
                """
                INSERT INTO products (stock_code, description)
                VALUES (%s, %s)
                ON CONFLICT (stock_code) DO UPDATE
                SET description = EXCLUDED.description
                """,
                list(products),
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
                list(orders),
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
                list(order_lines),
            )

    print(f"Loaded {len(df)} source rows into Postgres OLTP")


if __name__ == "__main__":
    main()
