from modules.ict_structures.candlestick_protocol import CandlestickProtocol

class Candlestick(CandlestickProtocol):
    """
    Represents a single candlestick in a financial chart, containing the open, high, low, and close prices for a specific time period.
    Attributes:
        timestamp (int): The timestamp of the candlestick.
        open (float): The opening price of the candlestick.
        high (float): The highest price during the time period of the candlestick.
        low (float): The lowest price during the time period of the candlestick.
        close (float): The closing price of the candlestick.
    """
    def __init__(self, timestamp, open_price, high_price, low_price, close_price):
        self.timestamp = timestamp
        self.open = open_price
        self.high = high_price
        self.low = low_price
        self.close = close_price