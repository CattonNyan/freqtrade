"""
scripts/seed_demo_trades.py

Seeds realistic sample dry-run trades into user_data/tradesv3.sqlite
to verify the dashboard, open trades, trade history, and KPI metrics in FreqUI.
"""

from datetime import datetime, timedelta, timezone
import sqlite3

conn = sqlite3.connect('user_data/tradesv3.sqlite')
cursor = conn.cursor()

now = datetime.now(timezone.utc)

# Clear existing sample trades if any
cursor.execute("DELETE FROM orders;")
cursor.execute("DELETE FROM trades;")
cursor.execute("DELETE FROM wallet_history;")

# 1. Closed Trade: ETH/USDT (+3.06% ROI Profit)
open_date_1 = now - timedelta(hours=5)
close_date_1 = now - timedelta(hours=2)
open_rate_1 = 2450.0
close_rate_1 = 2525.0
stake_1 = 250.0
amount_1 = stake_1 / open_rate_1
profit_ratio_1 = (close_rate_1 - open_rate_1) / open_rate_1
profit_abs_1 = stake_1 * profit_ratio_1

cursor.execute("""
INSERT INTO trades (
    id, exchange, pair, base_currency, stake_currency, is_open,
    fee_open, fee_open_cost, fee_open_currency,
    fee_close, fee_close_cost, fee_close_currency,
    open_rate, open_rate_requested, open_trade_value,
    close_rate, close_rate_requested, realized_profit, close_profit, close_profit_abs,
    stake_amount, max_stake_amount, amount, amount_requested,
    open_date, close_date,
    stop_loss, stop_loss_pct, initial_stop_loss, initial_stop_loss_pct,
    is_stop_loss_trailing, max_rate, min_rate,
    exit_reason, exit_order_status, strategy, enter_tag,
    timeframe, trading_mode, amount_precision, price_precision,
    precision_mode, precision_mode_price, contract_size, leverage, is_short,
    interest_rate, funding_fees, funding_fee_running, record_version
) VALUES (
    1, 'binance', 'ETH/USDT', 'ETH', 'USDT', 0,
    0.001, 0.25, 'USDT',
    0.001, 0.25, 'USDT',
    ?, ?, ?,
    ?, ?, ?, ?, ?,
    ?, ?, ?, ?,
    ?, ?,
    ?, -0.08, ?, -0.08,
    0, 2530.0, 2445.0,
    'roi', 'closed', 'KoreanStarterStrategy', 'trend_rsi_volume',
    15, 'spot', 4, 2,
    2, 2, 1.0, 1.0, 0,
    0.0, 0.0, 0.0, 1
)
""", (
    open_rate_1, open_rate_1, stake_1,
    close_rate_1, close_rate_1, profit_abs_1, profit_ratio_1, profit_abs_1,
    stake_1, stake_1, amount_1, amount_1,
    open_date_1.strftime('%Y-%m-%d %H:%M:%S'), close_date_1.strftime('%Y-%m-%d %H:%M:%S'),
    open_rate_1 * 0.92, open_rate_1 * 0.92
))

# 2. Closed Trade: SOL/USDT (+2.66% Trailing Stop Profit)
open_date_2 = now - timedelta(hours=8)
close_date_2 = now - timedelta(hours=3)
open_rate_2 = 101.5
close_rate_2 = 104.2
stake_2 = 250.0
amount_2 = stake_2 / open_rate_2
profit_ratio_2 = (close_rate_2 - open_rate_2) / open_rate_2
profit_abs_2 = stake_2 * profit_ratio_2

cursor.execute("""
INSERT INTO trades (
    id, exchange, pair, base_currency, stake_currency, is_open,
    fee_open, fee_open_cost, fee_open_currency,
    fee_close, fee_close_cost, fee_close_currency,
    open_rate, open_rate_requested, open_trade_value,
    close_rate, close_rate_requested, realized_profit, close_profit, close_profit_abs,
    stake_amount, max_stake_amount, amount, amount_requested,
    open_date, close_date,
    stop_loss, stop_loss_pct, initial_stop_loss, initial_stop_loss_pct,
    is_stop_loss_trailing, max_rate, min_rate,
    exit_reason, exit_order_status, strategy, enter_tag,
    timeframe, trading_mode, amount_precision, price_precision,
    precision_mode, precision_mode_price, contract_size, leverage, is_short,
    interest_rate, funding_fees, funding_fee_running, record_version
) VALUES (
    2, 'binance', 'SOL/USDT', 'SOL', 'USDT', 0,
    0.001, 0.25, 'USDT',
    0.001, 0.25, 'USDT',
    ?, ?, ?,
    ?, ?, ?, ?, ?,
    ?, ?, ?, ?,
    ?, ?,
    ?, -0.08, ?, -0.08,
    1, 105.8, 101.0,
    'trailing_stop_loss', 'closed', 'KoreanStarterStrategy', 'trend_rsi_volume',
    15, 'spot', 3, 2,
    2, 2, 1.0, 1.0, 0,
    0.0, 0.0, 0.0, 1
)
""", (
    open_rate_2, open_rate_2, stake_2,
    close_rate_2, close_rate_2, profit_abs_2, profit_ratio_2, profit_abs_2,
    stake_2, stake_2, amount_2, amount_2,
    open_date_2.strftime('%Y-%m-%d %H:%M:%S'), close_date_2.strftime('%Y-%m-%d %H:%M:%S'),
    open_rate_2 * 0.92, open_rate_2 * 0.92
))

# 3. Closed Trade: XRP/USDT (-2.41% Stoploss Loss)
open_date_3 = now - timedelta(hours=14)
close_date_3 = now - timedelta(hours=10)
open_rate_3 = 1.4500
close_rate_3 = 1.4150
stake_3 = 250.0
amount_3 = stake_3 / open_rate_3
profit_ratio_3 = (close_rate_3 - open_rate_3) / open_rate_3
profit_abs_3 = stake_3 * profit_ratio_3

cursor.execute("""
INSERT INTO trades (
    id, exchange, pair, base_currency, stake_currency, is_open,
    fee_open, fee_open_cost, fee_open_currency,
    fee_close, fee_close_cost, fee_close_currency,
    open_rate, open_rate_requested, open_trade_value,
    close_rate, close_rate_requested, realized_profit, close_profit, close_profit_abs,
    stake_amount, max_stake_amount, amount, amount_requested,
    open_date, close_date,
    stop_loss, stop_loss_pct, initial_stop_loss, initial_stop_loss_pct,
    is_stop_loss_trailing, max_rate, min_rate,
    exit_reason, exit_order_status, strategy, enter_tag,
    timeframe, trading_mode, amount_precision, price_precision,
    precision_mode, precision_mode_price, contract_size, leverage, is_short,
    interest_rate, funding_fees, funding_fee_running, record_version
) VALUES (
    3, 'binance', 'XRP/USDT', 'XRP', 'USDT', 0,
    0.001, 0.25, 'USDT',
    0.001, 0.25, 'USDT',
    ?, ?, ?,
    ?, ?, ?, ?, ?,
    ?, ?, ?, ?,
    ?, ?,
    ?, -0.08, ?, -0.08,
    0, 1.4550, 1.4120,
    'stop_loss', 'closed', 'KoreanStarterStrategy', 'trend_rsi_volume',
    15, 'spot', 1, 4,
    2, 2, 1.0, 1.0, 0,
    0.0, 0.0, 0.0, 1
)
""", (
    open_rate_3, open_rate_3, stake_3,
    close_rate_3, close_rate_3, profit_abs_3, profit_ratio_3, profit_abs_3,
    stake_3, stake_3, amount_3, amount_3,
    open_date_3.strftime('%Y-%m-%d %H:%M:%S'), close_date_3.strftime('%Y-%m-%d %H:%M:%S'),
    open_rate_3 * 0.92, open_rate_3 * 0.92
))

# 4. Active Open Trade: BTC/USDT (Currently holding and in profit!)
open_date_4 = now - timedelta(hours=1, minutes=20)
open_rate_4 = 78850.0  # slightly below current market (~79,400)
stake_4 = 300.0
amount_4 = stake_4 / open_rate_4

cursor.execute("""
INSERT INTO trades (
    id, exchange, pair, base_currency, stake_currency, is_open,
    fee_open, fee_open_cost, fee_open_currency,
    fee_close, fee_close_cost, fee_close_currency,
    open_rate, open_rate_requested, open_trade_value,
    close_rate, close_rate_requested, realized_profit, close_profit, close_profit_abs,
    stake_amount, max_stake_amount, amount, amount_requested,
    open_date, close_date,
    stop_loss, stop_loss_pct, initial_stop_loss, initial_stop_loss_pct,
    is_stop_loss_trailing, max_rate, min_rate,
    exit_reason, exit_order_status, strategy, enter_tag,
    timeframe, trading_mode, amount_precision, price_precision,
    precision_mode, precision_mode_price, contract_size, leverage, is_short,
    interest_rate, funding_fees, funding_fee_running, record_version
) VALUES (
    4, 'binance', 'BTC/USDT', 'BTC', 'USDT', 1,
    0.001, 0.30, 'USDT',
    0.001, 0.0, 'USDT',
    ?, ?, ?,
    NULL, NULL, 0.0, 0.0, 0.0,
    ?, ?, ?, ?,
    ?, NULL,
    ?, -0.08, ?, -0.08,
    0, 79450.0, 78800.0,
    NULL, NULL, 'KoreanStarterStrategy', 'trend_rsi_volume',
    15, 'spot', 5, 2,
    2, 2, 1.0, 1.0, 0,
    0.0, 0.0, 0.0, 1
)
""", (
    open_rate_4, open_rate_4, stake_4,
    stake_4, stake_4, amount_4, amount_4,
    open_date_4.strftime('%Y-%m-%d %H:%M:%S'),
    open_rate_4 * 0.92, open_rate_4 * 0.92
))

# Insert corresponding order for the active trade
cursor.execute("""
INSERT INTO orders (
    id, ft_trade_id, ft_order_side, ft_pair, ft_is_open, ft_amount, ft_price,
    order_id, status, symbol, order_type, side, price, average, amount, filled, remaining, cost,
    order_date, order_filled_date, order_update_date, funding_fee, ft_fee_base, ft_order_tag
) VALUES (
    1, 4, 'buy', 'BTC/USDT', 0, ?, ?,
    'demo_order_btc_1', 'closed', 'BTC/USDT', 'limit', 'buy', ?, ?, ?, ?, 0.0, ?,
    ?, ?, ?, 0.0, 0.001, 'trend_rsi_volume'
)
""", (
    amount_4, open_rate_4,
    open_rate_4, open_rate_4, amount_4, amount_4, stake_4,
    open_date_4.strftime('%Y-%m-%d %H:%M:%S'),
    open_date_4.strftime('%Y-%m-%d %H:%M:%S'),
    open_date_4.strftime('%Y-%m-%d %H:%M:%S')
))

conn.commit()
conn.close()
print("Successfully seeded 1 active open trade (BTC/USDT) and 3 closed trades (ETH, SOL, XRP)!")
