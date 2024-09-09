from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
import os
def rename_columns(df):
    # df = df.rename(columns={"date": "Date"})
    df.set_index("date", inplace=True)
    df = df.set_index(pd.DatetimeIndex(pd.to_datetime(df.index)))
    df = df.rename(columns={"open": "Open", "max": "High", "min": "Low", "close": "Close", "Trading_Volume": "Volume"})
    return df