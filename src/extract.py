import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/online_retail.xlsx")


def extract():
    print("Extracting data...")
    df = pd.read_excel(RAW_PATH)
    return df