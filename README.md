# Task1-Stock-OHLC-Downloader
This script downloads historical stock data using yfinance based on user-entered symbol, date range, and timeframe. It cleans, formats, and resamples the OHLCV data, then saves the processed output to a CSV file. Supports multiple intervals and automatically appends new data to existing files.
How It Works (Easy Explanation)

***1️⃣ User Enters Details***
You type symbol, date range, and timeframe.

Example:

Symbol: SBIN.NS
Start date: 2024-01-01
End date: 2024-02-01
Timeframe: 1h

***2️⃣ Timeframe Validation***

The script checks if your timeframe is valid.
If not, it stops and shows:
Invalid Timeframe

***3️⃣ Download Stock Data***

Using yfinance:
data = yf.download(...)
If no data:
No data available

***4️⃣ Clean Data***
The script:

Resets index
Identifies Datetime or Date column
Splits into date and time
Keeps only OHLCV columns
Drops missing rows

***5️⃣ Create Datetime Index***
date + time → datetime
Now resampling becomes possible.

***6️⃣ Resampling 🔁***
Example: 1h or 1d candle data

  The script applies:
        open → first value
        high → max value
        low → min value
        close → last value 
        volume → sum

***7️⃣ Save to CSV***

File name format:

SYMBOL_TIMEFRAME.csv
Example: SBIN.NS_1h.csv


If file already exists → new data will be appended.

📂 Output CSV Format
date, time, open, high, low, close, volume
2024-01-01, 09:15:00, 620.10, 622.50, 619.00, 622.00, 1200000
...
