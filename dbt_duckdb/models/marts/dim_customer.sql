SELECT DISTINCT
    customer_id,
    country
FROM {{ ref('stg_sales') }}
WHERE customer_id IS NOT NULL
