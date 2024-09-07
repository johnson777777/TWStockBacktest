from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from FinMind.data import DataLoader
import pandas as pd

import talib
from talib import abstract
import utils

class KdStrat(Strategy):
    def init(self):
        print(self.data)
        self.k, self.d = self.I(talib.STOCH, self.data.High, self.data.Low, self.data.Close, fastk_period=9, slowk_period=3, slowd_period=3)
        
    def next(self):
        if crossover(self.k, self.d) and self.k < 10: 
            self.buy()
        elif crossover(self.d, self.k) and self.k > 90:
            self.position.close()
            

df = DataLoader().taiwan_stock_daily(stock_id='3231', start_date='2003-01-01', end_date='2024-09-07')
df = utils.rename_columns(df)
bt = Backtest(df, KdStrat, cash=10000)
output = bt.run()
print(output)
bt.plot()