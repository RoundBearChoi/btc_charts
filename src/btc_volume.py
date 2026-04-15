import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_btc_hourly_volume_cryptocompare(hours=504, api_key=None):
    """
    Fetch hourly BTC volume for the past ~3 weeks.
    Returns timezone-aware DataFrame (UTC + KST).
    """
    url = "https://min-api.cryptocompare.com/data/v2/histohour"
    
    params = {
        'fsym': 'BTC',
        'tsym': 'USD',
        'limit': hours + 26,   # small buffer to ensure full coverage
    }
    if api_key:
        params['api_key'] = api_key
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data.get('Response') != 'Success':
        raise ValueError(f"API Error: {data.get('Message', 'Unknown error')}")
    
    df = pd.DataFrame(data['Data']['Data'])
    
    # === TIMEZONE-AWARE PROCESSING ===
    df['timestamp_utc'] = pd.to_datetime(df['time'], unit='s', utc=True)
    df['datetime_kst'] = df['timestamp_utc'].dt.tz_convert('Asia/Seoul')
    
    # Clean columns for readability
    df['date_kst'] = df['datetime_kst'].dt.strftime('%Y-%m-%d')
    df['hour_kst'] = df['datetime_kst'].dt.strftime('%H:%M')
    df['datetime_kst_str'] = df['datetime_kst'].dt.strftime('%Y-%m-%d %H:%M KST')
    
    # Rename volumes
    df = df[['timestamp_utc', 'datetime_kst', 'date_kst', 'hour_kst', 'datetime_kst_str',
             'volumefrom', 'volumeto']].rename(columns={
        'volumefrom': 'volume_btc',
        'volumeto': 'volume_usd'
    })
    
    # Sort and take exactly the requested hours
    df = df.sort_values('timestamp_utc').tail(hours).reset_index(drop=True)
    
    return df


def plot_btc_hourly_volume(df, save_path='btc_hourly_volume_3weeks_kst.png'):
    """Line + area chart with 24h moving average (ideal for hourly data)"""
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # Use KST datetime for x-axis
    x = df['datetime_kst']
    usd_millions = df['volume_usd'] / 1_000_000
    
    # Area fill + line for volume
    ax.fill_between(x, usd_millions, color='#3498db', alpha=0.4)
    ax.plot(x, usd_millions, color='#3498db', linewidth=2, label='Hourly USD Volume')
    
    # 24-hour rolling average (smooths noise)
    ma24 = usd_millions.rolling(window=24, min_periods=1).mean()
    ax.plot(x, ma24, color='#e74c3c', linewidth=3, label='24-Hour Moving Average (1-day trend)')
    
    # Formatting
    ax.set_title('Bitcoin Hourly Trading Volume — Past 3 Weeks (KST)', fontsize=18, pad=20)
    ax.set_xlabel('Date & Time (KST)', fontsize=13)
    ax.set_ylabel('Volume (USD Millions)', fontsize=13)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Smart x-axis: show major ticks every 3 days
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45, ha='right')
    
    # Legend
    ax.legend(loc='upper left')
    
    # Partial hour warning
    last_time = df['datetime_kst_str'].iloc[-1]
    ax.text(0.02, 0.95, f'⚠️  Last hour ({last_time}) is PARTIAL',
            transform=ax.transAxes, fontsize=11, color='red',
            bbox=dict(boxstyle="round", facecolor="yellow", alpha=0.3))
    
    # Disclaimer
    ax.text(0.02, 0.02, 'Volume aggregated by UTC hourly candles\n'
                        'Displayed in KST (UTC+9) for local readability',
            transform=ax.transAxes, fontsize=10, color='gray',
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.7))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"💾 Chart saved as {save_path} (high resolution)")
    plt.show()


# ====================== RUN IT ======================
if __name__ == "__main__":
    YOUR_API_KEY = "paste_your_key_here"   # ← your CryptoCompare key
    
    try:
        df = get_btc_hourly_volume_cryptocompare(hours=504, api_key=YOUR_API_KEY)
        
        print("✅ Hourly BTC Volume (Past 3 Weeks — KST)\n")
        
        # Show first 8 + last 8 rows (full data is 504 rows)
        preview = pd.concat([df.head(8), df.tail(8)])
        print(preview[['datetime_kst_str', 'volume_btc', 'volume_usd']].to_string(index=False))
        
        # Summary stats
        print(f"\nTotal USD volume over 3 weeks: ${df['volume_usd'].sum():,.0f}")
        print(f"Average hourly volume: ${df['volume_usd'].mean():,.0f}")
        print(f"Peak hourly volume: ${df['volume_usd'].max():,.0f} "
              f"({df.loc[df['volume_usd'].idxmax(), 'datetime_kst_str']})")
        
        # Generate chart
        plot_btc_hourly_volume(df)
        
        # Save full data (ready for Excel, further analysis, etc.)
        df.to_csv('btc_hourly_volume_3weeks_kst.csv', index=False)
        print("\n💾 Full hourly data (with UTC + KST) saved to btc_hourly_volume_3weeks_kst.csv")
        
    except Exception as e:
        print(f"❌ Error: {e}")
