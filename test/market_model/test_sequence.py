import pytest
import numpy as np
from typing import List, Tuple

from market_model.candlestick import Candlestick
from market_model.sequence import Sequence
from market_model.timeframe import Timeframe

from pathlib import Path

parent_dir = Path(__file__).parent

@pytest.fixture
def get_rates_m1() -> Tuple[Timeframe, List[Candlestick]]:
    file_path = parent_dir / "test_rates" / "step_index_m1.csv"
    rates_m1 = np.loadtxt(file_path, delimiter=",")
    return Timeframe.M1, [Candlestick(rate[0], rate[1], rate[2], rate[3], rate[4]) for rate in rates_m1]

@pytest.fixture
def get_rates_m15() -> Tuple[Timeframe, List[Candlestick]]:
    file_path = parent_dir / "test_rates" / "step_index_m15.csv"
    rates_m15 = np.loadtxt(file_path, delimiter=",")
    return Timeframe.M15, [Candlestick(rate[0], rate[1], rate[2], rate[3], rate[4]) for rate in rates_m15]

@pytest.fixture
def get_rates_h4() -> Tuple[Timeframe, List[Candlestick]]:
    file_path = parent_dir / "test_rates" / "step_index_h4.csv"
    rates_h4 = np.loadtxt(file_path, delimiter=",")
    return Timeframe.H4, [Candlestick(rate[0], rate[1], rate[2], rate[3], rate[4]) for rate in rates_h4]


def test_sequence_initialization():
    symbol = "Step Index"
    timeframes = [Timeframe.M1, Timeframe.M15, Timeframe.H4]
    sequence = Sequence(symbol, timeframes)
    
    assert sequence.get_symbol() == symbol
    assert sequence.get_timeframes() == timeframes
    assert all(len(candlesticks) == 0 for candlesticks in sequence.candlesticks)

def test_add_and_get_candlestick(get_rates_m1):
    symbol = "Step Index"
    timeframes = [Timeframe.M1]
    sequence = Sequence(symbol, timeframes)
    
    _, get_rates = get_rates_m1
    for candlestick in get_rates:
        sequence.add_candlestick(Timeframe.M1, candlestick)
    
    for candlestick in get_rates:
        retrieved_candlestick = sequence.get_candlestick(Timeframe.M1, candlestick.timestamp)
        assert retrieved_candlestick.timestamp == candlestick.timestamp
        assert retrieved_candlestick.open == candlestick.open
        assert retrieved_candlestick.high == candlestick.high
        assert retrieved_candlestick.low == candlestick.low
        assert retrieved_candlestick.close == candlestick.close

def test_get_candlesticks_in_range(get_rates_m1):
    symbol = "Step Index"
    timeframes = [Timeframe.M1]
    sequence = Sequence(symbol, timeframes)
    
    _, get_rates = get_rates_m1
    for candlestick in get_rates:
        sequence.add_candlestick(Timeframe.M1, candlestick)
    
    from_timestamp = get_rates[26].timestamp
    to_timestamp = get_rates[78].timestamp
    candlesticks_in_range = sequence.get_candlesticks(Timeframe.M1, from_timestamp, to_timestamp)
    
    expected_candlesticks = [candlestick for candlestick in get_rates if from_timestamp <= candlestick.timestamp <= to_timestamp]
    
    assert len(candlesticks_in_range) == len(expected_candlesticks)
    for retrieved, expected in zip(candlesticks_in_range, expected_candlesticks):
        assert retrieved.timestamp == expected.timestamp
        assert retrieved.open == expected.open
        assert retrieved.high == expected.high
        assert retrieved.low == expected.low
        assert retrieved.close == expected.close


def test_get_candlestick_not_found(get_rates_m1):
    symbol = "Step Index"
    timeframes = [Timeframe.M1]
    sequence = Sequence(symbol, timeframes)
    
    _, get_rates = get_rates_m1
    for candlestick in get_rates:
        sequence.add_candlestick(Timeframe.M1, candlestick)
    
    with pytest.raises(ValueError):
        sequence.get_candlestick(Timeframe.M1, 9999999999)


def test_window_trimming(mocker, get_rates_m15, get_rates_h4):
    symbol = "Step Index"
    timeframes = [Timeframe.M15, Timeframe.H4]
    window_weeks = 1
    sequence = Sequence(symbol, timeframes, window_weeks)

    # simulate adding candlesticks to the sequence for both timeframes
    # ensuring that the trim counter is updated and the sequence is trimmed when the overflow value is reached
    
    _, m15_rates = get_rates_m15
    _, h4_rates = get_rates_h4

    print(f"Total M15 candlesticks available: {len(m15_rates)}")
    print(f"Total H4 candlesticks available: {len(h4_rates)}")
    
    # get the last 10 days of H4 candlesticks and the corresponding M15 candlesticks to add to the sequence
    h4_candle_start_index = len(h4_rates) - 10 * 6 - 1
    print(f"H4 candle start index: {h4_candle_start_index}")
    h4_candle_to_add = h4_rates[h4_candle_start_index:]
    m15_candle_start_index = len(m15_rates) - 10 * 24 * 4 - 1
    print(f"M15 candle start index: {m15_candle_start_index}")
    m15_candle_to_add = m15_rates[m15_candle_start_index:]

    for index, m15_candle, in enumerate(m15_candle_to_add):
        sequence.add_candlestick(Timeframe.M15, m15_candle)
        if index % 16 == 0:  # add an H4 candlestick every 16 M15 candlesticks
            h4_candle = h4_candle_to_add[index // 16]

            # mock datetime.now().timestamp() to return a timestamp based on the current h4 candlestick
            mocker.patch('market_model.sequence.datetime').now.return_value.timestamp.return_value = h4_candle.timestamp + 4 * 60 * 60  # add 4 hours to the timestamp of the last M15 candlestick to simulate the passage of time

            sequence.add_candlestick(Timeframe.H4, h4_candle)

    
    # after adding the candlesticks, check that the sequence has been trimmed to the specified window of weeks
    # the number of H4 candlesticks in the sequence should be equal to the number of weeks in the window multiplied by the number of H4 candlesticks per week (7 days * 24 hours / 4 hours)
    expected_h4_candlesticks = window_weeks * 7 * 6 + 1 # trimming occurs at intervals so window size is not exact, we added 1 to match the actual number of H4 candlesticks in the sequence after trimming
    assert len(sequence.candlesticks[1]) == expected_h4_candlesticks
    # the number of M15 candlesticks in the sequence should be equal to the number of H4 candlesticks multiplied by the number of M15 candlesticks per H4 candlestick (4)
    expected_m15_candlesticks = expected_h4_candlesticks * 16 - 8  # trimming occurs at intervals so window size is not exact, we subtracted 8 to match the actual number of M15 candlesticks in the sequence after trimming
    assert len(sequence.candlesticks[0]) == expected_m15_candlesticks