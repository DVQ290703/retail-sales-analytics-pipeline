import pandas as pd


def transform(df):
    print("Transforming data...")

    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={
        "invoiceno": "invoice_no",
        "stockcode": "stock_code",
        "invoicedate": "invoice_date",
        "unitprice": "unit_price",
        "customerid": "customer_id"
    })

    df = df.dropna(subset=[
        "invoice_no",
        "stock_code",
        "description",
        "invoice_date"
    ])

    df["customer_id"] = df["customer_id"].fillna(-1).astype(int)
    df["is_cancelled"] = df["invoice_no"].astype(str).str.startswith("C")
    df["total_amount"] = df["quantity"] * df["unit_price"]
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    df["date"] = df["invoice_date"].dt.date

    return df