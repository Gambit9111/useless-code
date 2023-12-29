import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import ta
from backtesting.test import GOOG
from pathlib import Path

# Helper function for EMA indicator
def EMA_indicator(series, window):
    series = pd.Series(series)
    return ta.trend.EMAIndicator(series, window=window).ema_indicator()

# EMA crossover strategy with position flipping and stop-loss
class EMACrossoverStrategy(Strategy):
    # Risk management parameters
    stop_loss_percent = 0.02  # Stop loss as a fraction of entry price
    
    ema_short = 15
    ema_long = 196

    def init(self):
        self.ema_short = self.I(EMA_indicator, self.data.Close, self.ema_short)  # Short EMA
        self.ema_long = self.I(EMA_indicator, self.data.Close, self.ema_long)  # Long EMA

    def next(self):
        current_price = self.data.Close[-1]
        is_buy_signal = crossover(self.ema_short, self.ema_long)
        is_sell_signal = crossover(self.ema_long, self.ema_short)

        if is_buy_signal:
            if self.position.is_short:
                self.position.close()  # Close short position if it exists
            entry_price = self.data.Close[-1]
            stop_loss_price = entry_price * (1 - self.stop_loss_percent)  # Stop price for a long position
            self.buy(sl=stop_loss_price)

        elif is_sell_signal:
            if self.position.is_long:
                self.position.close()  # Close long position if it exists
            entry_price = self.data.Close[-1]
            stop_loss_price = entry_price * (1 + self.stop_loss_percent)  # Stop price for a short position
            self.sell(sl=stop_loss_price)


# Define the optimization settings
default_settings = {
    'ema_short': 50,
    'ema_long': 100,
}

# Run the backtest with optimization
bt = Backtest(strategy=EMACrossoverStrategy, data=GOOG, cash=10000, commission=0.002, margin=1.0, exclusive_orders=True)
result = bt.optimize(
    ema_short=(5, 200, 5),  
    ema_long=(5, 200, 5),  
    maximize='Equity Final [$]',
    constraint=lambda p: p.ema_short > p.ema_long  # Adding constraints
)

# Output the best settings
print(result)
print(bt.run())

# Plot the optimization summary
bt.plot()