from typing import List

from modules.market_model.candlestick import Candlestick
from modules.market_model.timeframe import Timeframe

class Sequence:
    """
    Represents a sequence of candlesticks, typically used for analyzing market trends and patterns.
    Attributes:
        timeframes (list): list of timeframes being tracked in the sequence.
        candlesticks (list): list of candlestick lists corresponding to the timeframes.
    """
    def __init__(self, symbol: str, timeframes: List[Timeframe]):
        Sequence.validate_timeframe_order(timeframes)
        self.timeframes = timeframes
        self.candlesticks = [[] for _ in timeframes]
        self.symbol = symbol

    @staticmethod
    def validate_timeframe_order(timeframes: List[Timeframe]):
        """
        verifies that the provided timeframes are orders from smallest to largest.
        Args:
            timeframes (list): list of timeframes to verify.
        """

        for i in range(len(timeframes) - 1):
            if timeframes[i].value >= timeframes[i + 1].value:
                raise ValueError("Timeframes must be in ascending order from smallest to largest.")
            
    def get_symbol(self) -> str:
        """
        Returns the symbol associated with the sequence.
        """
        return self.symbol
    
    def get_timeframes(self) -> List[Timeframe]:
        """
        Returns the list of timeframes being tracked in the sequence.
        """
        return self.timeframes
            
    def add_candlestick(self, timeframe: Timeframe, candlestick):
        """
        Adds a candlestick to the sequence for the specified timeframe.
        Args:
            timeframe (Timeframe): The timeframe to which the candlestick belongs.
            candlestick: The candlestick object to be added.
        """
        if timeframe not in self.timeframes:
            raise ValueError("Timeframe not found in the sequence.")
        
        index = self.timeframes.index(timeframe)
        self.candlesticks[index].append(candlestick)

    def get_candlestick(self, timeframe: Timeframe, timestamp: int) -> Candlestick:
        """
        Retrieves a specific candlestick from the sequence based on the timeframe and timestamp.
        Args:
            timeframe (Timeframe): The timeframe to which the candlestick belongs.
            timestamp (int): The timestamp of the desired candlestick.
        Returns:
            The requested candlestick object.
        """
        if timeframe not in self.timeframes:
            raise ValueError("Timeframe not found in the sequence.")
        
        index = self.timeframes.index(timeframe)

        start = 0
        end = len(self.candlesticks[index]) - 1
        while start <= end:
            mid = (start + end) // 2
            mid_timestamp = self.candlesticks[index][mid].timestamp

            if mid_timestamp == timestamp:
                return self.candlesticks[index][mid]
            elif mid_timestamp < timestamp:
                start = mid + 1
            else:
                end = mid - 1

        raise ValueError("Candlestick with the specified timestamp not found.")
    

    def get_candlesticks(self, timeframe: Timeframe, from_timestamp: int, to_timestamp: int | None = None) -> List[Candlestick]:
        """
        Retrieves a list of candlesticks from the sequence based on the timeframe and a range of timestamps.
        Args:
            timeframe (Timeframe): The timeframe to which the candlesticks belong.
            from_timestamp (int): The starting timestamp of the desired range.
            to_timestamp (int | None): The ending timestamp of the desired range. If None, retrieves all candlesticks from the starting timestamp onward.
        Returns:
            A list of candlestick objects within the specified range.
        """
        if timeframe not in self.timeframes:
            raise ValueError("Timeframe not found in the sequence.")
        
        index = self.timeframes.index(timeframe)
        candlesticks = self.candlesticks[index]

        start = 0
        end = len(candlesticks) - 1
        start_index = -1
        end_index = -1

        while start <= end:
            mid = (start + end) // 2
            mid_timestamp = candlesticks[mid].timestamp

            start_index = mid

            if mid_timestamp == from_timestamp:
                break
            elif mid_timestamp < from_timestamp:
                start = mid + 1
            else:
                end = mid - 1

        if to_timestamp is not None:
             while start <= end:
                mid = (start + end) // 2
                mid_timestamp = candlesticks[mid].timestamp

                end_index = mid

                if mid_timestamp == to_timestamp:
                    break
                elif mid_timestamp < to_timestamp:
                    start = mid + 1
                else:
                    end = mid - 1
        
        return candlesticks[start_index:end_index + 1] if to_timestamp is not None else candlesticks[start_index:]