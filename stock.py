# ============================================
# Stock Data Downloader & Resampler
# Using yfinance + pandas
# ============================================

import yfinance as yf
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

#---------------for user input--------------------------
symbol =input("💹Enter stock symbol(e.g., SBIN.NS, RELIANCE.NS)")#for user input
start_date = input("📅Enter Start Date(yyyy-mm-dd)")
end_date = input("📅Enter End Date(yyyy-mm-dd)")
timeframe = input("⌛Enter Timeframe(e.g.,1h, 2d, 5wk, etc.)")

# --- Validate Timeframe ---
valid_intervals = ['1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo']
if timeframe not in valid_intervals:#that not match to valid_time
        print("Invalid Timeframe")
        exit()

# --- Download stock Data ---
try:
    print(f"\nDownloading data for {symbol}...")
    data = yf.download(
        tickers=symbol,
        start=start_date,
        end=end_date,
        interval=timeframe,
        progress = False
    )

    # Check if data is empty
    if data.empty:
        print("No data available or chck your data")
        exit()#stops the script

    # --- Clean and Format Data ---
    data.reset_index(inplace=True)

    #--- If "Datetime" column  exists → use that.Else → use "Date".--
    datetime_col = 'Datetime' if 'Datetime' in data.columns else 'Date'

    #--------split date and time---------
    data['date'] = pd.to_datetime(data[datetime_col]).dt.date
    data['time'] = pd.to_datetime(data[datetime_col]).dt.time

    # Keep only necessary columns
    data = data[['date', 'time', 'Open', 'High', 'Low', 'Close', 'Volume']]
    data.columns = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']

    # Drop missing rows
    data.dropna(inplace=True)

    # --- Resampling ---
    data['datetime'] = pd.to_datetime(data['date'].astype(str) + ' ' + data['time'].astype(str))
    #--------Rename columns to lowercase----
    data.set_index('datetime', inplace=True)

    # Apply resampling logic
    # df.resample() that make group for same time
    # agg()->deside price
    resampled = data.resample(timeframe).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()#remove empty data
    #remove empty data
    #resampled ['date']

    # Recreate date/time columns
    resampled['date'] = resampled.index.date
    resampled['time'] = resampled.index.time

    # Rearrange columns
    resampled = resampled[['date', 'time', 'open', 'high', 'low', 'close', 'volume']]

    # --- Save to CSV ---
    filename = f"{symbol}_{timeframe}.csv"
    # -----add new data in common file
    # update csv file
    resampled.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)
    print(f"\n✅ Data saved successfully as: {filename}")

#if create error so try: is close(Exception)
except Exception as e:
    print(f"\n Error {e}")
