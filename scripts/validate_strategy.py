#!/usr/bin/env python3
"""
scripts/validate_strategy.py

Static & dynamic analyzer for Freqtrade strategies.
Checks for:
1. Required attributes (timeframe, minimal_roi, stoploss, INTERFACE_VERSION)
2. Required methods (populate_indicators, populate_entry_trend, populate_exit_trend)
3. Dangerous patterns / Lookahead bias (e.g. negative shifts like .shift(-1))
4. Syntax errors and interface conformance
"""

from __future__ import annotations

import argparse
import ast
import glob
import os
import sys
from pathlib import Path


class LookaheadVisitor(ast.NodeVisitor):
    def __init__(self):
        self.warnings: list[str] = []

    def visit_Call(self, node: ast.Call):
        # Detect df.shift(-1) or series.shift(-n)
        if isinstance(node.func, ast.Attribute) and node.func.attr == "shift":
            if node.args:
                first_arg = node.args[0]
                if isinstance(first_arg, ast.UnaryOp) and isinstance(first_arg.op, ast.USub):
                    self.warnings.append(
                        f"Line {node.lineno}: Suspicious negative shift detected (lookahead bias risk)."
                    )
        self.generic_visit(node)


def validate_file(file_path: Path) -> tuple[int, int]:
    errors = 0
    warnings = 0
    print(f"\n--- Checking Strategy: {file_path.name} ---")

    try:
        source_code = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source_code, filename=str(file_path))
    except Exception as e:
        print(f"  [ERROR] Syntax error in {file_path.name}: {e}")
        return 1, 0

    # Lookahead check
    visitor = LookaheadVisitor()
    visitor.visit(tree)
    for warn in visitor.warnings:
        print(f"  [WARNING] {warn}")
        warnings += 1

    # Find classes inheriting from IStrategy
    strategy_classes: list[ast.ClassDef] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if (isinstance(base, ast.Name) and base.id == "IStrategy") or (
                    isinstance(base, ast.Attribute) and base.attr == "IStrategy"
                ):
                    strategy_classes.append(node)

    if not strategy_classes:
        print(f"  [WARNING] No class inheriting from IStrategy found in {file_path.name}")
        warnings += 1
        return errors, warnings

    required_attrs = ["timeframe", "minimal_roi", "stoploss"]
    required_methods = ["populate_indicators", "populate_entry_trend", "populate_exit_trend"]

    for strat_cls in strategy_classes:
        print(f"  Found Strategy Class: {strat_cls.name}")
        defined_attrs = set()
        defined_methods = set()

        for item in strat_cls.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        defined_attrs.add(target.id)
            elif isinstance(item, ast.AnnAssign):
                if isinstance(item.target, ast.Name):
                    defined_attrs.add(item.target.id)
            elif isinstance(item, ast.FunctionDef):
                defined_methods.add(item.name)

        # Check required attributes
        for attr in required_attrs:
            if attr in defined_attrs:
                print(f"    [OK] Attribute '{attr}' defined")
            else:
                print(f"    [ERROR] Missing required attribute '{attr}'")
                errors += 1

        # Check INTERFACE_VERSION
        if "INTERFACE_VERSION" in defined_attrs:
            print("    [OK] INTERFACE_VERSION defined")
        else:
            print("    [WARNING] 'INTERFACE_VERSION' not explicitly defined (default is 3)")
            warnings += 1

        # Check required methods
        for meth in required_methods:
            if meth in defined_methods:
                print(f"    [OK] Method '{meth}' implemented")
            else:
                print(f"    [ERROR] Missing required method '{meth}'")
                errors += 1

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Validate Freqtrade strategies for syntax and correctness.")
    parser.add_argument(
        "targets",
        nargs="*",
        default=["user_data/strategies/*.py"],
        help="Strategy files or glob patterns to validate. Default: user_data/strategies/*.py",
    )
    args = parser.parse_args()

    matched_files: list[Path] = []
    for pattern in args.targets:
        for p in glob.glob(pattern):
            if os.path.isfile(p) and p.endswith(".py"):
                matched_files.append(Path(p))

    if not matched_files:
        print("No strategy files found matching the pattern.")
        sys.exit(0)

    total_errors = 0
    total_warnings = 0

    print("=" * 60)
    print(f"Validating {len(matched_files)} strategy file(s)...")
    print("=" * 60)

    for f in matched_files:
        errs, warns = validate_file(f)
        total_errors += errs
        total_warnings += warns

    print("\n" + "=" * 60)
    print(f"Summary: {len(matched_files)} files checked. Total Errors: {total_errors}, Warnings: {total_warnings}")
    print("=" * 60)

    if total_errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
