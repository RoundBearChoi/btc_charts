import pandas as pd
import os
import cryptocompare
import math
import datetime as dt
import time

CSV_FILE = 'btc_data.csv'


def download_btc_daily(years: float, end_date: dt.date = None) -> pd.DataFrame:
    """
    Downloads approximately 'years' worth of daily BTC/USD data from CryptoCompare,
    ending on or before 'end_date' (defaults to today).
    Handles chunking in 2000-day limits.
    """
    if end_date is None:
        end_date = dt.date.today()
    
    total_days = math.ceil(years * 365.25)  # Better account for leap years
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
    df = df.sort_index()  # Ensure chronological order
    df = df.resample('D').last().asfreq('D')  # Fill any missing days if needed

    print(f"Downloaded {len(df)} days of data.")
    return df


def download_full_df():
    """Download full ~16 years of data in two batches (most recent 8 years + older 8 years)."""
    today = dt.date.today()

    df_recent = download_btc_daily(8.0)  # Most recent ~8 years (up to today)

    time.sleep(1)  # Wait 1 second to be gentle on the API

    # For the older batch, calculate the end date as one day before the oldest in the recent df
    if not df_recent.empty:
        older_end_date = df_recent.index.min().date() - dt.timedelta(days=1)
        df_older = download_btc_daily(8.0, end_date=older_end_date)
    else:
        df_older = pd.DataFrame()

    # Combine them (older first)
    if not df_older.empty and not df_recent.empty:
        full_df = pd.concat([df_older, df_recent])
    elif not df_older.empty:
        full_df = df_older
    else:
        full_df = df_recent

    full_df = full_df.sort_index()
    print(f"\nTotal combined data: {len(full_df)} days from {full_df.index.min().date()} to {full_df.index.max().date()}")

    return full_df


def load_btc_data():
    """Load BTC data from the cached CSV file.
    
    Raises clear, user-friendly errors if the file is missing or unreadable.
    """
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(
            f"❌ '{CSV_FILE}' not found.\n"
            "Please run this script first (or call get_btc_price_data()) to download and cache the BTC data."
        )
    
    try:
        print(f"    Loading BTC data from {CSV_FILE}...")
        df = pd.read_csv(CSV_FILE, index_col=0, parse_dates=True)
        print(f"    Loaded {len(df):,} rows (latest date: {df.index.max().date()})")
        return df
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load {CSV_FILE}: {e}") from e


def get_btc_price_data(force_download: bool = False) -> pd.DataFrame:
    """
    Main entry point: returns the full BTC daily price DataFrame.
    
    - Uses cached CSV by default (fast, no prompt).
    - Downloads fresh data + saves cache if cache is missing or force_download=True.
    """
    if not force_download and os.path.exists(CSV_FILE):
        try:
            return load_btc_data()
        except Exception as e:
            print(f"⚠️  {e}\nDownloading fresh data instead.")
    
    print("Downloading fresh BTC data...")
    daily = download_full_df()
    
    # Save cache for next time
    daily.to_csv(CSV_FILE)
    print(f"✅ Data cached to: {os.path.abspath(CSV_FILE)}")
    
    return daily


if __name__ == "__main__":
    print("=== BTC Price Data Fetcher (CryptoCompare) ===")
    df = get_btc_price_data()
    print(f"\n✅ Final DataFrame ready: {len(df):,} rows")
    print(f"Date range: {df.index.min().date()} to {df.index.max().date()}")
    print(f"Cache file: {CSV_FILE}")
