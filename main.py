import cryptocompare
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import logging
import pandas
import numpy
import os
import math

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from matplotlib.colors import LinearSegmentedColormap
from pi_top import draw_pi_top
from pi_bottom import draw_pi_bottom
from moving_average_weeks import draw_moving_average_weeks


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


def draw_21ema_vs_50sma(data_frame, block_window):
    plt.figure(figsize=(12, 6))  # A new window

    # Calculate EMA21 and SMA50
    data_frame['EMA21'] = data_frame['close'].ewm(span=21, adjust=False).mean()
    data_frame['SMA50'] = data_frame['close'].rolling(window=50).mean()

    plt.style.use('fast')
    plt.grid(False)

    # Plot closing price, EMA21 and SMA50
    plt.plot(data_frame.index, data_frame['close'], label='Bitcoin Close Price', linewidth=0.55)
    plt.plot(data_frame.index, data_frame['EMA21'], label='21 Day EMA', linewidth=0.85)
    plt.plot(data_frame.index, data_frame['SMA50'], label='50 Day SMA', linewidth=0.85)

    plt.title('21-Day Exponential Moving Average vs 50-Day Simple Moving Average')
    plt.ylabel('Price (USD)')
    plt.legend()

    axis = plt.gca()
    axis.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    print('Drawing 21EMA vs 50SMA..')

    plt.show(block=block_window)


def draw_rsi_vs_halving(data_frame, block_window):
    plt.figure(figsize=(12, 6))  # A new window

    plt.style.use('fast')
    plt.grid(False)

    data_frame = data_frame.resample('ME').last().asfreq('ME')

    # Calculate the RSI
    delta = data_frame['close'].diff()
    up = delta.clip(lower=0)
    down = -1*delta.clip(upper=0)
    ema_up = up.ewm(com=13, adjust=False).mean()
    ema_down = down.ewm(com=13, adjust=False).mean()
    rs = ema_up/ema_down

    data_frame['RSI'] = 100 - (100/(1 + rs))

    # 2028-04-17 is next predicted date
    halving_dates = ['2012-11-28', '2016-07-09', '2020-05-11', '2024-04-19', '2028-04-17']
    halving_dates = pandas.to_datetime(halving_dates)
    halving_dates = pandas.DatetimeIndex(halving_dates)

    # plot RSI
    norm = plt.Normalize(0, 50)

    for i in numpy.arange(1, len(data_frame)):
        x_values = data_frame.index[i - 1:i + 1]
        y_values = data_frame['RSI'][i - 1:i + 1]

        months_left = None

        for halving_date in halving_dates:
            if x_values[1] < halving_date:
                diff = relativedelta(halving_date, x_values[0])
                months_left = diff.years * 12 + diff.months
                break

        cmap = LinearSegmentedColormap.from_list('my_cmap', ['lightgreen', 'red'])
        color_value = cmap(norm(months_left))

        plt.plot(x_values, y_values, color=color_value)

    plt.title('Monthly RSI vs Next Halving')

    print('Drawing Monthly RSI vs Next Halving..')

    plt.show(block=block_window)


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
