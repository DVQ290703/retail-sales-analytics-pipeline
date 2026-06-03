import json
from pathlib import Path

import pandas as pd

EVENT_LOG_PATH = Path("data/cdc/events.jsonl")
CHECKPOINT_PATH = Path("data/cdc/checkpoint.json")
FEATURE_STATE_PATH = Path("data/cdc/customer_feature_state.json")
FEATURE_OUTPUT_PATH = Path("data/gold/customer_streaming_features.csv")


def load_json(path, default):
    if not path.exists():
        return default

    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def read_events():
    with EVENT_LOG_PATH.open("r", encoding="utf-8") as input_file:
        for line in input_file:
            if line.strip():
                yield json.loads(line)


def update_feature_state(feature_state, events):
    for event in events:
        after = event["after"]
        if after["is_cancelled"]:
            continue

        customer_key = f"{after['customer_id']}|{after['country']}"
        customer_state = feature_state.setdefault(
            customer_key,
            {
                "customer_id": after["customer_id"],
                "country": after["country"],
                "invoice_nos": [],
                "line_count": 0,
                "lifetime_revenue": 0.0,
                "last_invoice_date": after["invoice_date"],
            },
        )

        if after["invoice_no"] not in customer_state["invoice_nos"]:
            customer_state["invoice_nos"].append(after["invoice_no"])

        customer_state["line_count"] += 1
        customer_state["lifetime_revenue"] += after["total_amount"]
        customer_state["last_invoice_date"] = max(
            customer_state["last_invoice_date"],
            after["invoice_date"],
        )

    return feature_state


def write_feature_output(feature_state):
    rows = []
    for customer_state in feature_state.values():
        line_count = customer_state["line_count"]
        rows.append(
            {
                "customer_id": customer_state["customer_id"],
                "country": customer_state["country"],
                "order_count": len(customer_state["invoice_nos"]),
                "line_count": line_count,
                "lifetime_revenue": round(customer_state["lifetime_revenue"], 2),
                "avg_line_value": round(
                    customer_state["lifetime_revenue"] / line_count,
                    2,
                )
                if line_count
                else 0,
                "last_invoice_date": customer_state["last_invoice_date"],
            }
        )

    FEATURE_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).sort_values(
        ["lifetime_revenue", "customer_id"],
        ascending=[False, True],
    ).to_csv(FEATURE_OUTPUT_PATH, index=False)


def main():
    checkpoint = load_json(
        CHECKPOINT_PATH,
        {"processed_event_ids": [], "last_offset": -1},
    )
    feature_state = load_json(FEATURE_STATE_PATH, {})
    processed_event_ids = set(checkpoint["processed_event_ids"])
    new_events = []
    last_offset = checkpoint["last_offset"]

    for event in read_events():
        event_id = event["event_id"]
        offset = event["source"]["offset"]

        if event_id in processed_event_ids:
            continue

        new_events.append(event)
        processed_event_ids.add(event_id)
        last_offset = max(last_offset, offset)

    feature_state = update_feature_state(feature_state, new_events)
    write_feature_output(feature_state)
    write_json(FEATURE_STATE_PATH, feature_state)
    write_json(
        CHECKPOINT_PATH,
        {
            "processed_event_ids": sorted(processed_event_ids),
            "last_offset": last_offset,
        },
    )

    print(f"Processed {len(new_events)} new CDC events")
    print(f"Saved streaming features to {FEATURE_OUTPUT_PATH}")
    print(f"Checkpoint offset: {last_offset}")


if __name__ == "__main__":
    main()
