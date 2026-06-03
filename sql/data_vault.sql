-- Data Vault 2.0 demo model derived from staging_sales.
-- Hubs store business keys, links store relationships, satellites store descriptive history.

CREATE OR REPLACE TABLE hub_customer AS
SELECT DISTINCT
    MD5(CAST(customer_id AS VARCHAR)) AS customer_hk,
    customer_id AS customer_bk,
    CURRENT_TIMESTAMP AS load_dts,
    'staging_sales' AS record_source
FROM staging_sales
WHERE customer_id IS NOT NULL;

CREATE OR REPLACE TABLE hub_product AS
SELECT DISTINCT
    MD5(CAST(stock_code AS VARCHAR)) AS product_hk,
    stock_code AS product_bk,
    CURRENT_TIMESTAMP AS load_dts,
    'staging_sales' AS record_source
FROM staging_sales
WHERE stock_code IS NOT NULL;

CREATE OR REPLACE TABLE hub_invoice AS
SELECT DISTINCT
    MD5(CAST(invoice_no AS VARCHAR)) AS invoice_hk,
    invoice_no AS invoice_bk,
    CURRENT_TIMESTAMP AS load_dts,
    'staging_sales' AS record_source
FROM staging_sales
WHERE invoice_no IS NOT NULL;

CREATE OR REPLACE TABLE link_invoice_product AS
SELECT DISTINCT
    MD5(CONCAT(CAST(invoice_no AS VARCHAR), '|', CAST(stock_code AS VARCHAR))) AS invoice_product_hk,
    MD5(CAST(invoice_no AS VARCHAR)) AS invoice_hk,
    MD5(CAST(stock_code AS VARCHAR)) AS product_hk,
    CURRENT_TIMESTAMP AS load_dts,
    'staging_sales' AS record_source
FROM staging_sales
WHERE invoice_no IS NOT NULL
  AND stock_code IS NOT NULL;

CREATE OR REPLACE TABLE link_invoice_customer AS
SELECT DISTINCT
    MD5(CONCAT(CAST(invoice_no AS VARCHAR), '|', CAST(customer_id AS VARCHAR))) AS invoice_customer_hk,
    MD5(CAST(invoice_no AS VARCHAR)) AS invoice_hk,
    MD5(CAST(customer_id AS VARCHAR)) AS customer_hk,
    CURRENT_TIMESTAMP AS load_dts,
    'staging_sales' AS record_source
FROM staging_sales
WHERE invoice_no IS NOT NULL
  AND customer_id IS NOT NULL;

CREATE OR REPLACE TABLE sat_customer_country AS
SELECT DISTINCT
    MD5(CAST(customer_id AS VARCHAR)) AS customer_hk,
    MD5(COALESCE(country, '')) AS hashdiff,
    country,
    CURRENT_TIMESTAMP AS load_dts,
    'staging_sales' AS record_source
FROM staging_sales
WHERE customer_id IS NOT NULL;

CREATE OR REPLACE TABLE sat_product_description AS
SELECT DISTINCT
    MD5(CAST(stock_code AS VARCHAR)) AS product_hk,
    MD5(COALESCE(description, '')) AS hashdiff,
    description,
    CURRENT_TIMESTAMP AS load_dts,
    'staging_sales' AS record_source
FROM staging_sales
WHERE stock_code IS NOT NULL;

CREATE OR REPLACE TABLE sat_invoice_line_metrics AS
SELECT
    MD5(CONCAT(CAST(invoice_no AS VARCHAR), '|', CAST(stock_code AS VARCHAR))) AS invoice_product_hk,
    MD5(CONCAT(
        COALESCE(CAST(quantity AS VARCHAR), ''),
        '|',
        COALESCE(CAST(unit_price AS VARCHAR), ''),
        '|',
        COALESCE(CAST(total_amount AS VARCHAR), '')
    )) AS hashdiff,
    quantity,
    unit_price,
    total_amount,
    is_cancelled,
    invoice_date,
    CURRENT_TIMESTAMP AS load_dts,
    'staging_sales' AS record_source
FROM staging_sales
WHERE invoice_no IS NOT NULL
  AND stock_code IS NOT NULL;
