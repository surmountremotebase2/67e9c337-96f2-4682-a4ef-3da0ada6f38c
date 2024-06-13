from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # The ticker we are interested in
        self.tickers = ["DDC"]
        # Initial purchase price for calculating the profit
        self.purchase_price = None

    @property
    def interval(self):
        # Set the interval to 5min for high-frequency data
        return "5min"

    @property
e    def assets(self):
        # Return the list of tickers the strategy operates on
        return self.tickers

    def run(self, data):
        # Fetch the 5min ohlcv data for DDC
        ohlcv_data = data["ohlcv"]
        ddc_data = ohlcv_data[-1]["DDC"]  # Get the most recent data
        close_price = ddc_data["close"]

        # Determine the 8-period EMA for DDC
        ema_8 = EMA("DDC", ohlcv_data, 8)[-1]

        # Check if we already have a position
        if self.purchase_price is None:
            # Check if the price touches the 8 EMA
            if close_price <= ema_8:
                # Buy condition met, save purchase price and set allocation to buy
                self.purchase-price = close_price
                # Assuming full investment in DDC with this signal
                return TargetAllocation({"DDC": 1.0})
            else:
                # No action required if condition not met
                return TargetAllocation({})
        else:
            # Sell condition based on profit target
            if close_price >= 2 * self.purchase_price:
                # Profit target met, reset purchase price to None and sell
                self.purchase_price = None
                # Assuming selling off all holdings of DDC
                return TargetAllocation({"DDC": 0.0})
            else:
                # Hold if not reached target
                return TargetAllocation({"DDC": 1.0})  # Maintain current position

        # Default action if none of the above conditions are met
        return TargetAllocation({})