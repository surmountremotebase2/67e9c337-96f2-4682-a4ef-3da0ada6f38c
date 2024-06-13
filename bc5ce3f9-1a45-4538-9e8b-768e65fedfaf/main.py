from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    
    def __init__(self):
        self.ticker = "DDC"
        self.ema_length = 8
        # Initialize holding tracking
        self.entry_price = None
        self.exit_target = None

    @property
    def assets(self):
        # Define which ticker(s) this strategy applies to
        return [self.ticker]

    @property
    def interval(self):
        # Set the price data interval to 5 minutes
        return "5min"
    
    def run(self, data):
        # Initialize target allocation dictionary
        allocation = {self.ticker: 0}

        # Check if there is enough data to calculate EMA
        if len(data["ohlcv"]) > self.ema_length:
            # Get the current and last closing prices and the current EMA
            current_close = data["ohlvc"][-1][self.ticker]["close"]
            previous_close = data["ohlvc"][-2][self.ticker]["close"]
            current_ema = EMA(self.ticker, data["ohlvc"], self.ema_length)[-1]

            # Check if price crossed above the EMA without an active position
            if current_close > current_ema and previous_close <= current_ema:
                log(f"Price crossed above EMA: Buying {self.ticker} at {current_close}")
                allocation[self.ticker] = 1  # Full allocation to this ticker
                self.entry_price = current_close
                self.exit_target = current_close * 2  # Setting target price for 100% gain

            # Check if the target has been reached to sell
            if self.entry_price and current_close >= self.exit_target:
                log(f"Target reached: Selling {self.ticker} at {current_close}")
                allocation[self.ticker] = 0  # Exit the position
                self.entry_price = None  # Reset entry price
                self.exit_target = None  # Reset exit target

        # If conditions to enter or exit a trade are not met, maintain current allocation
        return Targetallocation(allocation)