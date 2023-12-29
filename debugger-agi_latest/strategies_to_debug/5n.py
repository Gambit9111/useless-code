import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, TrailingStrategy
from ta.trend import SuperTrend, EMAIndicator, IchimokuIndicator
import matplotlib.pyplot as plt

class SuperTrendStrategy(TrailingStrategy):
    # Parameters for dynamic input and optimization
    super_trend_period = 10
    super_trend_multiplier = 3
    ema_period = 200
    stop_loss_percentage = 0.02  # 2% stop loss

    def init(self):
        # Data validation
        if len(self.data) < self.ema_period:
            raise ValueError(f"Insufficient data. Need at least {self.ema_period} data points.")
        
        # Implementing the Super Trend Indicator
        self.super_trend = SuperTrend(self.data.High, self.data.Low, self.data.Close, 
                                      period=self.super_trend_period, multiplier=self.super_trend_multiplier)
        
        # EMA Indicator
        self.ema = EMAIndicator(self.data.Close, window=self.ema_period).ema_indicator()
        
        # Ichimoku Indicator
        self.ichimoku = IchimokuIndicator(self.data.High, self.data.Low)

    def next(self):
        # Check if we are in a position
        if not self.position:
            # Long Entry Condition
            if self.data.Close > self.ema and self.data.Close > self.super_trend.super_trend():
                self.buy(sl=self.data.Close * (1 - self.stop_loss_percentage))
            
            # Short Entry Condition
            elif self.data.Close < self.ema and self.data.Close < self.super_trend.super_trend():
                self.sell(sl=self.data.Close * (1 + self.stop_loss_percentage))

        # Dynamic exit strategy based on Super Trend Indicator
        elif self.position.is_long and self.data.Close < self.super_trend.super_trend():
            self.position.close()
        elif self.position.is_short and self.data.Close > self.super_trend.super_trend():
            self.position.close()

# Load the data
data = pd.read_csv('GOOG_data.csv')

# Backtesting the strategy with dynamic parameters
bt = Backtest(data, SuperTrendStrategy, cash=10000, commission=.002, exclusive_orders=True)
stats = bt.optimize(super_trend_period=range(7, 15, 1),
                    super_trend_multiplier=[1.5, 2, 2.5, 3],
                    ema_period=range(50, 250, 50),
                    stop_loss_percentage=[0.01, 0.015, 0.02, 0.025],
                    maximize='Equity Final [$]')
print(stats)

# Plotting the performance
bt.plot()
