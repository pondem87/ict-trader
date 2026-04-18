from enum import Enum

class CHoCHType(Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"

class CHoCH:
    def __init__(self, structural_candlestick_timestamp: int, change_candlestick_timestamp: int, choch_type: CHoCHType):
        self.structural_candlestick_timestamp = structural_candlestick_timestamp
        self.change_candlestick_timestamp = change_candlestick_timestamp
        self.choch_type = choch_type