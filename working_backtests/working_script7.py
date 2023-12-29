# Import necessary libraries
from backtesting import Backtest
from backtesting.lib import SignalStrategy, TrailingStrategy
from backtesting.test import GOOG
import pandas as pd
import numpy as np

# Custom RSI calculation function
# Define custom indicator calculation functions
# Define the RSI, EMA, and ATR indicator calculation methods
def calculate_ema(series, window):
    return series.ewm(span=window, adjust=False).mean()

def calculate_rsi(series, window):
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=window).mean()
    avg_loss = pd.Series(loss).rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_atr(high, low, close, window):
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=window).mean()
    return atr

# Defining the RSI and MA Scalping Strategy with advanced features
class Enhanced_RSIMA_Scalping_Strategy(SignalStrategy, TrailingStrategy):
    # Strategy parameters (modifiable for optimization)
    n1 = 14  # RSI period
    n2 = 150  # EMA period
    rsi_high = 66  # RSI high level for sell signal
    rsi_low = 35.5  # RSI low level for buy signal
    atr_period = 14  # Average True Range period for dynamic SL/TP
    stop_loss_factor = 2.0  # Factor for setting stop loss (increased from 1.5 to enhance risk management)
    entry_price = None  # Entry price for trailing stop

    def init(self):
        # Calculating the RSI using the custom RSI function and the EMA indicator
        close = pd.Series(self.data.Close)
        self.rsi = self.I(calculate_rsi, close, self.n1)
        self.ema = self.I(calculate_ema, pd.Series(self.data.Close), self.n2)

        # Calculating the ATR indicator
        high = pd.Series(self.data.High)
        low = pd.Series(self.data.Low)
        close = pd.Series(self.data.Close)
        self.atr = self.I(calculate_atr, high, low, close, window=self.atr_period)

    def next(self):
        if len(self.atr) > 0:  # Ensure that ATR indicator values are available
            atr_value = self.atr[-1]  # Accessing ATR value directly

            if not self.position:  # If no position is open
                if self.rsi < 30 and self.ema > self.data.Close:
                    stop_loss = self.data.Close[-1] - atr_value * 2  # Set stop loss based on ATR
                    self.buy(sl=stop_loss)
                    self.entry_price = self.data.Close[-1]  # Store the entry price
                elif self.rsi > 70 and self.ema < self.data.Close:
                    stop_loss = self.data.Close[-1] + atr_value * 2  # Set stop loss based on ATR
                    self.sell(sl=stop_loss)
                    self.entry_price = self.data.Close[-1]  # Store the entry price
            else:  # If a position is open, check for opposite signals to close it
                if self.position.is_long and (self.rsi > 70 and self.ema < self.data.Close):
                    self.position.close()
                elif self.position.is_short and (self.rsi < 30 and self.ema > self.data.Close):
                    self.position.close()


# Run the backtest with modified parameters
bt = Backtest(strategy=Enhanced_RSIMA_Scalping_Strategy, data=GOOG, cash=10000, commission=0.002, margin=1.0, exclusive_orders=True)
stats = bt.optimize(
    n1=range(12, 16, 1),
    n2=range(100, 200, 10),  # Expanded range for EMA period
    atr_period=range(10, 20, 1),  # Expanded range for ATR period
    maximize='Return [%]',
)
print(stats)
# Plotting
bt.plot()