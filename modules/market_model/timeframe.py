import enum

class Timeframe(enum.Enum):
    """
    Enumeration for different timeframes used in financial market analysis.
    Each member represents a specific timeframe with its corresponding duration in seconds.
    """
    M1 = 60             # 1 minute
    M5 = 5 * 60         # 5 minutes
    M15 = 15 * 60       # 15 minutes
    M30 = 30 * 60       # 30 minutes
    H1 = 60 * 60        # 1 hour
    H4 = 4 * 60 * 60    # 4 hours
    D1 = 24 * 60 * 60   # 1 day