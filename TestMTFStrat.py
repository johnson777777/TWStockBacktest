from FinMind.data import DataLoader
import utils
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, resample_apply


class TestWeekly(Strategy):
    upper_bound = 60
    lower_bound = 60
    stop_loss = 0.95

    def init(self):
        # Calculate daily KD using talib
        self.daily_k, self.daily_d = self.I(
            talib.STOCH,
            self.data.High, self.data.Low, self.data.Close,
            fastk_period=9, slowk_period=3, slowd_period=3
        )
        # print(self.data.Close.s)
        # close = self.data.Close.s
        # weekly = close.resample('W-Fri').agg('last')
        # print(weekly)
        # # reindex
        # w = weekly.reindex(close.index).bfill()
        # print(w)
        # self.daily_rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        # self.weekly_rsi = resample_apply('W', talib.RSI, self.data.Close, timeperiod=14)
        # print(self.daily_rsi)
        # print(self.weekly_rsi)
        self.weekly_data = self.data.df.resample('W-Fri').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last'
        }).dropna()
        # print(self.weekly_data)
        # self.weekly_data = self.weekly_data.ffill().bfill()
        # print(self.weekly_data.isnull().sum())

        # t = self.weekly_data.reindex(self.data.df.index).bfill()
        # print(t)
        # print(self.data.Close)
        # Use pre-resampled weekly data for KD calculation
        # self.weekly_k, self.weekly_d = self.I(
        #     talib.STOCH,
        #     self.weekly_data['High'], self.weekly_data['Low'], self.weekly_data['Close'],
        #     fastk_period=9, slowk_period=3, slowd_period=3
        # )
        weekly_k, weekly_d = talib.STOCH(
            self.weekly_data.High, self.weekly_data.Low, self.weekly_data.Close,
            fastk_period=9, slowk_period=3, slowd_period=3
        )
        # print(weekly_k.to_string())
        # print(weekly_d)
        self.weekly_k = weekly_k.reindex(self.data.df.index).ffill()
        self.weekly_d = weekly_d.reindex(self.data.df.index).ffill()
        # self.weekly_k = pd.Series(weekly_k, index=self.weekly_data.index).reindex(self.data.df.index).ffill().values
        # self.weekly_d = pd.Series(weekly_d, index=self.weekly_data.index).reindex(self.data.df.index).ffill().values
        # print(self.weekly_k)
        # print(self.weekly_d)


    def next(self):
        # Define the entry/exit conditions using crossover of daily and weekly KD values
        if (crossover(self.daily_k, self.daily_d) and 
            self.daily_k < self.lower_bound and
            self.weekly_k[-1] < self.lower_bound):
            self.buy(sl=self.stop_loss * self.data.Close)
        
        elif (crossover(self.daily_d, self.daily_k) and 
              self.daily_k > self.upper_bound and
              self.weekly_k[-1] > self.upper_bound):
            if self.position.is_long:
                self.position.close()
# Load the data from FinMind
df = DataLoader().taiwan_stock_daily(stock_id='3231', start_date='2003-01-01', end_date='2024-09-07')
df = utils.rename_columns(df)

# Run the backtest
bt = Backtest(df, TestWeekly, cash=10000)
# output = bt.run()
output, heatmap = bt.optimize(
    upper_bound=range(0, 100, 5),
    lower_bound=range(0, 100, 5),
    # stop_loss=range(90, 100, 1),
    # constraint=lambda param: param.upper_bound > param.lower_bound,
    maximize='Equity Final [$]',
    return_heatmap=True
)
bt.plot()
print(output)