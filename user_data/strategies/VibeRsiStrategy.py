# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
import numpy as np
import pandas as pd
from pandas import DataFrame
from freqtrade.strategy import IStrategy
import talib.abstract as ta
from technical import qtpylib


class VibeRsiStrategy(IStrategy):
    """
    VibeRsiStrategy: A clean RSI & EMA trend-following strategy for Freqtrade.
    - Timeframe: 5m
    - Indicator: RSI(14), EMA(20), EMA(50)
    - Entry: RSI < 30 and EMA20 > EMA50
    - Exit: RSI > 70
    - Stoploss: -5%
    """

    INTERFACE_VERSION = 3

    # Define timeframe for this strategy
    timeframe = "5m"

    # Can this strategy go short?
    can_short: bool = False

    # Minimal ROI designed for the strategy
    minimal_roi = {
        "60": 0.01,
        "30": 0.02,
        "0": 0.04
    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.05

    # Trailing stoploss
    trailing_stop = False

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Calculate indicators to be used by the strategy.
        """
        # RSI (Relative Strength Index)
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)

        # Exponential Moving Averages (Trend indicators)
        dataframe["ema20"] = ta.EMA(dataframe, timeperiod=20)
        dataframe["ema50"] = ta.EMA(dataframe, timeperiod=50)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Entry signal logic based on indicators.
        """
        dataframe.loc[
            (
                (dataframe["rsi"] < 30) &
                (dataframe["ema20"] > dataframe["ema50"]) &
                (dataframe["volume"] > 0)
            ),
            "enter_long"
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Exit signal logic based on indicators.
        """
        dataframe.loc[
            (
                (dataframe["rsi"] > 70) &
                (dataframe["volume"] > 0)
            ),
            "exit_long"
        ] = 1

        return dataframe
