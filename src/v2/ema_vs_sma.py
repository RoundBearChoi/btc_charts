import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import get_btc_price_data_cryptocompare as btc_data


def draw(block_window):
    data_frame = btc_data.get_btc_price_data()

    plt.figure(figsize=(12, 6))

    # Calculate EMA21 and SMA50
    data_frame['EMA21'] = data_frame['close'].ewm(span=21, adjust=False).mean()
    data_frame['SMA50'] = data_frame['close'].rolling(window=50).mean()

    plt.style.use('fast')
    plt.grid(False)

    # Plot closing price, EMA21 and SMA50
    plt.plot(data_frame.index, data_frame['close'], label='Bitcoin Close Price', linewidth=0.55)
    plt.plot(data_frame.index, data_frame['EMA21'], label='21-Day EMA', linewidth=0.85)
    plt.plot(data_frame.index, data_frame['SMA50'], label='50-Day SMA', linewidth=0.85)

    plt.title('21-Day Exponential Moving Average vs 50-Day Simple Moving Average')
    plt.ylabel('Price (USD)')
    plt.legend()

    axis = plt.gca()
    axis.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    print('\nDrawing 21EMA vs 50SMA..')

    plt.show(block=block_window)


if __name__ == '__main__':   # ← Keeps standalone runs working
    draw(True)   # True = block until you close the plot window
