import duckdb
from pathlib import Path

DB_PATH = Path("retail_dw.duckdb")


def load(df):
    print("Loading to DuckDB...")

    conn = duckdb.connect(DB_PATH)

    conn.execute("DROP TABLE IF EXISTS staging_sales")
    conn.register("df", df)
    conn.execute("""
        CREATE TABLE staging_sales AS
        SELECT * FROM df
    """)

    conn.close()