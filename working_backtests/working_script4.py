import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG

import ta
# Helper function for SMA indicator
def SMA_indicator(series, window):
    series = pd.Series(series)
    return ta.trend.SMAIndicator(series, window=window).sma_indicator()

# SMA crossover strategy with single position management and stop-loss
class SMACrossoverStrategy(Strategy):
    # Risk management parameters
    stop_loss_percent = 0.25  # Stop loss as a fraction of entry price
    
    sma_short = 15
    sma_long = 196
    sma_day = 1535

    def init(self):
        self.sma_short = self.I(SMA_indicator, self.data.Close, self.sma_short)  # Short SMA (18 days)
        self.sma_long = self.I(SMA_indicator, self.data.Close, self.sma_long)  # Long SMA (183 days)
        self.sma_day = self.I(SMA_indicator, self.data.Close, self.sma_day)  # Long SMA (200 days)

    def next(self):
        current_price = self.data.Close[-1]

        is_buy_signal = crossover(self.sma_short, self.sma_long)
        is_sell_signal = crossover(self.sma_long, self.sma_short)

        if is_buy_signal:
            if self.position.is_short:
                self.position.close()  # Close short position if it exists
            elif current_price > self.sma_day[-1]:
                self.position.close()  # Close any existing long position before opening a new one
                entry_price = self.data.Close[-1]
                stop_loss_price = entry_price * (1 - self.stop_loss_percent)  # Stop price for a long position
                self.buy(sl=stop_loss_price)

        elif is_sell_signal:
            if self.position.is_long:
                self.position.close()  # Close long position if it exists
            elif current_price < self.sma_day[-1]:
                self.position.close()  # Close any existing short position before opening a new one
                entry_price = self.data.Close[-1]
                stop_loss_price = entry_price * (1 + self.stop_loss_percent)  # Stop price for a short position
                self.sell(sl=stop_loss_price)

# Define the optimization settings
default_settings = {
    'stop_loss_percent': 0.25,
    'sma_short': 15,
    'sma_long': 196,
    'sma_day': 500
}

# Run the backtest with optimization
bt = Backtest(strategy=SMACrossoverStrategy, data=GOOG, cash=10000, commission=0.002, margin=1.0, exclusive_orders=True)
result = bt.optimize(
    sma_short=(5, 200, 5),  
    sma_long=(5, 200, 5),
    sma_day=(200, 500, 100),
    maximize='Equity Final [$]',
    constraint=lambda p: p.sma_short < p.sma_long  # Adding constraints
)

# Output the best settings
print(result)
print(bt.run())

# Plot the optimization summary
bt.plot()