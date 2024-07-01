import cryptocompare
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import logging
import pandas
import os
import math

from datetime import date, timedelta


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


def draw_pi_top(data_frame, block_window):
    plt.figure(figsize=(12, 6))  # A new window

    plt.style.use('fast')
    plt.grid(False)

    slow = 365
    quick = math.floor(slow / 3.14159)
    data_frame[str(slow) + '_MA * 2'] = data_frame['close'].rolling(window=slow).mean() * 2
    data_frame[str(quick) + '_MA'] = data_frame['close'].rolling(window=quick).mean()

    plt.plot(data_frame['close'], label='BTC Price', linewidth=0.4)
    plt.plot(data_frame[str(slow) + '_MA * 2'], label=str(slow) + '-day MA * 2', linewidth=1)
    plt.plot(data_frame[str(quick) + '_MA'], label=str(quick) + '-day MA', linewidth=1)

    axis = plt.gca()
    axis.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    plt.title('Pi Top')
    plt.ylabel('Price (USD)')
    plt.legend()

    print('')
    print('Drawing Pi Top..')

    plt.show(block=block_window)


def draw_pi_bottom(data_frame, block_window):
    plt.figure(figsize=(12, 6))  # A new window

    plt.style.use('fast')
    plt.grid(False)

    # Calculate the 471-day Moving Average (MA) and multiply by 0.475
    data_frame['471_MA'] = data_frame['close'].rolling(window=471).mean() * 0.475

    # Calculate the 150-day Exponential Moving Average (EMA) and multiply by 0.475
    data_frame['150_EMA'] = data_frame['close'].ewm(span=150, adjust=False).mean() * 0.475

    plt.plot(data_frame.index, data_frame['close'], '-', linewidth=1)
    plt.plot(data_frame.index, data_frame['471_MA'], '-', linewidth=1)
    plt.plot(data_frame.index, data_frame['150_EMA'], '-', linewidth=1)

    axis = plt.gca()
    axis.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.title('Pi Bottom')
    plt.ylabel('Price (USD)')
    plt.legend(['BTC Price', '471 MA * 0.475', '150 EMA * 0.475'])

    print('')
    print('Drawing Pi Bottom..')

    plt.show(block=block_window)


def draw_weeks_moving_average(data_frame, weeks, block_window):
    plt.figure(figsize=(12, 6))  # A new window

    plt.style.use('fast')
    plt.grid(False)

    data_frame['moving_avg'] = data_frame['close'].rolling(window=7 * weeks).mean()

    plt.plot(data_frame['close'], label='Bitcoin Price', linewidth=1)
    plt.plot(data_frame['moving_avg'], label=f'{weeks}-Week Moving Average', linewidth=1)
    plt.title('Moving Average')

    axis = plt.gca()
    axis.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    plt.ylabel('Price (USD)')
    plt.legend()

    print('')
    print('Drawing Weeks Moving Average..')

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
    draw_pi_top(daily, False)
    draw_pi_bottom(daily, False)
    draw_weeks_moving_average(daily, 140, True)


if __name__ == '__main__':
    run()
