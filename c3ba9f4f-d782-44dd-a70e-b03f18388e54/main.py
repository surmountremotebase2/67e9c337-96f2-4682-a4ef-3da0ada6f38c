from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker symbol for the asset you want to trade.
        self.ticker = "AAPL"
        self.fast_period = 12
        self.slow_period = 26
        self.signal_period = 9

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        # Define the time interval for the data. 
        # This could be 1day for daily data, 1hour for hourly data, etc.
        return "1day"

    def run(self, data):
        # Calculate the MACD and MACD signal line values
        macd_data = MACD(self.ticker, data["ohlcv"], self.fast_period, self.slow_period)
        
        # Initialize the stake to 0
        ticker_stake = 0
        
        if macd_data is not None and len(macd_data["MACD"]) > self.signal_period:
            # MACD line
            macd_line = macd_data["MACD"][-1]
            # MACD signal line
            signal_line = macd_data["signal"][-1]
            
            # Check if MACD line crossed above the signal line
            if macd_line > signal_line:
                log(f"Buying signal detected for {self.ticker}")
                ticker_stake = 1  # Set allocation to 1 to indicate buying the asset fully.
            else:
                log(f"Selling signal detected for {self.ticker}")
                ticker_stake = 0  # Set allocation to 0 to indicate selling the asset.

        # Return the target allocation
        return TargetAllocation({self.ticker: ticker_stake})