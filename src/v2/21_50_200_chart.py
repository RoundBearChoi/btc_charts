import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pandas as pd
import get_btc_price_data_cryptocompare as btc_data

# ==================================================
# CONFIGURATION - Edit these values as needed
# ==================================================

# Chart behavior
LOG_SCALE = False
DAYS_BACK = 360*3
BLOCK_WINDOW = True # Set False if you want the script to continue immediately after plot

# Optional visual tweaks (advanced)
SHOW_GRID = True
FIGURE_SIZE = (14, 10)              # (width, height) in inches

# ==================================================
# END OF CONFIGURATION
# ==================================================

def draw(block_window=BLOCK_WINDOW, 
         log_scale=LOG_SCALE, 
         days_back=DAYS_BACK):
    """
    Enhanced Bitcoin chart: 21 EMA vs 50 SMA with 200 SMA long-term filter + Volume subplot.
    Now uses get_btc_price_data_cryptocompare for data consistency with other charts (like pi_bottom_top.py).
    All major settings are controlled from the CONFIG section at the top.
    """
    # === Load and prepare data ===
    data_frame = btc_data.get_btc_price_data()
    
    # === Optional recent-data filter (reliable slicing) ===
    if days_back is not None:
        data_frame = data_frame.sort_index()           # safety
        data_frame = data_frame.iloc[-days_back:]
    
    # === Calculate moving averages ===
    data_frame['EMA21'] = data_frame['close'].ewm(span=21, adjust=False).mean()
    data_frame['SMA50'] = data_frame['close'].rolling(window=50).mean()
    data_frame['SMA200'] = data_frame['close'].rolling(window=200).mean()

    # === Create figure with price + volume subplots ===
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=FIGURE_SIZE, 
                                   gridspec_kw={'height_ratios': [3, 1]},
                                   sharex=True)
    
    plt.style.use('fast')
    
    # === Price panel (top) ===
    ax1.plot(data_frame.index, data_frame['close'], 
             label='Bitcoin Close Price', linewidth=1.1, color='#F7931A')
    ax1.plot(data_frame.index, data_frame['EMA21'], 
             label='21-Day EMA', linewidth=1.3, color='#00FFAA')
    ax1.plot(data_frame.index, data_frame['SMA50'], 
             label='50-Day SMA', linewidth=1.3, color='#FF00FF')
    ax1.plot(data_frame.index, data_frame['SMA200'], 
             label='200-Day SMA (Long-term Filter)', 
             linewidth=1.6, linestyle='--', color='#4444FF')
    
    title = 'Bitcoin Price: 21 EMA vs 50 SMA with 200 SMA Filter'
    if log_scale:
        ax1.set_yscale('log')
        title += ' (Log Scale)'
    if days_back:
        title += f' — Last {days_back} days'
    
    ax1.set_title(title, fontsize=14, pad=20)
    ax1.set_ylabel('Price (USD)', fontsize=12)
    ax1.legend(loc='upper left', fontsize=10)
    
    if SHOW_GRID:
        ax1.grid(True, alpha=0.3)
    
    # Y-axis formatting
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'${int(x):,}'))
    
    # === Volume panel (bottom) ===
    ax2.bar(data_frame.index, data_frame['volumeto'], 
            width=0.9, color='#1E90FF', alpha=0.75, label='USD Volume')
    
    ax2.set_ylabel('Volume (USD)', fontsize=12)
    if SHOW_GRID:
        ax2.grid(True, alpha=0.3)
    
    # Smart volume formatter
    def volume_formatter(x, pos):
        if x >= 1e9:
            return f'${x/1e9:.1f}B'
        elif x >= 1e6:
            return f'${x/1e6:.0f}M'
        else:
            return f'${x:,.0f}'
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(volume_formatter))
    
    # === X-axis date formatting ===
    ax2.xaxis.set_major_locator(mdates.YearLocator())
    ax2.xaxis.set_minor_locator(mdates.MonthLocator())
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=0)
    plt.xlabel('Date')
    
    plt.tight_layout()
    
    print(f'\nDrawing BTC 21/50/200 + Volume chart '
          f'(log_scale={log_scale}, days_back={days_back})...')
    plt.show(block=block_window)


if __name__ == '__main__':
    draw()
