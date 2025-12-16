import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import requests
from pandas.tseries.offsets import MonthEnd

# downloaded usd m2 data
url = "https://www.federalreserve.gov/datadownload/Output.aspx?rel=H6&series=798e2796917702a5f8423426ba7e6b42&lastobs=&from=&to=&filetype=csv&label=include&layout=seriescolumn"
filename = "FRB_H6.csv"

response = requests.get(url)

if response.status_code == 200:
    with open(filename, 'wb') as f:
        f.write(response.content)
    # print(f"csv successfully downloaded and saved as '{filename}'")
# else:
    # print(f"failed to download usd m2. status code: {response.status_code}")

def draw(data_frame, block_window):
    # Resample daily BTC data to monthly (using last close of the month)
    monthly_btc = data_frame.resample('ME').agg({'close': 'last'})

    # Load US M2 from local CSV (monthly, billions USD) - skipping metadata rows
    us_m2 = pd.read_csv('FRB_H6.csv', skiprows=5, index_col='Time Period', parse_dates=True)['M2.M']

    # Shift US M2 index to month-end to align with BTC monthly data
    us_m2.index = us_m2.index + MonthEnd(0)

    # Combine with BTC data and drop NaNs (for alignment)
    df = pd.DataFrame({'BTC': monthly_btc['close'], 'US_M2': us_m2})
    df = df.dropna()

    # Create the plot with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})
    plt.style.use('fast')

    # Top subplot: BTC price
    ax1.plot(df.index, df['BTC'], label='BTC Monthly Close', color='green', linewidth=0.55)
    ax1.set_title('BTC Price vs US M2')
    ax1.set_ylabel('Price (USD)')
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax1.legend(loc='upper left')
    ax1.grid(False)

    # Bottom subplot: US M2
    ax2.plot(df.index, df['US_M2'], label='US M2 (Billions USD)', color='blue', linewidth=0.85)
    ax2.set_ylabel('M2 (Billions USD)')
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax2.legend(loc='upper left')
    ax2.grid(False)

    # Adjust layout to prevent overlap
    plt.tight_layout()
    print('Drawing US M2 (bottom) vs BTC Price (top)..')
    plt.show(block=block_window)
