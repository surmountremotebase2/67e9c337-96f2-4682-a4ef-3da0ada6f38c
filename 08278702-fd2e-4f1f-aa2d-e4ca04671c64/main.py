from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers to trade
        self.tickers = ["SPY"]
        # Profit target for each trade
        self.profit_target = 1.3

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # Use a 5-minute interval for this strategy
        return "5min"

    def run(self, data):
        # Initial allocation dictionary
        allocation_dict = {ticker: 0 for ticker in self.tickers}
        for ticker in self.tickers:
            # Ensure there is enough data to calculate indicators
            if len(data["ohlcv"]) > 8:
                # Calculate 8-period EMA
                ema8 = EMA(ticker, data["ohlcv"], 8)
                # Get the last two closing prices
                last_close = data["ohlcv"][-1][ticker]["close"]
                second_last_close = data["ohlcv"][-2][ticker]["close"]
                # Get the last and second last EMA values
                last_ema8 = ema8[-1]
                second_last_ema8 = ema8[-2]

                # Check for a pullback by ensuring the price was below the EMA in the previous period
                # and has crossed above the EMA in the most recent period
                crossed_above = second_last_close < second_last_ema8 and last_close > last_ema8

                if crossed_above:
                    # Check if current price has achieved the target based on the buy price
                    buy_price = second_last_close  # Assume buy at the close of the previous candle
                    target_price = buy_price * self.profit_target  # Calculate target sell price
                    if last_close >= target_price:
                        # Sell signal - Allocate 0% indicating taking profit
                        allocation_dict[ticker] = 0
                        log(f"Selling {ticker} at {last_close} for a profit target of 30%")
                    else:
                        # Buy signal - Allocate 100% to this ticker
                        allocation_dict[ticker] = 1.0
                        log(f"Buying {ticker} at {last_close}")
                else:
                    # No trade signal - Allocate 0%
                    allocation_dict[ticker] = 0

        return TargetAllocation(allocation_dict)