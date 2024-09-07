from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from FinMind.data import DataLoader
import pandas as pd

import talib
from talib import abstract
import utils


class RsiOscillator(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14
    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_window)

    def next(self):
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
        elif crossover(self.lower_bound, self.rsi):
            self.buy()

df = DataLoader().taiwan_stock_daily(stock_id='3231', start_date='2003-01-01', end_date='2024-09-07')
df = utils.rename_columns(df)
bt = Backtest(df, RsiOscillator, cash=10_000, commission=.002)
stats = bt.run()
print(stats)
bt.plot()