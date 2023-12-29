from backtesting import Backtest, Strategy
from backtesting.test import GOOG
import pandas as pd
import numpy as np

class AdvancedBollingerTrendStrategy(Strategy):
    # Define parameters as class variables 
    bb_window = 20 
    bb_dev = 2 
    rsi_period = 14 
    rsi_overbought = 70 
    rsi_oversold = 30 

    def init(self): 
        close = self.data.Close
        self.upper_band, self.lower_band = self.I(self.calculate_bollinger_bands, close, self.bb_window, self.bb_dev) 
        self.rsi = self.I(self.calculate_rsi, close, self.rsi_period)

    def calculate_bollinger_bands(self, series, window, std_dev):
        # Ensuring the series is a Pandas Series
        if not isinstance(series, pd.Series):
            series = pd.Series(series)
        rolling_mean = series.rolling(window).mean()
        rolling_std = series.rolling(window).std()
        upper_band = rolling_mean + (rolling_std * std_dev)
        lower_band = rolling_mean - (rolling_std * std_dev)
        return upper_band, lower_band

    def calculate_rsi(self, series, window):
        # Ensuring the series is a Pandas Series
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

    def next(self): 
        if self.position: 
            if self.data.Close[-1] < self.upper_band[-1] and self.position.is_long or self.rsi[-1] > self.rsi_overbought: 
                self.position.close() 
            elif self.data.Close[-1] > self.lower_band[-1] and self.position.is_short or self.rsi[-1] < self.rsi_oversold: 
                self.position.close() 
        else: 
            if self.data.Close[-1] > self.upper_band[-1]: 
                self.buy() 
            elif self.data.Close[-1] < self.lower_band[-1]: 
                self.sell()

# Define the optimization settings
default_settings = {
    'bb_window': 20,
    'bb_dev': 2,
    'rsi_period': 14,
    'rsi_overbought': 70,
    'rsi_oversold': 30,
}

# Run the backtest with optimization
bt = Backtest(strategy=AdvancedBollingerTrendStrategy, data=GOOG, cash=10000, commission=0.002, margin=1.0, exclusive_orders=True)
result = bt.optimize(
    bb_window=range(18, 22, 2),  
    bb_dev=range(1, 3, 1),
    rsi_period=range(10, 18, 2),
    rsi_overbought=range(60, 80, 10),
    rsi_oversold=range(20, 40, 10),
    maximize='Return [%]',
    constraint=lambda p: p.rsi_overbought > p.rsi_oversold
)

# Output the best settings
print(result)

# Plot the optimization summary
bt.plot()