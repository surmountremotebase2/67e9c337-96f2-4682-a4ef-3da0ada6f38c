from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AAPL"  # Example with Apple, but choose any ticker
        self.entry_price = None  # To keep track of the entry price
        self.profit_target = None  # To define the profit target
    
    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "5min"

    def run(self, data):
        ohlcv = data["ohlcv"]
        current_price = ohlcv[-1][self.ticker]["close"]
        ema8 = EMA(self.ticker, ohlcv, length=8)

        # If there's not enough data for EMA calculation, do nothing
        if ema8 is None or len(ema8) < 1:
            return TargetAllocation({})

        ema8_current = ema8[-1]
        allocation_dict = {self.ticker: 0}  # Default to no allocation

        # If we haven't yet bought the asset
        if self.entry_price is None:
            # Buy logic: current price pulls back to 8 EMA
            if current_price <= ema8_current:
                allocation_dict[self.ticker] = 1  # 100% of our capital to this asset
                self.entry_price = current_price
                self.profit_target = self.entry_price * 1.3  # Setting the profit target to 30% above entry
                log(f"Buying {self.ticker} at {current_price}, target {self.profit_with_target}%")
        else:
            # Sell logic: price reaches the profit target
            if current_price >= self.profit_target:
                allocation_dict[self.ticker] = 0  # Selling off the asset
                log(f"Selling {self.ticker} at {current_price}, reached profit target.")
                # Reset the entry price and profit target for the next trade
                self.entry_price = None
                self.profit_target = None

        return TargetAllocation(allocation_dict)