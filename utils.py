import pandas as pd

def rename_columns(df):
    df = df.rename(columns={"date": "Date"})
    df.set_index("Date", inplace=True)
    df = df.set_index(pd.DatetimeIndex(pd.to_datetime(df.index)))
    df = df.rename(columns={"open": "Open", "max": "High", "min": "Low", "close": "Close", "Trading_Volume": "Volume"})
    return df