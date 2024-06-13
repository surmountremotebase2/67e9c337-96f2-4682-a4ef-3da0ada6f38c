from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    
    def __init__(self):
        # Initialize assets to track (DDC in this example)
        self.tickers = ["DDC"]
        # Track purchase prices to decide on selling based on profit goal
        self.purchase_prices = {}

    @property
    def interval(self):
        # Set the candle interval to 5 minutes for this strategy
        return "5min"
    
    @property
    def assets(self):
        # Return the list of tickers this strategy applies to
        return self.tickers
    
    def run(self, data):
        # Initialize target allocation as empty; this will be populated based on conditions
        allocation_dict = {}
        
        # Loop through each ticker to evaluate strategy conditions
        for ticker in self.tickers:
            # Calculate the 8 EMA for the ticker
            ema_8 = EMA(ticker, data["ohlcv"], 8)
            
            # Fetch latest closing price of the ticker
            latest_close = data["ohlcv"][-1][ticker]["close"]
            
            # Check if price touches or crosses the 8 EMA
            if len(ema_8) > 0 and abs(latest_close - ema_8[-1]) / ema_8[-1] < 0.005:  # Example threshold
                # If not previously purchased, or not aiming for sale, buy.
                if ticker not in self.purchase_prices:
                    allocation_dict[ticker] = 1.0  # Full allocation
                    self.purchase_prices[ticker] = latest_close  # Track purchase price
                elif latest_close / self.purchase_prices[ticker] >= 2:  # Target 100% profit
                    allocation_dict[ticker] = 0  # Sell to take profit
                    del self.purchase_prices[ticker]  # Clear purchase price tracking

        # If no conditions met, maintain or adjust allocations as necessary
        if not allocation_dict: 
            for ticker in self.tickers:
                allocation_dict[ticker] = 0  # Example of holding/no action taken
        return TargetAllocation(allocation_dict)