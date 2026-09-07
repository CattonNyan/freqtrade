#!/usr/bin/env python3
"""
scripts/download_market_data.py

Convenient CLI utility to download historical OHLCV, Open Interest,
and Funding Rate candles for Freqtrade strategies.
Supports both local native execution and Docker Compose execution.
"""

from __future__ import annotations

import argparse
import subprocess
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download historical market data for Freqtrade backtesting."
    )
    parser.add_argument(
        "--exchange",
        default="binance",
        help="Exchange name (e.g., binance, bybit, upbit). Default: binance",
    )
    parser.add_argument(
        "--pairs",
        nargs="+",
        default=["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT"],
        help="List of pairs to download. Default: BTC/USDT ETH/USDT SOL/USDT XRP/USDT",
    )
    parser.add_argument(
        "--timeframes",
        nargs="+",
        default=["5m", "15m", "1h", "1d"],
        help="List of timeframes. Default: 5m 15m 1h 1d",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=60,
        help="Number of past days of data to download. Default: 60",
    )
    parser.add_argument(
        "--trading-mode",
        choices=["spot", "futures"],
        default="spot",
        help="Trading mode (spot or futures). Default: spot",
    )
    parser.add_argument(
        "--include-oi",
        action="store_true",
        help="Include open interest candles (Requires trading-mode=futures)",
    )
    parser.add_argument(
        "--config",
        default="user_data/config.dryrun.example.json",
        help="Config file path. Default: user_data/config.dryrun.example.json",
    )
    parser.add_argument(
        "--docker",
        action="store_true",
        help="Run download command inside Docker Compose instead of local python environment",
    )
    return parser.parse_args()


def build_command(args) -> list[str]:
    cmd: list[str] = []

    if args.docker:
        cmd.extend(["docker", "compose", "run", "--rm", "download-data", "download-data"])
    else:
        cmd.extend(["freqtrade", "download-data"])

    cmd.extend(["--exchange", args.exchange])
    cmd.extend(["--days", str(args.days)])
    cmd.extend(["--timeframes"] + args.timeframes)

    # Convert pairs if futures format requested
    pairs = args.pairs
    if args.trading_mode == "futures":
        cmd.extend(["--trading-mode", "futures"])
        formatted_pairs = []
        for pair in pairs:
            if ":" not in pair:
                base, quote = pair.split("/")
                formatted_pairs.append(f"{base}/{quote}:{quote}")
            else:
                formatted_pairs.append(pair)
        cmd.extend(["--pairs"] + formatted_pairs)

        if args.include_oi:
            cmd.extend(["--candle-types", "spot", "mark", "funding_rate", "open_interest"])
    else:
        cmd.extend(["--pairs"] + pairs)

    if args.config:
        cmd.extend(["--config", args.config])

    return cmd


def main():
    args = parse_args()
    cmd = build_command(args)

    print("=" * 60)
    print("Freqtrade Market Data Downloader")
    print("=" * 60)
    print(f"Exchange     : {args.exchange}")
    print(f"Trading Mode : {args.trading_mode}")
    print(f"Timeframes   : {' '.join(args.timeframes)}")
    print(f"Days         : {args.days}")
    print(f"Command      : {' '.join(cmd)}")
    print("=" * 60)

    try:
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    except FileNotFoundError:
        executable = "docker" if args.docker else "freqtrade"
        print(f"\n[ERROR] '{executable}' command not found.")
        if not args.docker:
            print("Tip: Run with '--docker' if you have Docker installed, or activate your venv with freqtrade.")
        sys.exit(1)


if __name__ == "__main__":
    main()
