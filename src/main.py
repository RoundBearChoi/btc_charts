import logging
import os
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
    daily = download.download_daily_btc_data(8.5)
    # Log data
    print('')
    print('Download complete. Logging BTC data..')
    log_file_name = 'btc_data.log'
    logging.basicConfig(filename=log_file_name, level=logging.INFO, filemode='w')
    logging.info(daily.to_string())
    print('Log file saved at: ' + os.path.abspath(log_file_name))
    # Draw graphs
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
