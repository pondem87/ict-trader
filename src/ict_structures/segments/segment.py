from enum import Enum
from hmac import new
import re
from turtle import st
from typing import List, Protocol

from ict_structures.candlestick_protocol import CandlestickProtocol
from ict_structures.segments.bos import BOS

class SegmentType(Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"

class Segment:
    def __init__(
            self,
            start_candle_timestamp: int,
            segment_type: SegmentType | None = None,
            last_swing_high_candle: CandlestickProtocol | None = None,
            last_swing_low_candle: CandlestickProtocol | None = None
            ):
        self.start_candle_timestamp = start_candle_timestamp
        self.end_candle_timestamp: int | None = None
        self.bosList: List[BOS] = []
        self.last_swing_high_candle: CandlestickProtocol | None = last_swing_high_candle
        self.last_swing_low_candle: CandlestickProtocol | None = last_swing_low_candle
        self.current_highest_candle: CandlestickProtocol | None = None
        self.current_lowest_candle: CandlestickProtocol | None = None
        self.segment_type: SegmentType | None = segment_type
        self.segment_state: SegmentState = UndecidedSegmentState() if segment_type is None else ExpansionSegmentState()

    @staticmethod
    def initialize_bullish_segment(
        start_candle: CandlestickProtocol,
        last_swing_low_candle: CandlestickProtocol,
        last_swing_high_candle: CandlestickProtocol
        ) -> Segment:
        new_segment = Segment(
            start_candle.timestamp,
            SegmentType.BULLISH,
            last_swing_low_candle,
            last_swing_high_candle
            )
        
        new_segment.current_highest_candle = start_candle
        return new_segment

    @staticmethod
    def initialize_bearish_segment(
        start_candle: CandlestickProtocol,
        last_swing_low_candle: CandlestickProtocol | None,
        last_swing_high_candle: CandlestickProtocol | None
        ) -> Segment:
        new_segment = Segment(
            start_candle.timestamp,
            SegmentType.BEARISH,
            last_swing_low_candle,
            last_swing_high_candle
            )
        
        new_segment.current_lowest_candle = start_candle
        return new_segment
    
    @staticmethod
    def initialize_first_segment(start_candle_timestamp: int) -> "Segment":
        return Segment(start_candle_timestamp)


    def update_segment_structure_with_candle(self, candle: CandlestickProtocol):
        self.segment_state = self.segment_state.update_segment_structure_with_candle(self, candle)

    def get_current_highest_candle(self) -> CandlestickProtocol | None:
        return self.current_highest_candle

    def get_current_lowest_candle(self) -> CandlestickProtocol | None:
        return self.current_lowest_candle
    
    def get_last_swing_high_candle(self) -> CandlestickProtocol | None:
        return self.last_swing_high_candle
    
    def get_last_swing_low_candle(self) -> CandlestickProtocol | None:
        return self.last_swing_low_candle
    
    def set_last_swing_high_candle(self, candle: CandlestickProtocol):
        self.last_swing_high_candle = candle

    def set_last_swing_low_candle(self, candle: CandlestickProtocol):
        self.last_swing_low_candle = candle


class SegmentState(Protocol):
    def update_segment_structure_with_candle(self, segment: Segment, candle: CandlestickProtocol) -> SegmentState:
        ...

class UndecidedSegmentState(SegmentState):
    def update_segment_structure_with_candle(self, segment: Segment, candle: CandlestickProtocol) -> SegmentState:
        pass

class ExpansionSegmentState(SegmentState):
    def update_segment_structure_with_candle(self, segment: Segment, candle: CandlestickProtocol) -> SegmentState:
        if segment.segment_type == SegmentType.BULLISH:
            if candle.high > segment.current_highest_candle.high:
                segment.current_highest_candle = candle
                return self
            
            if candle.low < segment.current_higest_candle.low:
                segment.last_swing_high_candle = segment.current_highest_candle
                return RetracementSegmentState()
            
        if segment.segment_type == SegmentType.BEARISH:
            if candle.low < segment.current_lowest_candle.low:
                segment.current_lowest_candle = candle
                return self
            
            if candle.high > segment.current_lowest_candle.high:
                segment.last_swing_low_candle = segment.current_lowest_candle
                return RetracementSegmentState()
            

class RetracementSegmentState(SegmentState):
    def update_segment_structure_with_candle(self, segment: Segment, candle: CandlestickProtocol) -> SegmentState:
        pass