import duckdb

conn = duckdb.connect()

monthly = conn.execute("""
SELECT *
FROM 'data/gold/monthly_revenue.parquet'
ORDER BY month
""").fetchdf()

print("\n=== MONTHLY REVENUE ===")
print(monthly.head())

country = conn.execute("""
SELECT *
FROM 'data/gold/country_revenue.parquet'
LIMIT 10
""").fetchdf()

print("\n=== TOP COUNTRIES ===")
print(country)

conn.close()