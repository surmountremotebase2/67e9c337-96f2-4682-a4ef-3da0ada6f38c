from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker to trade
        self.ticker = "DDC"
        # Set an initial entry price to a very high value
        self.entry_price = None  
        
    @property
    def assets(self):
        # List of assets this strategy will trade
        return [self.tazer]

    @property
    def interval(self):
        # The data interval required for the strategy
        return "5min"

    def run(self, data):
        # Get the current price and EMA data
        current_price = data["ohlcv"][-1][self.ticker]["close"]
        ema_data = EMA(self.ticker, data["ohlcv"], 8)
        
        # Determine whether to enter or exit
        buy_signal = current_price <= ema_data[-1] if ema_data else False

        # Allocation logic
        if buy_signal:
            # If buy signal and no position held, buy and set entry price
            if self.entry_price is None:
                self.entry_price = current_price
                log(f"Buying {self.ticker} at price: {current_price}")
                allocation_dict = {self.ticker: 1.0}
            else:
                allocation_dict = {self.ticker: 0.0}
        else:
            # Check for take profit condition
            if self.entry_price and current_price >= 2 * self.entry_price:
                log(f"Selling {self.ticker} at price: {current_price} for 100% gain")
                self.entry_price = None  # Reset entry price
                allocation_dict = {self.ticker: 0.0}
            else:
                allocation_dict = {self.ticker: 0.0}

        return TargetAllocation(allocation_dict)