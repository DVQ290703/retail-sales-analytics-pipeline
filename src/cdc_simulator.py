import json
from pathlib import Path

import pandas as pd

PROCESSED_PATH = Path("data/processed/cleaned_online_retail.csv")
EVENT_LOG_PATH = Path("data/cdc/events.jsonl")


def build_debezium_like_event(row, offset):
    invoice_no = str(row["invoice_no"])
    stock_code = str(row["stock_code"])
    event_id = f"{invoice_no}:{stock_code}:{offset}"

    return {
        "event_id": event_id,
        "source": {
            "connector": "retail-cdc-simulator",
            "db": "retail_oltp",
            "table": "order_lines",
            "offset": offset,
        },
        "op": "c" if not bool(row["is_cancelled"]) else "u",
        "ts_ms": int(pd.Timestamp.now("UTC").timestamp() * 1000),
        "before": None,
        "after": {
            "invoice_no": invoice_no,
            "stock_code": stock_code,
            "customer_id": int(row["customer_id"]),
            "country": row["country"],
            "invoice_date": str(row["invoice_date"]),
            "quantity": int(row["quantity"]),
            "unit_price": float(row["unit_price"]),
            "total_amount": float(row["total_amount"]),
            "is_cancelled": bool(row["is_cancelled"]),
        },
    }


def main(limit=5000):
    EVENT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(PROCESSED_PATH).head(limit)

    with EVENT_LOG_PATH.open("w", encoding="utf-8") as output_file:
        for offset, (_, row) in enumerate(df.iterrows()):
            event = build_debezium_like_event(row, offset)
            output_file.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(f"Wrote {len(df)} CDC events to {EVENT_LOG_PATH}")


if __name__ == "__main__":
    main()
