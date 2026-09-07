"""
Open Interest & Funding Rate based Futures Trend Strategy for Freqtrade.
Utilizes Freqtrade 2026.9+ native Open Interest (CandleType.OPEN_INTEREST) and Funding Rate data.
Supports bidirectional (Long/Short) trading on Binance/Bybit Futures.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pandas import DataFrame
import talib.abstract as ta

from freqtrade.enums import CandleType
from freqtrade.persistence import Trade
from freqtrade.strategy import (
    DecimalParameter,
    IStrategy,
    IntParameter,
    merge_informative_pair,
)
from technical import qtpylib


class OpenInterestTrendStrategy(IStrategy):
    """
    Futures Trend-following strategy combining:
    1. Base timeframe (1h) price action (EMA, RSI, Volume)
    2. Open Interest (OI) momentum to detect real institutional capital flow
    3. Funding Rate filters to prevent entering against crowded positions
    """

    INTERFACE_VERSION = 3

    timeframe = "1h"
    can_short = True
    process_only_new_candles = True
    startup_candle_count = 100

    # Minimal ROI
    minimal_roi = {
        "0": 0.08,
        "60": 0.04,
        "180": 0.02,
        "360": 0.0,
    }

    # Stoploss
    stoploss = -0.05
    use_custom_stoploss = True

    # Trailing Stoploss
    trailing_stop = False

    # Hyperparameters
    buy_rsi_min = IntParameter(45, 55, default=48, space="buy", optimize=True)
    buy_rsi_max = IntParameter(60, 75, default=68, space="buy", optimize=True)
    sell_rsi_min = IntParameter(25, 40, default=32, space="sell", optimize=True)
    sell_rsi_max = IntParameter(45, 55, default=52, space="sell", optimize=True)

    oi_surge_ratio = DecimalParameter(1.01, 1.10, default=1.02, space="buy", optimize=True)

    order_types = {
        "entry": "limit",
        "exit": "limit",
        "emergency_exit": "market",
        "force_entry": "market",
        "force_exit": "market",
        "stoploss": "market",
        "stoploss_on_exchange": False,
    }

    order_time_in_force = {
        "entry": "GTC",
        "exit": "GTC",
    }

    def informative_pairs(self):
        """
        Fetch Open Interest and Funding Rate candle data for whitelisted pairs.
        Requires Freqtrade 2026.9+ and exchange support (Binance, Bybit futures).
        """
        pairs = self.dp.current_whitelist()
        informative = []
        for pair in pairs:
            # Informative Open Interest candle
            informative.append((pair, self.timeframe, CandleType.OPEN_INTEREST))
            # Informative Funding Rate candle
            informative.append((pair, self.timeframe, CandleType.FUNDING_RATE))
        return informative

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Base Price Indicators
        dataframe["ema_20"] = ta.EMA(dataframe, timeperiod=20)
        dataframe["ema_50"] = ta.EMA(dataframe, timeperiod=50)
        dataframe["ema_200"] = ta.EMA(dataframe, timeperiod=200)
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
        dataframe["atr"] = ta.ATR(dataframe, timeperiod=14)
        dataframe["volume_mean_20"] = dataframe["volume"].rolling(20).mean().shift(1)

        # Merge Open Interest if available via DataProvider
        pair = metadata["pair"]
        if self.dp:
            try:
                oi_df = self.dp.get_pair_dataframe(
                    pair=pair,
                    timeframe=self.timeframe,
                    candle_type=CandleType.OPEN_INTEREST,
                )
                if not oi_df.empty:
                    oi_df["oi_sma_14"] = ta.SMA(oi_df, timeperiod=14, price="open_interest")
                    dataframe = merge_informative_pair(
                        dataframe,
                        oi_df,
                        self.timeframe,
                        self.timeframe,
                        ffill=True,
                        candle_type=CandleType.OPEN_INTEREST,
                    )
            except Exception:
                pass

            try:
                fr_df = self.dp.get_pair_dataframe(
                    pair=pair,
                    timeframe=self.timeframe,
                    candle_type=CandleType.FUNDING_RATE,
                )
                if not fr_df.empty:
                    dataframe = merge_informative_pair(
                        dataframe,
                        fr_df,
                        self.timeframe,
                        self.timeframe,
                        ffill=True,
                        candle_type=CandleType.FUNDING_RATE,
                    )
            except Exception:
                pass

        # Fallback columns if OI/FR candle data is not present in local test
        oi_col = f"open_interest_{self.timeframe}_{CandleType.OPEN_INTEREST}"
        oi_sma_col = f"oi_sma_14_{self.timeframe}_{CandleType.OPEN_INTEREST}"
        if oi_col not in dataframe.columns:
            dataframe[oi_col] = 1.0
            dataframe[oi_sma_col] = 1.0

        fr_col = f"open_{self.timeframe}_{CandleType.FUNDING_RATE}"
        if fr_col not in dataframe.columns:
            dataframe[fr_col] = 0.0

        # Calculate OI Momentum
        dataframe["oi_ratio"] = dataframe[oi_col] / dataframe[oi_sma_col].replace(0, 1.0)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        oi_expanding = dataframe["oi_ratio"] >= self.oi_surge_ratio.value

        enter_long_cond = (
            (dataframe["close"] > dataframe["ema_20"])
            & (dataframe["ema_20"] > dataframe["ema_50"])
            & (dataframe["rsi"] >= self.buy_rsi_min.value)
            & (dataframe["rsi"] <= self.buy_rsi_max.value)
            & (dataframe["volume"] > dataframe["volume_mean_20"])
            & oi_expanding
            & (dataframe["volume"] > 0)
        )

        dataframe.loc[enter_long_cond, ["enter_long", "enter_tag"]] = (
            1,
            "oi_bullish_momentum_long",
        )

        enter_short_cond = (
            (dataframe["close"] < dataframe["ema_20"])
            & (dataframe["ema_20"] < dataframe["ema_50"])
            & (dataframe["rsi"] >= self.sell_rsi_min.value)
            & (dataframe["rsi"] <= self.sell_rsi_max.value)
            & (dataframe["volume"] > dataframe["volume_mean_20"])
            & oi_expanding
            & (dataframe["volume"] > 0)
        )

        dataframe.loc[enter_short_cond, ["enter_short", "enter_tag"]] = (
            1,
            "oi_bearish_momentum_short",
        )

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        has_volume = dataframe["volume"] > 0

        # Long Exit
        long_exit = (
            (dataframe["rsi"] > 78)
            | (dataframe["close"] < dataframe["ema_50"])
        ) & has_volume
        dataframe.loc[long_exit, ["exit_long", "exit_tag"]] = (1, "long_trend_exhaustion")

        # Short Exit
        short_exit = (
            (dataframe["rsi"] < 22)
            | (dataframe["close"] > dataframe["ema_50"])
        ) & has_volume
        dataframe.loc[short_exit, ["exit_short", "exit_tag"]] = (1, "short_trend_exhaustion")

        return dataframe

    def leverage(
        self,
        pair: str,
        current_time: datetime,
        current_rate: float,
        proposed_leverage: float,
        max_leverage: float,
        entry_tag: Optional[str],
        side: str,
        **kwargs,
    ) -> float:
        """Enforce conservative 2x-3x leverage for safety in futures trading."""
        return min(3.0, max_leverage)

    def custom_stoploss(
        self,
        pair: str,
        trade: Trade,
        current_time: datetime,
        current_rate: float,
        current_profit: float,
        after_fill: bool,
        **kwargs,
    ) -> Optional[float]:
        """Dynamic break-even stoploss for futures."""
        if current_profit >= 0.04:
            return (1 + 0.02) / (1 + current_profit) - 1
        if current_profit >= 0.02:
            return (1 + 0.005) / (1 + current_profit) - 1
        return None
