SELECT
    CAST(invoice_no AS VARCHAR) AS invoice_no,
    CAST(stock_code AS VARCHAR) AS stock_code,
    CAST(description AS VARCHAR) AS description,
    CAST(customer_id AS INTEGER) AS customer_id,
    CAST(country AS VARCHAR) AS country,
    CAST(invoice_date AS TIMESTAMP) AS invoice_date,
    CAST(date AS DATE) AS order_date,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(unit_price AS DOUBLE) AS unit_price,
    CAST(total_amount AS DOUBLE) AS total_amount,
    CAST(is_cancelled AS BOOLEAN) AS is_cancelled
FROM {{ source('retail', 'staging_sales') }}
