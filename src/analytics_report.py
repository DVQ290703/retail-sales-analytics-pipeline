import duckdb
from pathlib import Path

conn = duckdb.connect("retail_dw.duckdb")

OUTPUT_DIR = Path("reports/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

queries = {
    "monthly_revenue": """
        SELECT 
            DATE_TRUNC('month', invoice_date) AS month,
            ROUND(SUM(total_amount), 2) AS revenue
        FROM fact_sales
        WHERE is_cancelled = false
        GROUP BY month
        ORDER BY month
    """,

    "top_10_products": """
        SELECT 
            stock_code,
            description,
            ROUND(SUM(total_amount), 2) AS revenue
        FROM fact_sales f
        JOIN dim_product p USING (stock_code)
        WHERE is_cancelled = false
        GROUP BY stock_code, description
        ORDER BY revenue DESC
        LIMIT 10
    """,

    "top_10_countries": """
        SELECT 
            country,
            ROUND(SUM(total_amount), 2) AS revenue
        FROM fact_sales
        WHERE is_cancelled = false
        GROUP BY country
        ORDER BY revenue DESC
        LIMIT 10
    """,

    "cancelled_orders": """
        SELECT 
            COUNT(DISTINCT invoice_no) AS cancelled_orders
        FROM fact_sales
        WHERE is_cancelled = true
    """
}

for name, query in queries.items():
    df = conn.execute(query).fetchdf()
    output_path = OUTPUT_DIR / f"{name}.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")

conn.close()