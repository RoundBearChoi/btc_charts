import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def draw_moving_average_weeks(data_frame, weeks, block_window):
    plt.figure(figsize=(12, 6))  # A new window

    plt.style.use('fast')
    plt.grid(False)

    data_frame['moving_avg'] = data_frame['close'].rolling(window=7 * weeks).mean()

    plt.plot(data_frame['close'], label='Bitcoin Price', linewidth=1)
    plt.plot(data_frame['moving_avg'], label=f'{weeks}-Week Moving Average', linewidth=1)

    axis = plt.gca()
    axis.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    plt.title('Moving Average')
    plt.ylabel('Price (USD)')
    plt.legend()

    print('Drawing Weeks Moving Average..')

    plt.show(block=block_window)
