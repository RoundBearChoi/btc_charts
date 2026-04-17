import logging
import os
import pandas as pd  # still needed for the download + save path

import download_btc_data as download
from btc_data_loader import load_btc_data   # ← NEW

import pi_top
import pi_bottom
import moving_average_weeks
import ema_vs_sma
import sma_vs_sma
import rsi_vs_halving
import fifty_week_ema_vs_weekly_rsi as ema_rsi
import usd_m2_vs_btc as m2_btc


def run():
    print('')
    print('Hi.')

    # === Data caching logic (unchanged user experience) ===
    data_file = 'btc_data.csv'
    log_file_name = 'btc_data.log'

    daily = None
    use_existing = False

    if os.path.exists(data_file):
        choice = input(f"Existing BTC data cache found ('{data_file}'). "
                       "Use existing data? (y/n): ").strip().lower()
        use_existing = choice in ('y', 'yes', '')

        if use_existing:
            try:
                daily = load_btc_data()   # ← now uses the shared loader
            except Exception as e:
                print(f"⚠️  {e}\nWill download fresh data instead.")
                daily = None
                use_existing = False

    # If no cache or user chose fresh download
    if daily is None:
        print("Downloading fresh BTC data...")
        daily = download.download_full_df()
        print(f"✅ Downloaded {len(daily):,} rows (latest date: {daily.index.max().date()})")
        
        # Save cache for next time
        daily.to_csv(data_file)
        print(f"Data cached to: {os.path.abspath(data_file)}")

    # === Original logging (unchanged) ===
    print('')
    print('Logging BTC data..')
    logging.basicConfig(filename=log_file_name, level=logging.INFO, filemode='w')
    logging.info(daily.to_string())
    print('Log file saved at: ' + os.path.abspath(log_file_name))

    # === Draw graphs (still passing data for now) ===
    print('')
    pi_top.draw(False)
    pi_bottom.draw(False)
    moving_average_weeks.draw(140, False)
    sma_vs_sma.draw(False)
    ema_vs_sma.draw(False)
    rsi_vs_halving.draw(False)
    ema_rsi.draw(False)
    m2_btc.draw(True)


if __name__ == '__main__':
    run()
