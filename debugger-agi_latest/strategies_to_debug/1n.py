import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, TrailingStopLoss
from ta.volatility import BollingerBands
from ta.trend import SMAIndicator

class DojiEngulfingStrategy(Strategy):
    # Strategy parameters, which can be optimized
    bollinger_period = 30
    bollinger_std_dev = 1.5
    trailing_stop_loss = 0.02
    position_size = 0.1  # Percentage of portfolio to be used per trade

    def init(self):
        # Initialize Bollinger Bands indicator
        close = self.data.Close
        self.bb = BollingerBands(close, self.bollinger_period, self.bollinger_std_dev)

        # Improved Doji and Engulfing patterns detection logic
        self.doji = self.I(self.is_doji, self.data.Open, self.data.Close, self.data.High, self.data.Low)
        self.engulfing = self.I(self.is_engulfing, self.data.Open, self.data.Close, self.data.High, self.data.Low)

    @staticmethod
    def is_doji(open, close, high, low):
        # A more refined Doji detection logic
        doji_size = 0.1  # Threshold for the body size relative to the candle size
        return abs(close - open) / (high - low) < doji_size

    @staticmethod
    def is_engulfing(open, close, high, low):
        # A more refined Engulfing pattern detection logic
        return (close > open and close > high.shift(1) and open < low.shift(1)) or                (open > close and open > high.shift(1) and close < low.shift(1))

    def next(self):
        # Implement dynamic position sizing based on the account equity
        position_size = self.equity * self.position_size

        # Define entry and exit criteria
        if not self.position:
            if (self.doji[-1] or self.engulfing[-1]) and self.data.Close[-1] < self.bb.bollinger_lband()[-1]:
                # Entry for a long position
                self.buy(size=position_size)
                self.sell(size=position_size, stop=self.data.Close[-1] * (1 - self.trailing_stop_loss))
        else:
            if (self.doji[-1] or self.engulfing[-1]) and self.data.Close[-1] > self.bb.bollinger_hband()[-1]:
                # Exit for a long position
                self.position.close()

# Load data
data = pd.read_csv('EURUSD_hourly.csv')

# Run backtest
backtest = Backtest(data, DojiEngulfingStrategy, cash=10000, commission=.002)
stats = backtest.run()
backtest.plot()
