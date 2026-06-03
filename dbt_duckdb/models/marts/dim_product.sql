SELECT DISTINCT
    stock_code,
    description
FROM {{ ref('stg_sales') }}
WHERE stock_code IS NOT NULL
