from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Initialize with the ticker you want to trade
        self.ticker = "NVVE"
        self.profit_target = 1.3 # Target for a 30% price increase
        self.entry_price = None # To keep track of our entry price for the trade

    @property
    def assets(self):
        # Define the asset you're trading
        return [self.ticker]

    @property
    def interval(self):
        # Use 5min chart for this strategy
        return "5min"

    def run(self, data):
        # Initialize an empty allocation
        allocation_dict = {self.ticker: 0}
        
        # Checking if we have enough data
        if len(data["ohlcv"]) < 2:
            return TargetAllocation(allocation_dict)
        
        # Calculate EMA with the length of 8
        ema8 = EMA(self.ticker, data["ohlcv"], 8)
        
        # Basic price data
        latest_close = data["ohlcv"][-1][self.ticker]["close"]
        previous_close = data["ohlcv"][-2][self.ticker]["close"]
        
        # Logic to buy
        if self.entry_price is None:
            if latest_close > ema8[-1] and previous_close < ema8[-2]:
                # Price has crossed above the 8 EMA after being below it:
                allocation_dict[self.ticker] = 1  # Allocate 100% to DDC
                self.entry_price = latest_close  # Update entry price for tracking

        # If already in a position, check for sell condition
        if self.entry_price is not None:
            if latest_close >= self.entry_price * self.profit_target:
                # If the price has reached the target profit, sell(allocate 0%)
                allocation_dict[self.ticker] = 0
                self.entry_price = None  # Reset entry price to None as we've exited the trade

        # Log for debugging or information
        log(f"Latest close: {latest_close}, EMA8: {ema8[-1]}, Allocation: {allocation_dict[self.ticker]}")

        return TargetAllocation(allocation_dict)