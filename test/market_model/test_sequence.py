import pytest

from market_model.candlestick import Candlestick
from market_model.sequence import Sequence
from market_model.timeframe import Timeframe

@pytest.fixture
def get_rates():
    rates = [
       (1776029100, 8044.2, 8044.5, 8043.5, 8044.5, 60, 1, 0),
       (1776029160, 8044.4, 8044.9, 8043.8, 8044.7, 60, 1, 0),
       (1776029220, 8044.6, 8044.6, 8043.1, 8043.1, 60, 1, 0),
       (1776029280, 8043.2, 8043.7, 8043.1, 8043.3, 60, 1, 0),
       (1776029340, 8043.4, 8043.4, 8042.3, 8042.9, 60, 1, 0),
       (1776029400, 8042.8, 8043. , 8042.3, 8042.9, 60, 1, 0),
       (1776029460, 8042.8, 8042.8, 8041.8, 8041.9, 60, 1, 0),
       (1776029520, 8042. , 8042.2, 8041.5, 8041.7, 60, 1, 0),
       (1776029580, 8041.8, 8042.9, 8041.6, 8042.1, 60, 1, 0),
       (1776029640, 8042. , 8042.3, 8042. , 8042.3,  8, 1, 0)
       ]
    
    return [Candlestick(rate[0], rate[1], rate[2], rate[3], rate[4]) for rate in rates]


def test_sequence_initialization():
    symbol = "BTCUSD"
    timeframes = [Timeframe.M1, Timeframe.M15, Timeframe.H4]
    sequence = Sequence(symbol, timeframes)
    
    assert sequence.get_symbol() == symbol
    assert sequence.get_timeframes() == timeframes
    assert all(len(candlesticks) == 0 for candlesticks in sequence.candlesticks)

def test_add_and_get_candlestick(get_rates):
    symbol = "BTCUSD"
    timeframes = [Timeframe.M1]
    sequence = Sequence(symbol, timeframes)
    
    for candlestick in get_rates:
        sequence.add_candlestick(Timeframe.M1, candlestick)
    
    for candlestick in get_rates:
        retrieved_candlestick = sequence.get_candlestick(Timeframe.M1, candlestick.timestamp)
        assert retrieved_candlestick.timestamp == candlestick.timestamp
        assert retrieved_candlestick.open == candlestick.open
        assert retrieved_candlestick.high == candlestick.high
        assert retrieved_candlestick.low == candlestick.low
        assert retrieved_candlestick.close == candlestick.close

def test_get_candlesticks_in_range(get_rates):
    symbol = "BTCUSD"
    timeframes = [Timeframe.M1]
    sequence = Sequence(symbol, timeframes)
    
    for candlestick in get_rates:
        sequence.add_candlestick(Timeframe.M1, candlestick)
    
    from_timestamp = get_rates[2].timestamp
    to_timestamp = get_rates[5].timestamp
    candlesticks_in_range = sequence.get_candlesticks(Timeframe.M1, from_timestamp, to_timestamp)
    
    expected_candlesticks = [candlestick for candlestick in get_rates if from_timestamp <= candlestick.timestamp <= to_timestamp]
    
    assert len(candlesticks_in_range) == len(expected_candlesticks)
    for retrieved, expected in zip(candlesticks_in_range, expected_candlesticks):
        assert retrieved.timestamp == expected.timestamp
        assert retrieved.open == expected.open
        assert retrieved.high == expected.high
        assert retrieved.low == expected.low
        assert retrieved.close == expected.close