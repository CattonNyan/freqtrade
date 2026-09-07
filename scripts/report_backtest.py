#!/usr/bin/env python3
"""
scripts/report_backtest.py

Parses Freqtrade backtest result JSON files and produces clean, readable
summary reports in Terminal, Markdown (.md), and optionally CSV format.
Extracts Sharpe, Sortino, MDD, Win Rate, Profit Factor, Pair metrics, and Exit reasons.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from pathlib import Path


def find_latest_backtest_file() -> Path | None:
    results_dir = Path("user_data/backtest_results")
    if not results_dir.exists():
        return None
    files = list(results_dir.glob(".last_result.json"))
    if files:
        try:
            last_meta = json.loads(files[0].read_text(encoding="utf-8"))
            filename = last_meta.get("latest_backtest")
            if filename and (results_dir / filename).exists():
                return results_dir / filename
        except Exception:
            pass

    # Fallback to newest backtest-result*.json
    candidates = sorted(
        results_dir.glob("backtest-result*.json"),
        key=os.path.getmtime,
        reverse=True,
    )
    # Ignore .meta.json files
    candidates = [f for f in candidates if not f.name.endswith(".meta.json")]
    return candidates[0] if candidates else None


def format_pct(val: float | None) -> str:
    if val is None:
        return "N/A"
    return f"{val * 100:.2f}%" if abs(val) < 10 else f"{val:.2f}%"


def generate_markdown(strat_name: str, strat_data: dict) -> str:
    lines = []
    lines.append(f"# 📊 Backtest Performance Summary: {strat_name}\n")

    # Overall metrics
    total_trades = strat_data.get("total_trades", 0)
    wins = strat_data.get("wins", 0)
    losses = strat_data.get("losses", 0)
    draws = strat_data.get("draws", 0)
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0.0

    profit_mean = strat_data.get("profit_mean_pct", 0.0)
    profit_total = strat_data.get("profit_total_pct", 0.0)
    profit_total_abs = strat_data.get("profit_total_abs", 0.0)
    profit_factor = strat_data.get("profit_factor", 0.0)

    mdd_pct = strat_data.get("max_drawdown_account", 0.0) * 100
    mdd_abs = strat_data.get("max_drawdown_abs", 0.0)
    sharpe = strat_data.get("sharpe", None)
    sortino = strat_data.get("sortino", None)
    calmar = strat_data.get("calmar", None)

    lines.append("## 1. Key Performance Indicators (KPI)")
    lines.append("| Metric | Value |")
    lines.append("| :--- | :--- |")
    lines.append(f"| **Total Trades** | {total_trades} (Win: {wins}, Loss: {losses}, Draw: {draws}) |")
    lines.append(f"| **Win Rate** | **{win_rate:.2f}%** |")
    lines.append(f"| **Profit Factor** | **{profit_factor:.2f}** |")
    lines.append(f"| **Total Profit %** | **{profit_total:.2f}%** |")
    lines.append(f"| **Total Profit (Fiat/Stake)** | {profit_total_abs:,.2f} |")
    lines.append(f"| **Avg Trade Profit** | {profit_mean:.2f}% |")
    lines.append(f"| **Max Drawdown (Account)** | **{mdd_pct:.2f}%** ({mdd_abs:,.2f}) |")
    lines.append(f"| **Sharpe Ratio** | {f'{sharpe:.2f}' if sharpe is not None else 'N/A'} |")
    lines.append(f"| **Sortino Ratio** | {f'{sortino:.2f}' if sortino is not None else 'N/A'} |")
    lines.append(f"| **Calmar Ratio** | {f'{calmar:.2f}' if calmar is not None else 'N/A'} |")
    lines.append("")

    # Exit reason summary
    exit_reasons = strat_data.get("exit_reason_summary", [])
    if exit_reasons:
        lines.append("## 2. Exit Reasons Breakdown")
        lines.append("| Exit Reason | Trades | Win Rate | Profit Total % |")
        lines.append("| :--- | :--- | :--- | :--- |")
        for r in exit_reasons:
            reason = r.get("exit_reason", "unknown")
            trades = r.get("trades", 0)
            w = r.get("wins", 0)
            wr = (w / trades * 100) if trades > 0 else 0
            p_tot = r.get("profit_total_pct", 0)
            lines.append(f"| `{reason}` | {trades} | {wr:.1f}% | {p_tot:.2f}% |")
        lines.append("")

    # Pair results
    results_per_pair = strat_data.get("results_per_pair", [])
    if results_per_pair:
        lines.append("## 3. Results by Pair")
        lines.append("| Pair | Trades | Win Rate | Profit % | Profit (Abs) |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for p in results_per_pair:
            key = p.get("key", "")
            t = p.get("trades", 0)
            w = p.get("wins", 0)
            wr = (w / t * 100) if t > 0 else 0
            p_pct = p.get("profit_total_pct", 0)
            p_abs = p.get("profit_total_abs", 0)
            lines.append(f"| **{key}** | {t} | {wr:.1f}% | {p_pct:.2f}% | {p_abs:,.2f} |")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate clean summary report from Freqtrade backtest result JSON.")
    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="Path to backtest-result*.json. Defaults to the latest result in user_data/backtest_results",
    )
    parser.add_argument(
        "--output-md",
        "-o",
        default=None,
        help="Path to save markdown report (e.g. backtest_report.md)",
    )
    args = parser.parse_args()

    target_file = Path(args.file) if args.file else find_latest_backtest_file()

    if not target_file or not target_file.exists():
        print("[INFO] No backtest result file found. Run a backtest first!")
        print("Example: freqtrade backtesting --strategy MultiTimeframeAtrStrategy")
        sys.exit(0)

    print(f"Loading backtest result from: {target_file}")
    data = json.loads(target_file.read_text(encoding="utf-8"))

    strategy_data = data.get("strategy", {})
    if not strategy_data:
        print("[ERROR] No strategy results found in JSON file.")
        sys.exit(1)

    all_reports = []
    for strat_name, s_data in strategy_data.items():
        md = generate_markdown(strat_name, s_data)
        all_reports.append(md)
        print("\n" + md)

    final_md = "\n\n---\n\n".join(all_reports)

    if args.output_md:
        out_path = Path(args.output_md)
        out_path.write_text(final_md, encoding="utf-8")
        print(f"\n[SUCCESS] Markdown report saved to: {out_path.resolve()}")


if __name__ == "__main__":
    main()
