import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def draw(data_frame, block_window):
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

    print('Drawing Pi Bottom..')

    plt.show(block=block_window)
