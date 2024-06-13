from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.data import OHLCV
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]  # Example with Apple stock, can be modified to use any stock
        # Define the profit target as a percentage (30% in this case)
        self.profit_target = 1.30
        # Defining the entry EMA length
        self.ema_length = 8

    @property
    def interval(self):
        # Defining the interval for the data (daily, for this example)
        return "1day"

    @property
    def assets(self):
        # Return the assets that this strategy is interested in
        return self.tickers

    @property
    def data(self):
        # Data needed for computing indicators and making decisions
        return [OHLCV(i) for i in self.tickers]

    def run(self, data):
        # Initialize an empty allocation dictionary
        allocation_dict = {}
        for ticker in self.tickers:
            # Fetch closing prices and compute 8 EMA for the current ticker
            close_prices = [d[ticker]["close"] for d in data["ohlcv"]]
            ema_8 = EMA(ticker, data["ohlcv"], length=self.ema_length)

            if not ema_8 or len(close_prices) < self.ema_length:
                # If EMA is not available or there's insufficient data, do nothing
                allocation_dict[ticker] = 0
                continue

            # Retrieve the current close price and the last computed EMA value
            current_price = close_prices[-1]
            last_ema_value = ema_8[-1]

            # Get the buy price (assuming it's stored somewhere after a buy execution)
            buy_price = ...  # This should be replaced with actual logic to fetch the purchase price

            # Determine if the strategy conditions are met
            if current_price <= last_ema_value:  # Price pulls back to 8 EMA
                # Allocate full budget to this ticker
                allocation_dict[ticker] = 1
            elif buy_price and current_price >= buy_price * self.profit_target:  # Take profit condition
                # Signal to sell the stock by setting the allocation to 0
                allocation_dict[ticker] = 0
            else:
                # Hold if none of the conditions are met
                allocation_dict[ticker] = 0

            log(f"Allocating {allocation_dict[ticker] * 100}% to {ticker}")

        # Return the target allocation based on the decision
        return TargetAllocation(allocation_dict)