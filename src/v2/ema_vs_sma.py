import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.widgets import Slider

import get_btc_price_data_cryptocompare as btc_data


# ==================== CONFIGURATION SECTION ====================
# Adjust these values to change slider ranges and defaults.
# You can edit them anytime—changes take effect on the next run.

EMA_MIN   = 5      # Minimum EMA period
EMA_MAX   = 200    # Maximum EMA period
EMA_INIT  = 21     # Starting EMA value (original default)

SMA_MIN   = 10     # Minimum SMA period
SMA_MAX   = 300    # Maximum SMA period (SMA often uses longer windows)
SMA_INIT  = 50     # Starting SMA value (original default)
# ============================================================


def draw(block_window):
    data_frame = btc_data.get_btc_price_data()

    # Keep a clean reference to the close prices (used for all recalcs)
    close = data_frame['close']
    index = data_frame.index

    # Create figure and main axis (slightly taller to fit sliders nicely)
    fig, ax = plt.subplots(figsize=(12, 7))
    
    plt.style.use('fast')
    ax.grid(False)

    # Initial calculations (same as original)
    ema = close.ewm(span=EMA_INIT, adjust=False).mean()
    sma = close.rolling(window=SMA_INIT).mean()

    # Plot lines (save references so we can update them later)
    line_close, = ax.plot(index, close, 
                          label='Bitcoin Close Price', 
                          linewidth=0.55)
    line_ema, = ax.plot(index, ema, 
                        label=f'{EMA_INIT}-Day EMA', 
                        linewidth=0.85)
    line_sma, = ax.plot(index, sma, 
                        label=f'{SMA_INIT}-Day SMA', 
                        linewidth=0.85)

    # Title, labels, and formatting (preserves original look)
    ax.set_title(f'{EMA_INIT}-Day Exponential Moving Average vs {SMA_INIT}-Day Simple Moving Average')
    ax.set_ylabel('Price (USD)')
    ax.legend(loc='upper left')

    axis = ax
    axis.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # Make room at the bottom for the two sliders
    plt.subplots_adjust(bottom=0.25)

    # ====================== SLIDER AXES ======================
    # EMA slider
    ax_ema = plt.axes([0.1, 0.13, 0.65, 0.03])
    slider_ema = Slider(
        ax=ax_ema,
        label=f'EMA Period ({EMA_MIN}-{EMA_MAX})',
        valmin=EMA_MIN,
        valmax=EMA_MAX,
        valinit=EMA_INIT,
        valstep=1,           # force integer steps
        valfmt='%d'
    )

    # SMA slider
    ax_sma = plt.axes([0.1, 0.08, 0.65, 0.03])
    slider_sma = Slider(
        ax=ax_sma,
        label=f'SMA Period ({SMA_MIN}-{SMA_MAX})',
        valmin=SMA_MIN,
        valmax=SMA_MAX,
        valinit=SMA_INIT,
        valstep=1,
        valfmt='%d'
    )

    # ====================== UPDATE CALLBACK ======================
    def update(val):
        ema_p = int(slider_ema.val)
        sma_p = int(slider_sma.val)

        # Recalculate both moving averages from raw close prices
        new_ema = close.ewm(span=ema_p, adjust=False).mean()
        new_sma = close.rolling(window=sma_p).mean()

        # Update the line data
        line_ema.set_ydata(new_ema)
        line_sma.set_ydata(new_sma)

        # Update legend labels and title
        line_ema.set_label(f'{ema_p}-Day EMA')
        line_sma.set_label(f'{sma_p}-Day SMA')
        ax.set_title(f'{ema_p}-Day Exponential Moving Average vs {sma_p}-Day Simple Moving Average')

        # Refresh legend and redraw the canvas
        ax.legend(loc='upper left')
        fig.canvas.draw_idle()

    # Connect sliders to the update function
    slider_ema.on_changed(update)
    slider_sma.on_changed(update)

    print('\nInteractive plot with EMA and SMA sliders ready!')
    print('Drag the sliders below the chart to change periods in real time.\n')

    plt.show(block=block_window)


if __name__ == '__main__':   # ← Keeps standalone runs working
    draw(True)   # True = block until you close the plot window
