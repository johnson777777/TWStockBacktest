import pandas as pd
import requests
import zipfile
import io
import os
from datetime import datetime, timedelta
import argparse


def process_data(product_code, start_date, end_date):
    current_date = start_date
    all_data = []

    while current_date <= end_date:
        date_str = current_date.strftime("%Y_%m_%d")
        file_path = f"/workspaces/TWStockBacktest/data/Daily_{date_str}.csv"
        
        
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, encoding='big5', 
                             dtype={'ExpiryMonth(Week)': str}, low_memory=False)

            df.columns = [
                'Date', 'ProductCode', 'ExpiryMonth(Week)', 'TradeTime', 
                'TradePrice', 'TradeVolume(B+S)', 'NearMonthPrice', 'FarMonthPrice', 'OpeningAuctionPrice'
            ]
            # product code "TX    " -> "TX"
            df.columns = df.columns.str.strip()
            df['ProductCode'] = df['ProductCode'].str.strip()


            # # Filter data
            df = df[df['ProductCode'] == 'TX']

            # Clean TradeTime column
            # Ensure the 'TradeTime' column is in datetime format
            # Drop rows with invalid TradeTime
            df['TradeTime'] = df['TradeTime'].astype(str).str.zfill(6)
            df['TradeTime'] = pd.to_datetime(df['TradeTime'], format='%H%M%S', errors='coerce')
            df = df.dropna(subset=['TradeTime'])

            # # Convert Date column to string
            df['Date'] = df['Date'].astype(str)

            # # Combine Date and TradeTime into a single datetime column
            df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['TradeTime'].dt.strftime('%H:%M:%S'))
            df.drop(columns=['Date', 'TradeTime'], inplace=True)

            # # Set 'Datetime' as the index for resampling
            df.set_index('Datetime', inplace=True)

            # ExpiryMonth(Week) sholud be one like 202408 if like 202408/202409, we should drop it
            df = df[~df['ExpiryMonth(Week)'].str.contains('/')]

            df_1m = df['TradePrice'].resample('1min').ohlc()

            all_data.append(df)

        current_date += timedelta(days=1)

    if all_data:
        combined_df = pd.concat(all_data)
        # Resample tick data to 1-minute intervals and compute OHLC
        df_1m = combined_df['TradePrice'].resample('1min').ohlc()

        # Aggregate other columns like 'TradeVolume'
        df_1m['Volume'] = combined_df['TradeVolume(B+S)'].resample('1min').sum()

        return df_1m
    else:
        return pd.DataFrame()

# Parse command line arguments
parser = argparse.ArgumentParser(description="Download and extract data from Taifex.")
parser.add_argument("product_code", type=str, help="Product code")
parser.add_argument("start_date", type=str, help="Start date in YYYY_MM_DD format")
parser.add_argument("end_date", type=str, help="End date in YYYY_MM_DD format")
args = parser.parse_args()

# Generate dates from start_date to end_date
start_date = datetime.strptime(args.start_date, "%Y_%m_%d")
end_date = datetime.strptime(args.end_date, "%Y_%m_%d")

# Generate 1-minute K-line data
df_1m_k = process_data(args.product_code, start_date, end_date)
print(df_1m_k)
df_1m_k.to_csv(f'/workspaces/TWStockBacktest/1mk/{args.product_code}_{args.start_date}_{args.end_date}_1m.csv')