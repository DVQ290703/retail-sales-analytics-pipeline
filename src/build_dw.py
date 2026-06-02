import duckdb

conn = duckdb.connect("retail_dw.duckdb")

conn.execute("""
CREATE OR REPLACE TABLE dim_product AS
SELECT DISTINCT
    stock_code,
    description
FROM staging_sales
""")

conn.execute("""
CREATE OR REPLACE TABLE dim_country AS
SELECT DISTINCT
    country
FROM staging_sales
""")

conn.execute("""
CREATE OR REPLACE TABLE dim_customer AS
SELECT DISTINCT
    customer_id,
    country
FROM staging_sales
""")

conn.execute("""
CREATE OR REPLACE TABLE dim_date AS
SELECT DISTINCT
    date,
    YEAR(date) AS year,
    MONTH(date) AS month,
    DAY(date) AS day
FROM staging_sales
""")

conn.execute("""
CREATE OR REPLACE TABLE fact_sales AS
SELECT
    invoice_no,
    stock_code,
    customer_id,
    country,
    invoice_date,
    quantity,
    unit_price,
    total_amount,
    is_cancelled
FROM staging_sales
""")