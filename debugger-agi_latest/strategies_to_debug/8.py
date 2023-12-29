import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, SignalStrategy, TrailingStrategy
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import EMAIndicator, MACD
from ta.volatility import AverageTrueRange, BollingerBands

class AdvancedTradingStrategy(Strategy):
    # Define parameters for optimization and dynamic adjustment
    rsi_period = 14
    ema_short_period = 50
    ema_long_period = 200
    atr_period = 14
    macd_fast = 12
    macd_slow = 26
    macd_signal = 9
    bollinger_period = 20
    stochastic_k = 14
    stochastic_d = 3

    def init(self):
        # Initialize and calculate indicators
        price = self.data.Close
        self.rsi = RSIIndicator(close=price, window=self.rsi_period).rsi()
        self.ema_short = EMAIndicator(close=price, window=self.ema_short_period).ema_indicator()
        self.ema_long = EMAIndicator(close=price, window=self.ema_long_period).ema_indicator()
        self.macd = MACD(close=price, window_slow=self.macd_slow, window_fast=self.macd_fast, window_sign=self.macd_signal).macd_diff()
        self.atr = AverageTrueRange(high=self.data.High, low=self.data.Low, close=price, window=self.atr_period).average_true_range()
        self.bollinger = BollingerBands(close=price, window=self.bollinger_period).bollinger_hband_indicator()
        self.stochastic = StochasticOscillator(high=self.data.High, low=self.data.Low, close=price, window=self.stochastic_k, smooth_window=self.stochastic_d).stoch()

        # Entry conditions
        self.long_condition = (self.rsi > 50) & (price > self.ema_long)
        self.short_condition = (self.rsi < 50) & (price < self.ema_long)

    def next(self):
        if not self.position:
            # Long entry condition
            if self.long_condition[-1]:
                self.buy(sl=self.data.Low[-1] - 2 * self.atr[-1],
                         tp=self.data.Close[-1] + 4 * self.atr[-1])
            # Short entry condition
            elif self.short_condition[-1]:
                self.sell(sl=self.data.High[-1] + 2 * self.atr[-1],
                          tp=self.data.Close[-1] - 4 * self.atr[-1])
        else:
            # Dynamic exit strategy
            if self.position.is_long and self.macd[-1] < 0:
                self.position.close()
            elif self.position.is_short and self.macd[-1] > 0:
                self.position.close()

# Load Google's stock data
from backtesting.test import GOOG

# Run backtesting with optimization
backtest = Backtest(GOOG, AdvancedTradingStrategy, cash=10000, commission=.002)
stats = backtest.optimize(rsi_period=range(12, 18, 2),
                          ema_short_period=range(40, 60, 5),
                          ema_long_period=range(190, 220, 10),
                          constraint=lambda p: p.ema_short_period < p.ema_long_period)
print(stats)

# Optionally, plot the results
backtest.plot()