import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.widgets import Slider
from get_btc_price_data_cryptocompare import get_btc_price_data   # ← now uses the cryptocompare data fetcher


# ==================== CONFIG SECTION ====================
MIN_DAYS       = 3      # Minimum value the slider can reach (leftmost position)
MAX_DAYS       = 200*7    # Maximum value the slider can reach (rightmost position)
DEFAULT_DAYS   = 360     # Starting value (red line starts here)

FIGURE_SIZE    = (12, 8)   # Width × Height in inches (taller = more room for slider)
BLOCK_WINDOW   = True      # True = script waits until you close the plot window
# ======================================================


def draw(initial_days=DEFAULT_DAYS,
         min_days=MIN_DAYS,
         max_days=MAX_DAYS,
         block_window=BLOCK_WINDOW):
    """
    Draw Bitcoin price chart with real-time adjustable moving average.
    Now uses get_btc_price_data() from get_btc_price_data_cryptocompare.py
    (automatically downloads + caches data if the CSV is missing).
    """

    # === Load data using the CryptoCompare fetcher (handles cache or download) ===
    data_frame = get_btc_price_data()

    # === Create figure and axis ===
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    plt.style.use('fast')
    plt.grid(False)

    # Plot Bitcoin price (unchanged)
    price_line, = ax.plot(data_frame['close'], label='Bitcoin Price', linewidth=1.2)

    # Initial moving average (starts at DEFAULT_DAYS)
    ma_series = data_frame['close'].rolling(window=initial_days).mean()
    ma_line, = ax.plot(ma_series,
                       label=f'{initial_days}-Day Moving Average',
                       linewidth=1.5,
                       color='orange')

    # Nice comma formatting for large USD values
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    plt.title('Bitcoin Price with Real-Time Adjustable Moving Average')
    plt.ylabel('Price (USD)')
    plt.xlabel('Time (data points)')
    plt.legend()

    # === Real-time Slider ===
    slider_ax = plt.axes([0.20, 0.02, 0.60, 0.03], facecolor='lightgray')
    days_slider = Slider(
        ax=slider_ax,
        label='Moving Average (days)',
        valmin=min_days,
        valmax=max_days,
        valinit=initial_days,        # ← This is what positions the red line at start
        valstep=1,
        valfmt='%d days'
    )

    # Update function called every time the slider moves
    def update(val):
        days = int(days_slider.val)
        # Recompute the moving average instantly
        ma_series = data_frame['close'].rolling(window=days).mean()
        ma_line.set_ydata(ma_series)
        ma_line.set_label(f'{days}-Day Moving Average')
        ax.legend()                  # refresh legend
        fig.canvas.draw_idle()       # efficient redraw

    days_slider.on_changed(update)

    # Friendly console output
    print(f'\nDrawing interactive Moving Average (range: {min_days}-{max_days} days)')

    plt.show(block=block_window)


if __name__ == '__main__':
    draw()   # Uses ALL values from the CONFIG SECTION above
