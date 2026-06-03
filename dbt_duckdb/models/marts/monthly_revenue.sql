SELECT
    DATE_TRUNC('month', invoice_date) AS month,
    ROUND(SUM(total_amount), 2) AS revenue
FROM {{ ref('fct_sales') }}
WHERE is_cancelled = FALSE
GROUP BY month
