import cryptocompare
import matplotlib.pyplot as plotter
import matplotlib.ticker as ticker
import numpy as np
import logging
import pandas
import os
import math

from datetime import date, timedelta


def download_daily_btc_data():
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

    df = pandas.DataFrame(data)
    df['time'] = pandas.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True, drop=False)

    # Resampled to daily by default
    df = df.resample('D').last().asfreq('D')

    return df


def draw_pi_top_chart(data_frame):
    slow = 360
    quick = math.floor(slow / 3.14159)
    data_frame[str(slow) + '_MA'] = data_frame['close'].rolling(window=slow).mean() * 2
    data_frame[str(quick) + '_MA'] = data_frame['close'].rolling(window=quick).mean()

    plotter.style.use('ggplot')
    plotter.figure(figsize=(14, 7))
    plotter.plot(data_frame[str(slow) + '_MA'], label=str(slow) + '-day MA', linewidth=0.8)
    plotter.plot(data_frame[str(quick) + '_MA'], label=str(quick) + '-day MA', linewidth=0.8)
    plotter.plot(data_frame['close'], label='Bitcoin', linewidth=0.4)
    plotter.xlabel('Date')
    plotter.ylabel('Price (USD)')
    plotter.grid(False)
    plotter.legend()

    ax = plotter.gca()
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    plotter.show()


def run():
    print('')
    print('Hi.')
    print('')

    daily = download_daily_btc_data()

    # Log data
    print('')
    print('Download complete. Logging BTC data..')
    log_file_name = 'btc_data.log'
    logging.basicConfig(filename=log_file_name, level=logging.INFO, filemode='w')
    logging.info(daily.to_string())
    print('Log file saved at: ' + os.path.abspath(log_file_name))

    # Draw
    draw_pi_top_chart(daily)


if __name__ == '__main__':
    run()
