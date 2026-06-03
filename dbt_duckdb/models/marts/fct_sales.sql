SELECT
    invoice_no,
    stock_code,
    customer_id,
    country,
    order_date,
    invoice_date,
    quantity,
    unit_price,
    total_amount,
    is_cancelled
FROM {{ ref('stg_sales') }}
