import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pandas as pd
import get_price_data_cryptocompare as price_data

# ==================================================
# CONFIGURATION - Edit these values as needed
# ==================================================

# Chart behavior
LOG_SCALE = False
DAYS_BACK = 360*3
BLOCK_WINDOW = True # Set False if you want the script to continue immediately after plot

# Optional visual tweaks (advanced)
SHOW_GRID = True
FIGURE_SIZE = (14, 10) # (width, height) in inches

# === Line colors and widths  ===
CLOSE_COLOR = '#9EB3DB'
CLOSE_WIDTH = 0.9

EMA21_COLOR = '#E15FC3' # shorter term
EMA21_WIDTH = 1.3

SMA50_COLOR = '#00D118' # longer term
SMA50_WIDTH = 1.3

SMA200_COLOR = '#C80C01' # really long term
SMA200_WIDTH = 1.6

VOLUME_COLOR = '#8F8C57'
VOLUME_ALPHA = 0.75
VOLUME_BAR_WIDTH = 0.9

# === Volume SMA ===
VOLUME_SMA_DAYS = 15
VOLUME_SMA_COLOR = '#263549'
VOLUME_SMA_WIDTH = 1.5

# ==================================================
# END OF CONFIGURATION
# ==================================================

def draw(block_window=BLOCK_WINDOW, 
         log_scale=LOG_SCALE, 
         days_back=DAYS_BACK):
    """
    Enhanced Bitcoin chart: 21 EMA vs 50 SMA with 200 SMA long-term filter + 
    Volume subplot with configurable SMA overlay.
    Uses get_price_data_cryptocompare for data consistency.
    """
    # === Load and prepare data ===
    data_frame = price_data.get_btc_price_data()
    
    # === Optional recent-data filter ===
    if days_back is not None:
        data_frame = data_frame.sort_index()
        data_frame = data_frame.iloc[-days_back:]
    
    # === Calculate moving averages ===
    data_frame['EMA21'] = data_frame['close'].ewm(span=21, adjust=False).mean()
    data_frame['SMA50'] = data_frame['close'].rolling(window=50).mean()
    data_frame['SMA200'] = data_frame['close'].rolling(window=200).mean()
    
    # === Volume SMA (optional) ===
    if VOLUME_SMA_DAYS > 0:
        data_frame['VOLUME_SMA'] = data_frame['volumeto'].rolling(window=VOLUME_SMA_DAYS).mean()

    # === Create figure with price + volume subplots ===
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=FIGURE_SIZE, 
                                   gridspec_kw={'height_ratios': [3, 1]},
                                   sharex=True)
    
    plt.style.use('fast')
    
    # === Price panel (top) ===
    ax1.plot(data_frame.index, data_frame['close'], 
             label='Bitcoin Close Price', linewidth=CLOSE_WIDTH, color=CLOSE_COLOR)
    ax1.plot(data_frame.index, data_frame['EMA21'], 
             label='21-Day EMA', linewidth=EMA21_WIDTH, color=EMA21_COLOR)
    ax1.plot(data_frame.index, data_frame['SMA50'], 
             label='50-Day SMA', linewidth=SMA50_WIDTH, color=SMA50_COLOR)
    ax1.plot(data_frame.index, data_frame['SMA200'], 
             label='200-Day SMA (Long-term Filter)', 
             linewidth=SMA200_WIDTH, linestyle='--', color=SMA200_COLOR)
    
    title = 'Bitcoin Price: 21 EMA vs 50 SMA with 200 SMA Filter + Volume SMA'
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
            width=VOLUME_BAR_WIDTH, color=VOLUME_COLOR, alpha=VOLUME_ALPHA, label='USD Volume')
    
    # Volume SMA line (if enabled)
    if VOLUME_SMA_DAYS > 0 and 'VOLUME_SMA' in data_frame.columns:
        ax2.plot(data_frame.index, data_frame['VOLUME_SMA'], 
                 label=f'{VOLUME_SMA_DAYS}-Day Volume SMA', 
                 linewidth=VOLUME_SMA_WIDTH, color=VOLUME_SMA_COLOR)
    
    ax2.set_ylabel('Volume (USD)', fontsize=12)
    ax2.legend(loc='upper left', fontsize=10)
    
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
    
    print(f'\nDrawing BTC 21/50/200 + Volume + {VOLUME_SMA_DAYS}-day SMA chart '
          f'(log_scale={log_scale}, days_back={days_back})...')
    plt.show(block=block_window)


if __name__ == '__main__':
    draw()
