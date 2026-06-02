import duckdb

conn = duckdb.connect("retail_dw.duckdb")

result = conn.execute("""
SELECT 
    DATE_TRUNC('month', invoice_date) AS month,
    SUM(total_amount) AS revenue
FROM staging_sales
WHERE is_cancelled = false
GROUP BY month
ORDER BY month
""").fetchdf()

print(result)