from typing import Protocol


class CandlestickProtocol(Protocol):
    """
    Protocol for a candlestick data structure, defining the expected attributes and methods for a candlestick.
    This protocol can be used to ensure that any class representing a candlestick adheres to this structure.
    """
    timestamp: int
    open: float
    high: float
    low: float
    close: float