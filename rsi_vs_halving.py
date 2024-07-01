import matplotlib.pyplot as plt
import pandas
import numpy

from dateutil.relativedelta import relativedelta
from matplotlib.colors import LinearSegmentedColormap

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
