-- Normalized OLTP-style source schema for retail transactions.
-- This is intentionally separate from the OLAP star schema in DuckDB.

CREATE TABLE IF NOT EXISTS oltp_customers (
    customer_id INTEGER PRIMARY KEY,
    country VARCHAR
);

CREATE TABLE IF NOT EXISTS oltp_products (
    stock_code VARCHAR PRIMARY KEY,
    description VARCHAR
);

CREATE TABLE IF NOT EXISTS oltp_orders (
    invoice_no VARCHAR PRIMARY KEY,
    customer_id INTEGER,
    invoice_date TIMESTAMP,
    is_cancelled BOOLEAN,
    FOREIGN KEY (customer_id) REFERENCES oltp_customers(customer_id)
);

CREATE TABLE IF NOT EXISTS oltp_order_lines (
    invoice_no VARCHAR,
    stock_code VARCHAR,
    quantity INTEGER,
    unit_price DOUBLE,
    PRIMARY KEY (invoice_no, stock_code),
    FOREIGN KEY (invoice_no) REFERENCES oltp_orders(invoice_no),
    FOREIGN KEY (stock_code) REFERENCES oltp_products(stock_code)
);
