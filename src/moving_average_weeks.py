import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from btc_data_loader import load_btc_data   # ← NEW


def draw(weeks, block_window):
    # === Load data using the shared loader (no more duplication) ===
    data_frame = load_btc_data()

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

    print('Drawing Weeks Moving Average..')

    plt.show(block=block_window)


if __name__ == '__main__':   # ← Added for standalone runs
    draw(140, True)   # Default to 140 weeks (same value main.py currently uses)
