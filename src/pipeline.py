from pathlib import Path

from extract import extract
from transform import transform
from load import load

PROCESSED_PATH = Path("data/processed/cleaned_online_retail.csv")


def main():
    df = extract()
    df = transform(df)

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"Saved processed data to {PROCESSED_PATH}")

    load(df)

    print("Pipeline completed successfully!")


if __name__ == "__main__":
    main()