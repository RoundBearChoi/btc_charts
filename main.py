import logging
import os

from download_btc_data import download_daily_btc_data
from pi_top import draw_pi_top
from pi_bottom import draw_pi_bottom
from moving_average_weeks import draw_moving_average_weeks
from ema_vs_sma import draw_21ema_vs_50sma
from rsi_vs_halving import draw_rsi_vs_halving


def run():
    print('')
    print('Hi.')
    print('')

    daily = download_daily_btc_data(8.5)

    # Log data
    print('')
    print('Download complete. Logging BTC data..')
    log_file_name = 'btc_data.log'
    logging.basicConfig(filename=log_file_name, level=logging.INFO, filemode='w')
    logging.info(daily.to_string())
    print('Log file saved at: ' + os.path.abspath(log_file_name))

    # Draw graphs
    print('')
    draw_pi_top(daily, False)
    draw_pi_bottom(daily, False)
    draw_moving_average_weeks(daily, 140, False)
    draw_21ema_vs_50sma(daily, False)
    draw_rsi_vs_halving(daily, True)


if __name__ == '__main__':
    run()
