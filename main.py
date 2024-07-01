import cryptocompare
import logging
import pandas
import os
import math

from datetime import date, timedelta
from pi_top import draw_pi_top
from pi_bottom import draw_pi_bottom
from moving_average_weeks import draw_moving_average_weeks
from ema_vs_sma import draw_21ema_vs_50sma
from rsi_vs_halving import draw_rsi_vs_halving


def download_daily_btc_data(total_years):
    total_days = math.ceil(total_years * 365)
    today = date.today()
    num_downloads = total_days // 2000
    days_per_download = 2000
    remaining_days = total_days % 2000

    print('Downloading ' + str(total_days) + ' days worth of data from cryptocompare..')
    print('(' + str(total_years) + ' years)')

    data = []

    for i in range(num_downloads):
        download_date = today - timedelta(days=i * days_per_download)
        data_part = cryptocompare.get_historical_price_day(
            'BTC', currency='USD', limit=2000, toTs=download_date)
        data += data_part

    # Download remaining days
    if remaining_days > 0:
        download_date = today - timedelta(days=num_downloads * days_per_download)
        data_part = cryptocompare.get_historical_price_day(
            'BTC', currency='USD', limit=remaining_days, toTs=download_date)
        data += data_part

    df = pandas.DataFrame(data)
    df['time'] = pandas.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True, drop=False)

    # Resample to daily
    df = df.resample('D').last().asfreq('D')

    return df


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
