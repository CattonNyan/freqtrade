"""
tests/strategy/test_custom_user_strategies.py

Unit test suite for custom user strategies:
- MultiTimeframeAtrStrategy
- OpenInterestTrendStrategy
- KoreanStarterStrategy
- VibeRsiStrategy

Compatible with standard unittest and pytest.
Executes static AST structure checks and interface verification.
"""

from __future__ import annotations

import ast
from pathlib import Path
import unittest


class TestCustomUserStrategies(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.strategies_dir = Path("user_data/strategies")
        cls.strategy_files = [
            "KoreanStarterStrategy.py",
            "MultiTimeframeAtrStrategy.py",
            "OpenInterestTrendStrategy.py",
            "VibeRsiStrategy.py",
        ]

    def test_all_strategy_files_exist(self):
        """Ensure all 4 custom strategy files exist in user_data/strategies."""
        for filename in self.strategy_files:
            file_path = self.strategies_dir / filename
            self.assertTrue(file_path.exists(), f"Strategy file missing: {filename}")

    def test_strategy_ast_structure_and_interface(self):
        """Verify that all strategies inherit from IStrategy and define required attributes/methods."""
        required_attrs = {"timeframe", "minimal_roi", "stoploss"}
        required_methods = {"populate_indicators", "populate_entry_trend", "populate_exit_trend"}

        for filename in self.strategy_files:
            file_path = self.strategies_dir / filename
            code = file_path.read_text(encoding="utf-8")
            tree = ast.parse(code, filename=filename)

            # Find strategy class
            strategy_classes = [
                node
                for node in tree.body
                if isinstance(node, ast.ClassDef)
                and any(
                    (isinstance(b, ast.Name) and b.id == "IStrategy")
                    or (isinstance(b, ast.Attribute) and b.attr == "IStrategy")
                    for b in node.bases
                )
            ]
            self.assertTrue(
                len(strategy_classes) >= 1,
                f"No IStrategy class found in {filename}",
            )

            strat_cls = strategy_classes[0]
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

            # Assert required attributes
            for attr in required_attrs:
                self.assertIn(
                    attr,
                    defined_attrs,
                    f"{filename}: Missing required attribute '{attr}'",
                )

            # Assert required methods
            for meth in required_methods:
                self.assertIn(
                    meth,
                    defined_methods,
                    f"{filename}: Missing required method '{meth}'",
                )

    def test_no_negative_shifts_lookahead(self):
        """Ensure no strategy contains dangerous negative shift calls (.shift(-n))."""
        for filename in self.strategy_files:
            file_path = self.strategies_dir / filename
            code = file_path.read_text(encoding="utf-8")
            tree = ast.parse(code, filename=filename)

            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    if node.func.attr == "shift" and node.args:
                        arg = node.args[0]
                        if isinstance(arg, ast.UnaryOp) and isinstance(arg.op, ast.USub):
                            self.fail(f"Lookahead bias detected in {filename} at line {node.lineno}")


if __name__ == "__main__":
    unittest.main()
