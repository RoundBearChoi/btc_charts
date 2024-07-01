import cryptocompare
import matplotlib.pyplot as plt
import numpy as np
import logging
import pandas as pd
import os

from matplotlib.colors import LinearSegmentedColormap
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta


def download_btc_data():
    today = date.today()
    num_downloads = 3
    days_per_download = 1400

    print('Downloading ' + str(1400) + ' days worth of data ' + str(num_downloads) + ' times..')
    total_days = num_downloads * days_per_download
    total_years = round(total_days / 365, 2)
    print('Total of ' + str(total_days) + ' days (' + str(total_years) + ' years)')

    data = []

    for i in range(num_downloads):
        download_date = today - timedelta(days=i * days_per_download)
        data_part = cryptocompare.get_historical_price_day('BTC', currency='USD', limit=2000, toTs=download_date)
        data += data_part

    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True, drop=False)
    df = df.resample('ME').last().asfreq('ME')

    return df


def run():
    print('')
    print('Hi.')
    print('')

    data = download_btc_data()

    # Log data
    print('')
    print('Download complete. Logging BTC data..')
    log_file = 'btc_data.log'
    logging.basicConfig(filename=log_file, level=logging.INFO, filemode='w')
    logging.info(data.to_string())
    print('Log file saved at: ' + os.path.abspath(log_file))


if __name__ == '__main__':
    run()
