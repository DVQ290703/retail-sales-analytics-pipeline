CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    country TEXT
);

CREATE TABLE IF NOT EXISTS products (
    stock_code TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    invoice_no TEXT PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    invoice_date TIMESTAMP NOT NULL,
    is_cancelled BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS order_lines (
    invoice_no TEXT REFERENCES orders(invoice_no),
    stock_code TEXT REFERENCES products(stock_code),
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (invoice_no, stock_code)
);

ALTER TABLE customers REPLICA IDENTITY FULL;
ALTER TABLE products REPLICA IDENTITY FULL;
ALTER TABLE orders REPLICA IDENTITY FULL;
ALTER TABLE order_lines REPLICA IDENTITY FULL;
