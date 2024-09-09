import pandas as pd
from backtesting import Backtest, Strategy
import utils
import talib
from backtesting.lib import crossover


class DayTradeStrat(Strategy):
    def init(self):
        pass

    def next(self):
        pass

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


df = pd.read_csv('1mk/TX_2024_07_30_2024_07_30_1m.csv')
df = df.dropna()
df = df.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close"})
df = df.set_index("Datetime")
df = df.set_index(pd.DatetimeIndex(pd.to_datetime(df.index)))
bt = Backtest(df, RsiOscillator, cash=1000000)
output = bt.run()
print(output)
bt.plot()