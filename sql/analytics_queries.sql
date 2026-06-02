-- Tổng số dòng
SELECT COUNT(*) FROM staging_sales;

-- Doanh thu tổng
SELECT SUM(total_amount) AS total_revenue
FROM staging_sales
WHERE is_cancelled = false;

-- Doanh thu theo tháng
SELECT 
    DATE_TRUNC('month', invoice_date) AS month,
    SUM(total_amount) AS revenue
FROM staging_sales
WHERE is_cancelled = false
GROUP BY month
ORDER BY month;

-- Top 10 sản phẩm doanh thu cao nhất
SELECT 
    stock_code,
    description,
    SUM(total_amount) AS revenue
FROM staging_sales
WHERE is_cancelled = false
GROUP BY stock_code, description
ORDER BY revenue DESC
LIMIT 10;