import logging
import os

import get_btc_price_data_cryptocompare as btc_data

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

    # Get BTC price data (cache/download logic is now fully inside the dedicated module)
    print("Getting BTC price data...")
    daily = btc_data.get_btc_price_data()

    # === Original logging (unchanged) ===
    print('')
    print('Logging BTC data..')
    log_file_name = 'btc_data.log'
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
