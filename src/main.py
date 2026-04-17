import logging
import os
import pandas as pd  # <-- Added for reliable CSV load/save

import download_btc_data as download
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

    # === Data caching logic ===
    data_file = 'btc_data.csv'      # Primary cache (reliable)
    log_file_name = 'btc_data.log'  # Human-readable log (kept for compatibility)

    daily = None
    use_existing = False

    if os.path.exists(data_file):
        # Prompt the user exactly as requested
        choice = input(f"Existing BTC data cache found ('{data_file}'). "
                       "Use existing data? (y/n): ").strip().lower()
        use_existing = choice in ('y', 'yes', '')
        
        if use_existing:
            try:
                print("Loading data from cache...")
                daily = pd.read_csv(data_file, index_col=0, parse_dates=True)
                print(f"✅ Loaded {len(daily):,} rows from cache (latest date: {daily.index.max().date()})")
            except Exception as e:
                print(f"⚠️  Could not read cache ({e}). Will download fresh data instead.")
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

    # === Original logging (unchanged behavior) ===
    print('')
    print('Logging BTC data..')
    logging.basicConfig(filename=log_file_name, level=logging.INFO, filemode='w')
    logging.info(daily.to_string())
    print('Log file saved at: ' + os.path.abspath(log_file_name))

    # === Draw graphs (unchanged) ===
    print('')
    pi_top.draw(daily, False)
    pi_bottom.draw(daily, False)
    moving_average_weeks.draw(daily, 140, False)
    sma_vs_sma.draw(daily, False)
    ema_vs_sma.draw(daily, False)
    rsi_vs_halving.draw(daily, False)
    ema_rsi.draw(daily, False)
    m2_btc.draw(daily, True)


if __name__ == '__main__':
    run()
