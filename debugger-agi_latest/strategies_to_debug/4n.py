from backtesting import Backtest, Strategy
from backtesting.lib import crossover, SignalStrategy, TrailingStrategy
from backtesting.test import GOOG
import pandas as pd
import numpy as np
import ta

class AdvancedPriceActionStrategy(Strategy):
    stop_loss_percentage = 0.02  # 2% stop loss
    take_profit_ratio = 2       # Take profit at two times the risk

    def init(self):
        # More sophisticated technical analysis methods
        self.atr = self.I(ta.volatility.average_true_range, self.data.High, self.data.Low, self.data.Close)
        self.support = self.I(self.calculate_dynamic_support, self.data.Low)
        self.resistance = self.I(self.calculate_dynamic_resistance, self.data.High)
        self.is_bullish_engulfing = self.I(ta.candlestick.bullish_engulfing, self.data.Open, self.data.Close)
        self.is_bearish_engulfing = self.I(ta.candlestick.bearish_engulfing, self.data.Open, self.data.Close)

    def calculate_dynamic_support(self, low_prices):
        # Advanced support calculation
        return ta.volatility.bollinger_lband(low_prices)

    def calculate_dynamic_resistance(self, high_prices):
        # Advanced resistance calculation
        return ta.volatility.bollinger_hband(high_prices)

    def next(self):
        price = self.data.Close[-1]

        # Dynamic risk management
        self.stop_loss = price * self.stop_loss_percentage * self.atr[-1]
        self.take_profit = price * self.take_profit_ratio * self.atr[-1]

        # Entry Criteria
        if self.is_bullish_engulfing and price < self.support and not self.position:
            self.buy()
        elif self.is_bearish_engulfing and price > self.resistance and not self.position:
            self.sell()

        # Exit Criteria
        if self.position.is_long:
            if price >= self.position.entry_price + self.take_profit:
                self.position.close()
            elif price <= self.position.entry_price - self.stop_loss:
                self.position.close()

        elif self.position.is_short:
            if price <= self.position.entry_price - self.take_profit:
                self.position.close()
            elif price >= self.position.entry_price + self.stop_loss:
                self.position.close()

# Backtesting
bt = Backtest(GOOG, AdvancedPriceActionStrategy, cash=10000, commission=.002)
stats = bt.run()
bt.plot()

# Print key performance metrics
print(f"Sharpe Ratio: {stats['Sharpe Ratio']}")
print(f"Max Drawdown: {stats['Max. Drawdown']}")
print(f"Profit Factor: {stats['Profit Factor']}")