import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def draw(data_frame, block_window):
    plt.figure(figsize=(12, 6))  # A new window

    data_frame['SMA111'] = data_frame['close'].rolling(window=111).mean()
    data_frame['SMA50'] = data_frame['close'].rolling(window=50).mean()

    plt.style.use('fast')
    plt.grid(False)

    plt.plot(data_frame.index, data_frame['close'], label='Bitcoin Close Price', linewidth=0.55)
    plt.plot(data_frame.index, data_frame['SMA111'], label='111-Day SMA', linewidth=0.85)
    plt.plot(data_frame.index, data_frame['SMA50'], label='50-Day SMA', linewidth=0.85)

    plt.title('111-Day Simple Moving Average vs 50-Day Simple Moving Average')
    plt.ylabel('Price (USD)')
    plt.legend()

    axis = plt.gca()
    axis.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    print('Drawing 111SMA vs 50SMA..')

    plt.show(block=block_window)
