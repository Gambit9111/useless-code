import numpy as np
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, SignalStrategy, TrailingStrategy
import pandas as pd
import yfinance as yf
from backtesting.test import GOOG

class AdvancedRhinoTheoBollingerStrategy(SignalStrategy, TrailingStrategy):
    # Define optimizable parameters as class variables
    ema_fast_length = 150
    ema_slow_length = 200
    rsi_length = 12
    bollinger_length = 14
    bollinger_std = 2.0
    trail_sl = 0.95

    def init(self):
        price = self.data.Close

        # Register indicators for visualization
        self.ema_fast = self.I(self.calculate_ema, price, self.ema_fast_length)
        self.ema_slow = self.I(self.calculate_ema, price, self.ema_slow_length)
        self.rsi = self.I(self.calculate_rsi, price, self.rsi_length)
        self.bollinger_high, self.bollinger_low = self.I(self.calculate_bollinger_bands, price, self.bollinger_length, self.bollinger_std)


        # Initialize trailing stop-loss
        self.trail_sl = 0.1

    def calculate_ema(self, series, window):
        # Convert to Pandas Series if not already
        if not isinstance(series, pd.Series):
            series = pd.Series(series)
        return series.ewm(span=window, adjust=False).mean()

    def calculate_rsi(self, series, window):
        # Convert to Pandas Series if not already
        if not isinstance(series, pd.Series):
            series = pd.Series(series)
        delta = series.diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = pd.Series(gain).rolling(window=window).mean()
        avg_loss = pd.Series(loss).rolling(window=window).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_bollinger_bands(self, series, window, std_dev):
        # Convert to Pandas Series if not already
        if not isinstance(series, pd.Series):
            series = pd.Series(series)
        rolling_mean = series.rolling(window).mean()
        rolling_std = series.rolling(window).std()
        upper_band = rolling_mean + (rolling_std * std_dev)
        lower_band = rolling_mean - (rolling_std * std_dev)
        return upper_band, lower_band

    def next(self):
        if len(self.data.Close) < max(self.ema_fast_length, self.ema_slow_length, self.rsi_length, self.bollinger_length):
            return  # Not enough data

        # Enhanced exit logic
        if self.position:
            if self.position.is_long and self.rsi[-1] > 70:
                self.position.close()
            elif self.position.is_short and self.rsi[-1] < 30:
                self.position.close()

        # Entry logic
        else:
            if crossover(self.ema_fast, self.ema_slow):
                if self.data.Close[-1] > self.bollinger_high[-1]:
                    sl_price = self.data.Close[-1] * (1 - self.trail_sl)  # Stop-loss below the current price for a long position
                    self.buy(sl=sl_price)
            elif crossover(self.ema_slow, self.ema_fast):
                if self.data.Close[-1] < self.bollinger_low[-1]:
                    sl_price = self.data.Close[-1] * (1 + self.trail_sl)  # Stop-loss above the current price for a short position
                    self.sell(sl=sl_price)

# Run the backtest
bt = Backtest(strategy=AdvancedRhinoTheoBollingerStrategy, data=GOOG, cash=10000, commission=0.002, margin=1.0, exclusive_orders=True)
stats = bt.optimize(
    ema_fast_length=range(25, 200, 25),
    ema_slow_length=range(25, 200, 25),
    rsi_length=range(15, 17, 1),
    bollinger_length=range(19, 22, 1),
    bollinger_std=range(1, 3, 1),
    trail_sl = [0.1, 0.2, 0.3, 0.4, 0.5],
    maximize='Return [%]',
    constraint=lambda p: p.ema_fast_length < p.ema_slow_length
)
print(stats)
# Plotting
bt.plot()