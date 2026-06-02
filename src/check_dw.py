import duckdb

conn = duckdb.connect("retail_dw.duckdb")

tables = conn.execute("""
SHOW TABLES
""").fetchall()

print(tables)