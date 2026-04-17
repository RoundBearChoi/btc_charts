import pandas as pd
import os

CSV_FILE = 'btc_data.csv'

def load_btc_data():
    """Load BTC data from the cached CSV file.
    
    Raises clear, user-friendly errors if the file is missing or unreadable.
    """
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(
            f"❌ '{CSV_FILE}' not found.\n"
            "Please run main.py first to download and cache the BTC data."
        )
    
    try:
        print(f"Loading BTC data from {CSV_FILE}...")
        df = pd.read_csv(CSV_FILE, index_col=0, parse_dates=True)
        print(f"✅ Loaded {len(df):,} rows (latest date: {df.index.max().date()})")
        return df
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load {CSV_FILE}: {e}") from e
