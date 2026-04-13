from datetime import datetime
from typing import List
from xmlrpc.client import boolean

from market_model.candlestick import Candlestick
from market_model.timeframe import Timeframe

DEFAULT_WINDOW_WEEKS = 12
TRIM_COUNTER_OVERFLOW_VALUE = 10

class Sequence:
    """
    Represents a sequence of candlesticks, typically used for analyzing market trends and patterns.
    Attributes:
        timeframes (list): list of timeframes being tracked in the sequence.
        candlesticks (list): list of candlestick lists corresponding to the timeframes.
    """
    def __init__(self, symbol: str, timeframes: List[Timeframe], window_weeks: int = DEFAULT_WINDOW_WEEKS):
        Sequence.validate_timeframe_order(timeframes)
        self.timeframes = timeframes
        self.candlesticks = [[] for _ in timeframes]
        self.symbol = symbol
        self.window_weeks = window_weeks
        self.trim_counter = 0


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

        # update trim counter when a new candlestick is added to the sequence for the largest timeframe
        # if the trim counter has reached the overflow value, trim the sequence to the specified window of weeks
        if index == len(self.timeframes) - 1:
            if self.check_trim_counter_overflow_and_update():
                self.trim_sequence_to_window()

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

        # using binary search to find the candlestick with the specified timestamp
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

        # using binary search to find the starting and ending indices of the candlesticks within the specified timestamp range
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

        start = 0
        end = len(candlesticks) - 1

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
    
    def trim_sequence_to_window(self) -> None:
        """
        Trims the sequence to only include candlesticks within the specified window of weeks.
        This method should be called periodically to ensure that the sequence does not grow indefinitely.
        """
        # Implementation would involve calculating the cutoff timestamp based on the current time and window_weeks,
        # and then removing any candlesticks from each timeframe that are older than the cutoff timestamp.
        earliest_timestamp = int(datetime.now().timestamp()) - self.window_weeks * 7 * 24 * 60 * 60

        for index, _ in enumerate(self.timeframes):
            start_index = 0

            for i, candlestick in enumerate(self.candlesticks[index]):
                if candlestick.timestamp >= earliest_timestamp:
                    start_index = i
                    break

            self.candlesticks[index] = self.candlesticks[index][start_index:]

    def check_trim_counter_overflow_and_update(self) -> boolean:
        """
        Checks if the trim counter has reached the overflow value and updates it accordingly.

        Returns:
            boolean: True if the trim counter has reached the overflow value and was reset, False otherwise.
        """

        self.trim_counter += 1

        if self.trim_counter < int(TRIM_COUNTER_OVERFLOW_VALUE):
            return False
        else:
            self.trim_counter = 0
            return True
