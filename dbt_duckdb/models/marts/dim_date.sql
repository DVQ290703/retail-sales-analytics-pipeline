SELECT DISTINCT
    order_date,
    EXTRACT(year FROM order_date) AS year,
    EXTRACT(month FROM order_date) AS month,
    EXTRACT(day FROM order_date) AS day,
    STRFTIME(order_date, '%Y-%m') AS year_month
FROM {{ ref('stg_sales') }}
WHERE order_date IS NOT NULL
