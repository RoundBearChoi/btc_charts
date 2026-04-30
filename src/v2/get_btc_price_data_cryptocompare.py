import pandas as pd
import os
import cryptocompare
import math
import datetime as dt
import time

# ==================== CONFIGURATION ====================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "cryptocompare_data")

CSV_FILE = os.path.join(DATA_DIR, 'cryptocompare_historic_btc_price.csv')
# =======================================================

def _clean_btc_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean BTC DataFrame:
      - Remove rows where ALL price/volume columns are zero (pre-trading artifacts).
      - Drop unnecessary API metadata columns (always constant).
    Returns the cleaned DataFrame.
    """
    if df.empty:
        return df

    # Remove pre-trading all-zero rows
    numeric_cols = ['high', 'low', 'open', 'volumefrom', 'volumeto', 'close']
    zero_mask = (df[numeric_cols] == 0).all(axis=1)
    removed_count = zero_mask.sum()

    if removed_count > 0:
        df = df[~zero_mask].copy()
        print(f"Removed {removed_count:,} all-zero pre-trading rows.")
    else:
        print("No all-zero pre-trading rows found.")

    # Drop metadata columns (always 'direct' / empty)
    metadata_cols = ['conversionType', 'conversionSymbol']
    dropped = []
    for col in metadata_cols:
        if col in df.columns:
            df = df.drop(columns=[col])
            dropped.append(col)
    if dropped:
        print(f"Dropped metadata columns: {', '.join(dropped)}")

    return df


def download_btc_daily(years: float, end_date: dt.date = None) -> pd.DataFrame:
    """
    Downloads approximately 'years' worth of daily BTC/USD data from CryptoCompare,
    ending on or before 'end_date' (defaults to today).
    Handles chunking in 2000-day limits.

    NOTE: Cleaning is now performed only once at the very end inside download_full_df()
          to keep logs clean and avoid redundant processing.
    """
    if end_date is None:
        end_date = dt.date.today()
    
    total_days = math.ceil(years * 365.25)
    print(f"\nDownloading ~{years} years ({total_days} days) of BTC data ending on {end_date}...")

    data = []
    days_per_chunk = 2000
    num_full_chunks = total_days // days_per_chunk
    remaining_days = total_days % days_per_chunk

    current_end = end_date

    # Full chunks of 2000 days
    for i in range(num_full_chunks):
        chunk_data = cryptocompare.get_historical_price_day(
            'BTC', currency='USD', limit=days_per_chunk, toTs=current_end
        )
        data.extend(chunk_data)
        current_end = current_end - dt.timedelta(days=days_per_chunk)

    # Remaining days
    if remaining_days > 0:
        chunk_data = cryptocompare.get_historical_price_day(
            'BTC', currency='USD', limit=remaining_days, toTs=current_end
        )
        data.extend(chunk_data)

    if not data:
        print("No data returned.")
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    df = df.sort_index()

    print(f"Downloaded {len(df):,} days of raw data (cleaning will happen after concatenation).")
    return df


def download_full_df():
    """Download full ~16 years of data in two batches (most recent 8 years + older 8 years)."""
    today = dt.date.today()

    df_recent = download_btc_daily(8.0)  # Most recent ~8 years

    time.sleep(1)  # Be gentle on the API

    # Older batch ends one day before the oldest date in recent data
    if not df_recent.empty:
        older_end_date = df_recent.index.min().date() - dt.timedelta(days=1)
        df_older = download_btc_daily(8.0, end_date=older_end_date)
    else:
        df_older = pd.DataFrame()

    # Combine (older first)
    if not df_older.empty and not df_recent.empty:
        full_df = pd.concat([df_older, df_recent])
    elif not df_older.empty:
        full_df = df_older
    else:
        full_df = df_recent

    full_df = full_df.sort_index()

    # === FINAL CLEANING — DONE ONLY ONCE ===
    full_df = _clean_btc_dataframe(full_df)

    # Extra safety: guard against any accidental date overlap between batches
    if not full_df.empty:
        full_df = full_df[~full_df.index.duplicated(keep='first')]

    print(f"\nFinal cleaned DataFrame: {len(full_df):,} rows "
          f"from {full_df.index.min().date()} to {full_df.index.max().date()}")

    return full_df


def load_btc_data():
    """Load BTC data from the cached CSV file."""
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(
            f"❌ '{CSV_FILE}' not found.\n"
            f"Please run this script first (or call get_btc_price_data()) to download and cache the BTC data.\n"
            f"Data will be saved in folder: {DATA_DIR}"
        )
    
    try:
        print(f"\nLoading BTC data from {CSV_FILE}...")
        df = pd.read_csv(CSV_FILE, index_col=0, parse_dates=True)
        print(f"Loaded {len(df):,} rows (latest date: {df.index.max().date()})")
        return df
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load {CSV_FILE}: {e}") from e


def get_btc_price_data(force_download: bool = False) -> pd.DataFrame:
    """
    Main entry point: returns the full cleaned BTC daily price DataFrame.
    """
    if not force_download and os.path.exists(CSV_FILE):
        try:
            return load_btc_data()
        except Exception as e:
            print(f"⚠️  {e}\nDownloading fresh data instead.")
    
    print("Downloading fresh BTC data...")
    daily = download_full_df()
    
    # Ensure directory exists and save clean cache
    os.makedirs(DATA_DIR, exist_ok=True)
    daily.to_csv(CSV_FILE)
    print(f"✅ Clean data saved to: {os.path.abspath(CSV_FILE)}")
    
    return daily


if __name__ == "__main__":
    print("=== BTC Price Data Fetcher (CryptoCompare) ===")
    print(f"Script location : {SCRIPT_DIR}")
    print(f"Data folder     : {DATA_DIR}")
    print(f"CSV file        : {CSV_FILE}")
    df = get_btc_price_data()
    print(f"\nFinal DataFrame ready: {len(df):,} rows")
    print(f"Date range: {df.index.min().date()} to {df.index.max().date()}")
    print(f"Cache file: {CSV_FILE}")
