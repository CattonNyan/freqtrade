"""
scripts/seed_trades_internal.py

Uses Freqtrade's native Trade ORM to insert realistic demo trades.
Run inside docker container to ensure 100% schema and enum compatibility.
"""

from datetime import datetime, timedelta, timezone
from freqtrade.configuration import Configuration
from freqtrade.persistence import Trade, Order, init_db
from freqtrade.enums import TradingMode

# Load configuration and init db
db_url = "sqlite:////freqtrade/user_data/tradesv3.sqlite"
init_db(db_url)

# Clear existing trades
Trade.session.query(Order).delete()
Trade.session.query(Trade).delete()
Trade.session.commit()

now = datetime.now(timezone.utc)

# 1. Closed Trade: ETH/USDT (+3.06% ROI Profit)
trade_eth = Trade(
    exchange='binance',
    pair='ETH/USDT',
    base_currency='ETH',
    stake_currency='USDT',
    is_open=False,
    open_rate=2450.0,
    open_rate_requested=2450.0,
    open_trade_value=250.0,
    close_rate=2525.0,
    close_rate_requested=2525.0,
    realized_profit=7.65,
    close_profit=0.0306,
    close_profit_abs=7.65,
    stake_amount=250.0,
    max_stake_amount=250.0,
    amount=250.0 / 2450.0,
    amount_requested=250.0 / 2450.0,
    open_date=now - timedelta(hours=5),
    close_date=now - timedelta(hours=2),
    fee_open=0.001,
    fee_open_cost=0.25,
    fee_open_currency='USDT',
    fee_close=0.001,
    fee_close_cost=0.25,
    fee_close_currency='USDT',
    stop_loss=2450.0 * 0.92,
    stop_loss_pct=-0.08,
    initial_stop_loss=2450.0 * 0.92,
    initial_stop_loss_pct=-0.08,
    max_rate=2530.0,
    min_rate=2445.0,
    exit_reason='roi',
    strategy='KoreanStarterStrategy',
    enter_tag='trend_rsi_volume',
    timeframe=15,
    trading_mode=TradingMode.SPOT,
    amount_precision=4,
    price_precision=2,
    precision_mode=2,
    precision_mode_price=2,
    contract_size=1.0,
    leverage=1.0,
    is_short=False,
)
Trade.session.add(trade_eth)

# 2. Closed Trade: SOL/USDT (+2.66% Trailing Stop Profit)
trade_sol = Trade(
    exchange='binance',
    pair='SOL/USDT',
    base_currency='SOL',
    stake_currency='USDT',
    is_open=False,
    open_rate=101.5,
    open_rate_requested=101.5,
    open_trade_value=250.0,
    close_rate=104.2,
    close_rate_requested=104.2,
    realized_profit=6.65,
    close_profit=0.0266,
    close_profit_abs=6.65,
    stake_amount=250.0,
    max_stake_amount=250.0,
    amount=250.0 / 101.5,
    amount_requested=250.0 / 101.5,
    open_date=now - timedelta(hours=8),
    close_date=now - timedelta(hours=3),
    fee_open=0.001,
    fee_open_cost=0.25,
    fee_open_currency='USDT',
    fee_close=0.001,
    fee_close_cost=0.25,
    fee_close_currency='USDT',
    stop_loss=101.5 * 0.92,
    stop_loss_pct=-0.08,
    initial_stop_loss=101.5 * 0.92,
    initial_stop_loss_pct=-0.08,
    is_stop_loss_trailing=True,
    max_rate=105.8,
    min_rate=101.0,
    exit_reason='trailing_stop_loss',
    strategy='KoreanStarterStrategy',
    enter_tag='trend_rsi_volume',
    timeframe=15,
    trading_mode=TradingMode.SPOT,
    amount_precision=3,
    price_precision=2,
    precision_mode=2,
    precision_mode_price=2,
    contract_size=1.0,
    leverage=1.0,
    is_short=False,
)
Trade.session.add(trade_sol)

# 3. Closed Trade: XRP/USDT (-2.41% Stoploss Loss)
trade_xrp = Trade(
    exchange='binance',
    pair='XRP/USDT',
    base_currency='XRP',
    stake_currency='USDT',
    is_open=False,
    open_rate=1.4500,
    open_rate_requested=1.4500,
    open_trade_value=250.0,
    close_rate=1.4150,
    close_rate_requested=1.4150,
    realized_profit=-6.03,
    close_profit=-0.0241,
    close_profit_abs=-6.03,
    stake_amount=250.0,
    max_stake_amount=250.0,
    amount=250.0 / 1.4500,
    amount_requested=250.0 / 1.4500,
    open_date=now - timedelta(hours=14),
    close_date=now - timedelta(hours=10),
    fee_open=0.001,
    fee_open_cost=0.25,
    fee_open_currency='USDT',
    fee_close=0.001,
    fee_close_cost=0.25,
    fee_close_currency='USDT',
    stop_loss=1.4500 * 0.92,
    stop_loss_pct=-0.08,
    initial_stop_loss=1.4500 * 0.92,
    initial_stop_loss_pct=-0.08,
    max_rate=1.4550,
    min_rate=1.4120,
    exit_reason='stop_loss',
    strategy='KoreanStarterStrategy',
    enter_tag='trend_rsi_volume',
    timeframe=15,
    trading_mode=TradingMode.SPOT,
    amount_precision=1,
    price_precision=4,
    precision_mode=2,
    precision_mode_price=2,
    contract_size=1.0,
    leverage=1.0,
    is_short=False,
)
Trade.session.add(trade_xrp)

# 4. Active Open Trade: BTC/USDT (Currently holding and in profit!)
trade_btc = Trade(
    exchange='binance',
    pair='BTC/USDT',
    base_currency='BTC',
    stake_currency='USDT',
    is_open=True,
    open_rate=78850.0,
    open_rate_requested=78850.0,
    open_trade_value=300.0,
    stake_amount=300.0,
    max_stake_amount=300.0,
    amount=300.0 / 78850.0,
    amount_requested=300.0 / 78850.0,
    open_date=now - timedelta(hours=1, minutes=20),
    fee_open=0.001,
    fee_open_cost=0.30,
    fee_open_currency='USDT',
    stop_loss=78850.0 * 0.92,
    stop_loss_pct=-0.08,
    initial_stop_loss=78850.0 * 0.92,
    initial_stop_loss_pct=-0.08,
    max_rate=79450.0,
    min_rate=78800.0,
    strategy='KoreanStarterStrategy',
    enter_tag='trend_rsi_volume',
    timeframe=15,
    trading_mode=TradingMode.SPOT,
    amount_precision=5,
    price_precision=2,
    precision_mode=2,
    precision_mode_price=2,
    contract_size=1.0,
    leverage=1.0,
    is_short=False,
)
Trade.session.add(trade_btc)

Trade.session.commit()

# Add order for active trade
order_btc = Order(
    ft_trade_id=trade_btc.id,
    ft_order_side='buy',
    ft_pair='BTC/USDT',
    ft_is_open=False,
    ft_amount=trade_btc.amount,
    ft_price=78850.0,
    order_id='demo_btc_order_1',
    status='closed',
    symbol='BTC/USDT',
    order_type='limit',
    side='buy',
    price=78850.0,
    average=78850.0,
    amount=trade_btc.amount,
    filled=trade_btc.amount,
    remaining=0.0,
    cost=300.0,
    order_date=now - timedelta(hours=1, minutes=20),
    order_filled_date=now - timedelta(hours=1, minutes=20),
    order_update_date=now - timedelta(hours=1, minutes=20),
    ft_fee_base=0.001,
    ft_order_tag='trend_rsi_volume',
)
Trade.session.add(order_btc)
Trade.session.commit()

print(f"Successfully seeded demo trades using Freqtrade ORM: Active BTC Trade ID={trade_btc.id}")
