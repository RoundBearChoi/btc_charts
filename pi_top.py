
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math


def draw(data_frame, block_window):
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

    print('Drawing Pi Top..')

    plt.show(block=block_window)
