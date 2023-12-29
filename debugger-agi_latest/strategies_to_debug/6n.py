# Importing required libraries
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, TrailingStopLoss
import pandas as pd
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

class AdvancedBreakoutStrategy(Strategy):
    # Parameters for optimization
    n1 = 20  # Period for fast EMA
    n2 = 50  # Period for slow EMA
    macd_fast = 12
    macd_slow = 26
    macd_signal = 9
    rsi_period = 14
    atr_period = 14
    trailing_stop_multiplier = 3  # Multiplier for ATR-based trailing stop-loss

    def init(self):
        # Indicators
        close = self.data.Close
        self.ema_fast = self.I(EMAIndicator(close, self.n1).ema_indicator)
        self.ema_slow = self.I(EMAIndicator(close, self.n2).ema_indicator)
        self.macd = self.I(MACD(close, self.macd_fast, self.macd_slow, self.macd_signal).macd_diff)
        self.rsi = self.I(RSIIndicator(close, self.rsi_period).rsi)
        self.atr = self.I(AverageTrueRange(self.data.High, self.data.Low, close, self.atr_period).average_true_range)

    def next(self):
        # Entry criteria
        if crossover(self.ema_fast, self.ema_slow) and self.macd > 0 and self.rsi < 70:
            if not self.position.is_long:
                self.buy()
        elif crossover(self.ema_slow, self.ema_fast) and self.macd < 0 and self.rsi > 30:
            if not self.position.is_short:
                self.sell()

        # Dynamic trailing stop-loss based on ATR
        if self.position:
            atr_stop_loss = self.atr * self.trailing_stop_multiplier
            self.position.close_if(lambda x: 
                                   (x.is_long and x.price <= x.entry_price - atr_stop_loss) or 
                                   (x.is_short and x.price >= x.entry_price + atr_stop_loss))

def backtest_strategy():
    # Loading data
    from backtesting.test import GOOG
    data = GOOG

    # Running backtest
    bt = Backtest(data, AdvancedBreakoutStrategy, cash=10000, commission=.002)
    stats = bt.run()
    bt.plot()

    return stats

# Running the backtest
stats = backtest_strategy()
print(stats)