import cryptocompare
import pandas
import math
import datetime as dt


def download_daily_btc_data(total_years):
    total_days = math.ceil(total_years * 365)
    today = dt.date.today()
    num_downloads = total_days // 2000
    days_per_download = 2000
    remaining_days = total_days % 2000

    print('')
    print('Downloading ' + str(total_days) + ' days worth of data from cryptocompare..')
    print('(' + str(total_years) + ' years)')

    data = []

    for i in range(num_downloads):
        download_date = today - dt.timedelta(days=i * days_per_download)
        data_part = cryptocompare.get_historical_price_day(
            'BTC', currency='USD', limit=2000, toTs=download_date)
        data += data_part

    # Download remaining days
    if remaining_days > 0:
        download_date = today - dt.timedelta(days=num_downloads * days_per_download)
        data_part = cryptocompare.get_historical_price_day(
            'BTC', currency='USD', limit=remaining_days, toTs=download_date)
        data += data_part

    df = pandas.DataFrame(data)
    df['time'] = pandas.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True, drop=False)

    # Resample to daily
    df = df.resample('D').last().asfreq('D')

    return df
