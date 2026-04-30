import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import get_btc_price_data_cryptocompare as btc_data


def draw(block_window):
    # === Load data using the new unified data module ===
    # (No more dependency on deleted btc_data_loader.py)
    data_frame = btc_data.get_btc_price_data()

    # === Pi Cycle Bottom Indicator (Correct & Polished Version) ===
    # This is the widely used modern variant of the Pi Bottom
    # Signal: 150-day EMA crosses BELOW 471-day SMA × 0.745
    # (Matches the majority of TradingView scripts and recent analyses)

    PI_FACTOR = 0.745   # Most common / accurate scaling factor for this cycle

    # Calculate the lines
    data_frame['471_MA'] = data_frame['close'].rolling(window=471).mean() * PI_FACTOR
    data_frame['150_EMA'] = data_frame['close'].ewm(span=150, adjust=False).mean()

    # === Plotting ===
    plt.figure(figsize=(12, 6))

    plt.style.use('fast')
    plt.grid(False)

    plt.plot(data_frame.index, data_frame['close'], '-', linewidth=1, label='BTC Price')
    plt.plot(data_frame.index, data_frame['471_MA'], '-', linewidth=1, label=f'471 SMA × {PI_FACTOR}')
    plt.plot(data_frame.index, data_frame['150_EMA'], '-', linewidth=1, label='150 EMA')

    # Format Y-axis with commas
    axis = plt.gca()
    axis.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    plt.title('Pi Cycle Bottom Indicator')
    plt.ylabel('Price (USD)')
    plt.legend()

    print('\nDrawing Pi Cycle Bottom Indicator...')
    print(f'   → Using scaling factor: {PI_FACTOR}')
    print(f'   → Latest data point: {data_frame.index[-1].date()}')

    plt.show(block=block_window)


if __name__ == '__main__':   # ← Keeps standalone runs working
    draw(True)   # True = block until you close the plot window
