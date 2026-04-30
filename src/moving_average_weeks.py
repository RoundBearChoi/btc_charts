import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import get_btc_price_data_cryptocompare as btc_data


def draw(weeks, block_window):
    # === Load data using the new unified data module ===
    # (No more dependency on deleted btc_data_loader.py)
    data_frame = btc_data.get_btc_price_data()

    # === Original plotting logic (100% unchanged) ===
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

    print('\nDrawing Weeks Moving Average..')

    plt.show(block=block_window)


if __name__ == '__main__':   # ← Keeps standalone runs working
    draw(140, True)   # Default to 140 weeks (same value main.py currently uses)
