import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.widgets import Slider
from btc_data_loader import load_btc_data   # ← shared loader (unchanged)


# ==================== CONFIG SECTION ====================
# ←←← EDIT THESE VALUES TO CUSTOMIZE THE SLIDER ←←←
# All changes here take effect immediately on the next run.

MIN_DAYS       = 3      # Minimum value the slider can reach (leftmost position)
MAX_DAYS       = 160*7    # Maximum value the slider can reach (rightmost position)

# ── This is the one you asked about ──
# DEFAULT_DAYS sets the INITIAL POSITION of the small red indicator line/handle
# on the slider bar when the chart first opens. It also becomes the starting
# moving-average period.
DEFAULT_DAYS   = 360     # Starting value (red line starts here)

# Optional visual / behavior tweaks (rarely need changing)
FIGURE_SIZE    = (12, 8)   # Width × Height in inches (taller = more room for slider)
BLOCK_WINDOW   = True      # True = script waits until you close the plot window
# ======================================================


def draw(initial_days=DEFAULT_DAYS,
         min_days=MIN_DAYS,
         max_days=MAX_DAYS,
         block_window=BLOCK_WINDOW):
    """
    Draw Bitcoin price chart with real-time adjustable moving average.
    All slider settings come from the CONFIG SECTION above (or can be overridden).
    """

    # === Load data using the shared loader (no duplication) ===
    data_frame = load_btc_data()

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

    # === Real-time Slider (now with even clearer config mapping) ===
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
    print(f'Drawing interactive Moving Average (range: {min_days}-{max_days} days)')
    print(f'→ Red indicator line starts at {initial_days} days (see CONFIG SECTION)')
    print('→ Drag the slider below the chart to adjust in real time.')

    plt.show(block=block_window)


if __name__ == '__main__':
    draw()   # Uses ALL values from the CONFIG SECTION above
