from pathlib import Path
import pandas as pd

BRONZE_PATH = Path("data/bronze/sales.parquet")
SILVER_PATH = Path("data/silver/cleaned_sales.parquet")
GOLD_MONTHLY_PATH = Path("data/gold/monthly_revenue.parquet")
GOLD_COUNTRY_PATH = Path("data/gold/country_revenue.parquet")

PROCESSED_PATH = Path("data/processed/cleaned_online_retail.csv")


def create_dirs():
    for path in [BRONZE_PATH, SILVER_PATH, GOLD_MONTHLY_PATH, GOLD_COUNTRY_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)


def bronze_layer():
    print("Creating Bronze layer...")

    df = pd.read_csv(PROCESSED_PATH)
    df.to_parquet(BRONZE_PATH, index=False)

    print(f"Bronze saved: {BRONZE_PATH}")
    return df


def silver_layer(df):
    print("Creating Silver layer...")

    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    df["total_amount"] = df["quantity"] * df["unit_price"]

    silver_df = df[
        (df["quantity"] > 0) &
        (df["unit_price"] > 0) &
        (df["is_cancelled"] == False)
    ].copy()

    silver_df.to_parquet(SILVER_PATH, index=False)

    print(f"Silver saved: {SILVER_PATH}")
    return silver_df


def gold_layer(silver_df):
    print("Creating Gold layer...")

    monthly_revenue = (
        silver_df
        .assign(month=silver_df["invoice_date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "revenue"})
    )

    country_revenue = (
        silver_df
        .groupby("country", as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "revenue"})
        .sort_values("revenue", ascending=False)
    )

    monthly_revenue.to_parquet(GOLD_MONTHLY_PATH, index=False)
    country_revenue.to_parquet(GOLD_COUNTRY_PATH, index=False)

    print(f"Gold saved: {GOLD_MONTHLY_PATH}")
    print(f"Gold saved: {GOLD_COUNTRY_PATH}")


def main():
    create_dirs()

    bronze_df = bronze_layer()
    silver_df = silver_layer(bronze_df)
    gold_layer(silver_df)

    print("Lakehouse pipeline completed successfully!")


if __name__ == "__main__":
    main()