from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from ta.trend import SMAIndicator
from backtesting.test import GOOG
import pandas as pd

class BinaryOptionsStrategy(Strategy):
    def init(self):
        self.sma = SMAIndicator(pd.Series(self.data.Close), window=14).sma_indicator()
        self.upper_envelope = self.sma * (1 + 0.06)
        self.lower_envelope = self.sma * (1 - 0.06)

    def next(self):
        if crossover(pd.Series(self.data.Close), pd.Series(self.upper_envelope)) and not self.position:
            self.buy()
        elif crossover(pd.Series(self.lower_envelope), pd.Series(self.data.Close)) and self.position:
            self.position.close()

# Load Google stock data and run the backtest
data = GOOG.copy()
bt = Backtest(data, BinaryOptionsStrategy, cash=10000, commission=0.002)
stats = bt.run()
bt.plot()