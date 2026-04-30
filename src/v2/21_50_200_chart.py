import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

import get_btc_price_data_cryptocompare as btc_data


def draw(block_window):
    # === Load data using the new unified data module ===
    # (No more dependency on deleted btc_data_loader.py)
    data_frame = btc_data.get_btc_price_data()

    # === Calculate moving averages (now with 200-day SMA) ===
    data_frame['EMA21'] = data_frame['close'].ewm(span=21, adjust=False).mean()
    data_frame['SMA50'] = data_frame['close'].rolling(window=50).mean()
    data_frame['SMA200'] = data_frame['close'].rolling(window=200).mean()   # ← NEW: long-term filter

    plt.figure(figsize=(12, 6))  # A new window

    plt.style.use('fast')
    plt.grid(False)

    # Plot closing price, EMA21, SMA50 and SMA200
    plt.plot(data_frame.index, data_frame['close'], label='Bitcoin Close Price', linewidth=0.55)
    plt.plot(data_frame.index, data_frame['EMA21'], label='21-Day EMA', linewidth=0.85)
    plt.plot(data_frame.index, data_frame['SMA50'], label='50-Day SMA', linewidth=0.85)
    plt.plot(data_frame.index, data_frame['SMA200'], 
             label='200-Day SMA (Long-term Filter)', linewidth=1.3, linestyle='--')

    plt.title('21-Day EMA vs 50-Day SMA with 200-Day SMA Long-Term Filter')
    plt.ylabel('Price (USD)')
    plt.legend()

    # Y-axis formatting (unchanged)
    axis = plt.gca()
    axis.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # === LONG-TERM REGIME FILTER (console feedback) ===
    latest = data_frame.iloc[-1]
    if pd.isna(latest['SMA200']):
        print("\n⚠️  Not enough historical data yet for 200-day SMA (need ~200 days)")
    elif latest['close'] > latest['SMA200']:
        print("\n✅ LONG-TERM BULLISH REGIME: Price is trading ABOVE 200-day SMA")
    else:
        print("\n⚠️  LONG-TERM BEARISH REGIME: Price is trading BELOW 200-day SMA")

    print('\nDrawing 21EMA vs 50SMA vs 200SMA..')

    plt.show(block=block_window)


if __name__ == '__main__':   # ← Keeps standalone runs working
    draw(True)   # True = block until you close the plot window
