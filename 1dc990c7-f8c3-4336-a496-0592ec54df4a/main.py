from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Set the tickers for the assets you want to trade. Modify this list as per your requirements.
        self.tickers = ["AAPL", "GOOGL", "MSFT"]

    @property
    def assets(self):
        # The assets property returns the list of tickers that the strategy will operate on.
        return self.tickers

    @property
    def interval(self):
        # This strategy operates on a 5 minute interval chart.
        return "5min"

    def run(self, data):
        allocation_dict = {}

        for ticker in self.tickers:
            # Compute the 8 period EMA for each ticker.
            ema_8 = EMA(ticker, data["ohlcv"], 8)
            
            # If EMA calculation is successful and has enough data points
            if ema_8 is not None and len(ema_8) > 0:
                current_price = data["ohlcv"][-1][ticker]["close"]
                ema_price = ema_8[-1]

                # Calculate the target sell price as a 30% profit over the EMA price.
                target_sell_price = ema_price * 1.30

                # Check if the current price is within 0.5% of the EMA price as a buy signal.
                if abs(current_price - ema_price) / ema_price <= 0.005:
                    allocation_dict[ticker] = {"action": "buy", "target_sell_price": target_sell_price}
                    log(f"Buying {ticker} at {current_price}, targeting a sell at {target_sell_price}.")
                else:
                    # No action specified for this ticker in this run.
                    allocation_dict[ticker] = {"action": "hold"}
            else:
                log(f"EMA calculation failed or not enough data for {ticker}.")

        # In this strategy example, we're not directly returning a TargetAllocation object because we're focusing on 
        # logic for buy signals and target sell prices. Actual allocation will depend 
        # on integrating this logic within your larger trading system.
        return allocation_dict