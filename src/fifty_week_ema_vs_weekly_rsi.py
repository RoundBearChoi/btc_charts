'''
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def draw(data_frame, block_window):
    # Resample daily data to weekly (using last close of the week)
    weekly = data_frame.resample('W').agg({'close': 'last'})
    
    # Calculate 50-week EMA on weekly closes
    weekly['EMA50'] = weekly['close'].ewm(span=50, adjust=False).mean()
    
    # Calculate weekly RSI (14-period)
    delta = weekly['close'].diff()
    gain = delta.clip(lower=0).rolling(window=14).mean()
    loss = -delta.clip(upper=0).rolling(window=14).mean()
    rs = gain / loss
    weekly['RSI'] = 100 - (100 / (1 + rs))
    
    # Create the plot with dual axes
    fig, ax1 = plt.subplots(figsize=(12, 6))
    plt.style.use('fast')
    plt.grid(False)
    
    # Plot BTC price and 50-week EMA on the left axis
    ax1.plot(weekly.index, weekly['close'], label='BTC Weekly Close', color='green', linewidth=0.55)
    ax1.plot(weekly.index, weekly['EMA50'], label='50-Week EMA', color='blue', linewidth=0.85)
    ax1.set_title('50-Week EMA vs Weekly RSI vs BTC Price')
    ax1.set_ylabel('Price (USD)')
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    # Create a twin axis for RSI on the right
    ax2 = ax1.twinx()
    ax2.plot(weekly.index, weekly['RSI'], label='Weekly RSI (14)', color='orange', linewidth=0.85)
    ax2.set_ylabel('RSI')
    ax2.set_ylim(0, 100)
    
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    print('Drawing 50-Week EMA vs Weekly RSI..')
    plt.show(block=block_window)
    '''

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def draw(data_frame, block_window):
    # Resample daily data to weekly (using last close of the week)
    weekly = data_frame.resample('W').agg({'close': 'last'})

    # Calculate 50-week EMA on weekly closes
    weekly['EMA50'] = weekly['close'].ewm(span=50, adjust=False).mean()

    # Calculate weekly RSI (14-period)
    delta = weekly['close'].diff()
    gain = delta.clip(lower=0).rolling(window=14).mean()
    loss = -delta.clip(upper=0).rolling(window=14).mean()
    rs = gain / loss
    weekly['RSI'] = 100 - (100 / (1 + rs))

    # Create the plot with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})
    plt.style.use('fast')

    # Top subplot: BTC price and 50-week EMA
    ax1.plot(weekly.index, weekly['close'], label='BTC Weekly Close', color='green', linewidth=0.55)
    ax1.plot(weekly.index, weekly['EMA50'], label='50-Week EMA', color='blue', linewidth=0.85)
    ax1.set_title('50-Week EMA vs Weekly RSI vs BTC Price')
    ax1.set_ylabel('Price (USD)')
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax1.legend(loc='upper left')
    ax1.grid(False)

    # Bottom subplot: RSI
    ax2.plot(weekly.index, weekly['RSI'], label='Weekly RSI (14)', color='orange', linewidth=0.85)
    ax2.set_ylabel('RSI')
    ax2.set_ylim(0, 100)
    ax2.legend(loc='upper left')
    ax2.grid(False)

    # Adjust layout to prevent overlap
    plt.tight_layout()

    print('Drawing 50-Week EMA vs Weekly RSI (with RSI below)..')
    plt.show(block=block_window)
