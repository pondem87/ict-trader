from enum import Enum

from ict_structures.candlestick_protocol import CandlestickProtocol
from ict_structures.segments.segment import SegmentType

class BOSType(Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"

class BOS:
    """
    Break of structure (ICT concept) class representing a break of structure event in price action analysis.
    """
    def __init__(
            self,
            structural_candlestick_timestamp: int,
            breaking_candlestick_timestamp: int,
            bos_type: BOSType
            ):
        self.start_candle_timestamp = structural_candlestick_timestamp
        self.breaking_candlestick_timestamp = breaking_candlestick_timestamp
        self.bos_type = bos_type

    @staticmethod
    def find_BOS(
            last_swing_high_candle: CandlestickProtocol,
            last_swing_low_candle: CandlestickProtocol,
            current_highest_candle: CandlestickProtocol,
            current_lowest_candle: CandlestickProtocol,
            current_segment_type: SegmentType
            ) -> BOS | None:
        """
        Determines if a BOS has occurred based on the last swing high and low candles and the current highest and lowest candles.
        Returns a BOS object if a BOS is detected, otherwise returns None.
        """

        # check for bullish BOS: current highest candle's high is greater than last swing high candle's high
        if current_segment_type == SegmentType.BULLISH and current_highest_candle.high > last_swing_high_candle.high:
            return BOS(
                structural_candlestick_timestamp = last_swing_high_candle.timestamp,
                breaking_candlestick_timestamp = current_highest_candle.timestamp,
                bos_type=BOSType.BULLISH
            )
        # check for bearish BOS: current lowest candle's low is less than last swing low candle's low
        if current_segment_type == SegmentType.BEARISH and current_lowest_candle.low < last_swing_low_candle.low:
            return BOS(
                structural_candlestick_timestamp=last_swing_low_candle.timestamp,
                breaking_candlestick_timestamp=current_lowest_candle.timestamp,
                bos_type=BOSType.BEARISH
            )
        return None