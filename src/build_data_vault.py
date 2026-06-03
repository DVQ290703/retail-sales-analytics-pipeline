from pathlib import Path

import duckdb

DB_PATH = Path("retail_dw.duckdb")
DATA_VAULT_SQL = Path("sql/data_vault.sql")


def main():
    conn = duckdb.connect(DB_PATH)
    conn.execute(DATA_VAULT_SQL.read_text(encoding="utf-8"))
    tables = conn.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'main'
          AND (
              table_name LIKE 'hub_%'
              OR table_name LIKE 'link_%'
              OR table_name LIKE 'sat_%'
          )
        ORDER BY table_name
        """
    ).fetchall()
    conn.close()

    print("Built Data Vault tables:")
    for table_name, in tables:
        print(f"- {table_name}")


if __name__ == "__main__":
    main()
