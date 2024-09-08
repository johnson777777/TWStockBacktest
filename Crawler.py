import requests
import zipfile
import io
import os
from datetime import datetime, timedelta
import argparse

# Function to download and extract ZIP file
def download_and_extract(date_str):
    url = f"https://www.taifex.com.tw/file/taifex/Dailydownload/DailydownloadCSV/Daily_{date_str}.zip"
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall("/workspaces/TWStockBacktest/data")
            print(f"Files for {date_str} extracted successfully.")
    else:
        print(f"Failed to download file for {date_str}: {response.status_code}")

# Parse command line arguments
parser = argparse.ArgumentParser(description="Download and extract data from Taifex.")
parser.add_argument("start_date", type=str, help="Start date in YYYY_MM_DD format")
parser.add_argument("end_date", type=str, help="End date in YYYY_MM_DD format")
args = parser.parse_args()

# Generate dates from start_date to end_date
start_date = datetime.strptime(args.start_date, "%Y_%m_%d")
end_date = datetime.strptime(args.end_date, "%Y_%m_%d")
current_date = start_date

while current_date <= end_date:
    date_str = current_date.strftime("%Y_%m_%d")
    print(f"Processing date: {date_str}")
    try:
        download_and_extract(date_str)
    except Exception as e:
        print(f"Error processing date {date_str}: {e}")
    current_date += timedelta(days=1)

# List the extracted files
extracted_files = os.listdir("/workspaces/TWStockBacktest/data")
print("Extracted files:", extracted_files)