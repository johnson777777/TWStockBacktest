from backtesting import Backtest, Strategy
from backtesting.lib import crossover, plot_heatmaps

from FinMind.data import DataLoader
import pandas as pd

import talib
from talib import abstract
import utils

class KdStrat(Strategy):
    upper_bound = 92
    lower_bound = 4
    stop_loss = 0.95

    def init(self):
        self.k, self.d = self.I(talib.STOCH, self.data.High, self.data.Low, self.data.Close, fastk_period=9, slowk_period=3, slowd_period=3)
        
    def next(self):
        if (crossover(self.k, self.d) and self.k < self.lower_bound):
            # self.buy(size=0.1, sl=0.95*self.data.Close)
            self.buy(sl=0.95*self.data.Close)
            if self.position.is_short:
                self.position.close()
        elif crossover(self.d, self.k) and self.k > self.upper_bound:
            # self.sell()
            if self.position.is_long:
                self.position.close()
            

df = DataLoader().taiwan_stock_daily(stock_id='3231', start_date='2003-01-01', end_date='2024-09-07')
df = utils.rename_columns(df)
bt = Backtest(df, KdStrat, cash=10000)
output = bt.run()
# output, heatmap= bt.optimize(
#     upper_bound=range(50, 100, 5),
#     lower_bound=range(0, 50, 5),
#     constraint=lambda param: param.upper_bound > param.lower_bound,
#     maximize='Equity Final [$]',
#     return_heatmap=True)
print(output)
lower_bound, upper_bound = output._strategy.lower_bound, output._strategy.upper_bound
bt.plot(filename=f'plot/{lower_bound}-{upper_bound}.html')
# plot_heatmaps(heatmap, filename=f'plot/{lower_bound}-{upper_bound}-heatmap.html')