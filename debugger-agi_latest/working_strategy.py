from backtesting import Backtest, Strategy
from backtesting.test import GOOG
import pandas as pd
import ta

class GridTradingStrategy(Strategy):
    # Define optimizable parameters
    atr_period = 14
    atr_multiplier = 2
    lot_size = 50

    # Define the init method
    def init(self):
        df = pd.DataFrame({
            'open': self.data.Open,
            'high': self.data.High,
            'low': self.data.Low,
            'close': self.data.Close
        })
        
        # Calculate the ATR with optimizable period
        df['atr'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=self.atr_period)
        self.df = df
        self.upper_grid = None
        self.lower_grid = None

    # Main strategy loop
    def next(self):
        atr_value = self.df['atr'].iloc[-1]  # Get the ATR value
        price = self.data.Close[-1]

        if self.upper_grid is None or price >= self.upper_grid or price <= self.lower_grid:
            self.upper_grid = price + atr_value * self.atr_multiplier
            self.lower_grid = price - atr_value * self.atr_multiplier

        if not self.position:
            sl_price = price + atr_value
            tp_price = price - atr_value
            self.sell(size=self.lot_size, sl=sl_price, tp=tp_price)
            self.buy(size=self.lot_size, sl=tp_price, tp=sl_price)
        else:
            if self.position.is_long and price <= self.lower_grid:
                self.position.close()
            elif self.position.is_short and price >= self.upper_grid:
                self.position.close()

# Define the optimization settings
default_settings = {
    'atr_period': 14,
    'atr_multiplier': 2,
    'lot_size': 50
}

# Run the backtest with optimization
bt = Backtest(strategy=GridTradingStrategy, data=GOOG, cash=10000, commission=0.002, margin=1.0, exclusive_orders=True)
result = bt.optimize(
    atr_period=(10, 30, 5),  # ATR period to optimize
    atr_multiplier=(1, 3, 0.5),  # ATR multiplier to optimize
    lot_size=(50, 100, 10),  # Lot size to optimize
    constraint=lambda p: p.atr_period < 2 * p.atr_multiplier  # Adding constraints
)

# Output the best settings
print(result)
print(bt.run())

# Plot the optimization summary
bt.plot()