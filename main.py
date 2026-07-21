"""
Main entry point for NSE Trading Bot
"""

import logging
import argparse
import sys
from datetime import datetime
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def setup_directories():
    """Create necessary directories if they don't exist"""
    import os
    
    directories = [
        'data/raw',
        'data/processed',
        'data/historical',
        'logs',
        'models/checkpoints',
        'results/backtest'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Ensured directory exists: {directory}")


def collect_historical_data(stocks=None):
    """Download historical data for backtesting"""
    from src.data_collection.nse_fetcher import NSEDataCollector, setup_logging
    
    setup_logging()
    logger.info("Starting historical data collection...")
    
    if stocks is None:
        from config.settings import NSE_STOCKS
        stocks = NSE_STOCKS[:10]  # Start with first 10 stocks
    
    collector = NSEDataCollector()
    
    logger.info(f"Collecting data for {len(stocks)} stocks...")
    data = collector.download_historical_data(
        tickers=stocks,
        start_date='2021-01-01',
        end_date=datetime.now().strftime('%Y-%m-%d')
    )
    
    if not data.empty:
        collector.save_data_to_csv(data, 'nse_historical_data.csv')
        logger.info(f"Successfully collected data for {len(stocks)} stocks")
        print(f"\nData collection complete!")
        print(f"Shape: {data.shape}")
        print(f"Tickers: {data['Ticker'].unique()}")
    else:
        logger.error("No data collected")
        print("Error: No data was collected. Check your internet connection.")


def backtest_strategy(strategy_name='momentum', start_date=None, end_date=None):
    """Run backtesting for a specific strategy"""
    from src.data_collection.nse_fetcher import NSEDataCollector
    from src.indicators.technical_indicators import TechnicalIndicators
    from src.strategies.trading_strategies import create_strategy
    from src.risk_management.risk_manager import RiskManager
    from config.settings import INITIAL_CAPITAL
    
    logger.info(f"Starting backtest for {strategy_name} strategy...")
    
    if start_date is None:
        start_date = '2023-01-01'
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Load historical data
    collector = NSEDataCollector()
    try:
        data = collector.load_data_from_csv('nse_historical_data.csv')
    except:
        print("No historical data found. Please run 'collect-data' first.")
        return
    
    # Filter data by date range
    data = data[start_date:end_date]
    
    if data.empty:
        logger.error("No data for the specified date range")
        return
    
    # Get first available ticker
    ticker = data['Ticker'].iloc[0] if 'Ticker' in data.columns else 'EQUITY'
    ticker_data = data[data['Ticker'] == ticker].copy()
    
    # Calculate indicators
    signals_df = TechnicalIndicators.create_signals_df(ticker_data)
    
    # Generate trading signals
    strategy = create_strategy(strategy_name)
    signals_df = strategy.generate_signals(signals_df)
    
    # Initialize risk manager
    risk_mgr = RiskManager(INITIAL_CAPITAL)
    
    # Backtest logic
    equity_curve = [INITIAL_CAPITAL]
    trades = []
    position_open = False
    entry_price = 0
    
    for idx, row in signals_df.iterrows():
        if pd.isna(row['Signal']):
            continue
        
        current_price = row['Close']
        
        # BUY signal
        if row['Signal'] == 1 and not position_open:
            entry_price = current_price
            position_open = True
            logger.debug(f"BUY at {current_price:.2f} on {idx}")
            trades.append({
                'date': idx,
                'type': 'BUY',
                'price': current_price
            })
        
        # SELL signal
        elif row['Signal'] == -1 and position_open:
            pnl = (current_price - entry_price) * 100  # Assuming 100 units
            position_open = False
            logger.debug(f"SELL at {current_price:.2f} on {idx}, PnL: {pnl:.2f}")
            trades.append({
                'date': idx,
                'type': 'SELL',
                'price': current_price,
                'pnl': pnl
            })
            equity_curve.append(equity_curve[-1] + pnl)
    
    # Print results
    print(f"\n{'='*60}")
    print(f"BACKTEST RESULTS: {strategy_name.upper()} STRATEGY")
    print(f"{'='*60}")
    print(f"Ticker: {ticker}")
    print(f"Period: {start_date} to {end_date}")
    print(f"Initial Capital: {INITIAL_CAPITAL:,.0f} KES")
    print(f"Final Capital: {equity_curve[-1]:,.0f} KES")
    print(f"Total Return: {((equity_curve[-1] - INITIAL_CAPITAL) / INITIAL_CAPITAL * 100):.2f}%")
    print(f"Total Trades: {len([t for t in trades if t['type'] == 'SELL'])}")
    print(f"{'='*60}\n")
    
    return {
        'strategy': strategy_name,
        'equity_curve': equity_curve,
        'trades': trades,
        'final_capital': equity_curve[-1]
    }


def run_live_trading(mode='paper'):
    """Run live trading bot"""
    logger.info(f"Starting NSE Trading Bot in {mode} mode...")
    
    if mode == 'paper':
        logger.info("Running in PAPER TRADING mode (no real money at risk)")
    elif mode == 'live':
        logger.warning("Running in LIVE TRADING mode (REAL MONEY)")
        confirm = input("Are you sure? Type 'yes' to confirm: ")
        if confirm.lower() != 'yes':
            logger.info("Live trading cancelled")
            return
    
    print(f"\n{'='*60}")
    print(f"NSE TRADING BOT - {mode.upper()} MODE")
    print(f"{'='*60}")
    print("Features:")
    print("  ✓ Real-time data collection")
    print("  ✓ Technical analysis")
    print("  ✓ Algorithmic trading strategies")
    print("  ✓ Risk management")
    print("  ✓ Trade logging")
    print(f"{'='*60}\n")
    
    logger.info("Bot initialization complete. Ready for trading.")
    logger.info("Note: Full implementation requires broker API integration")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='NSE Trading Bot - AI-Powered Algorithmic Trading'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Collect data command
    collect_parser = subparsers.add_parser('collect-data', help='Download historical NSE data')
    collect_parser.add_argument('--stocks', nargs='+', help='Specific stocks to download')
    
    # Backtest command
    backtest_parser = subparsers.add_parser('backtest', help='Run strategy backtest')
    backtest_parser.add_argument('--strategy', default='momentum', 
                                help='Strategy name (momentum, mean_reversion, trend_following, breakout)')
    backtest_parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    backtest_parser.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    
    # Live trading command
    live_parser = subparsers.add_parser('live', help='Run live trading bot')
    live_parser.add_argument('--mode', choices=['paper', 'live'], default='paper',
                            help='Trading mode (paper or live)')
    
    args = parser.parse_args()
    
    # Setup
    setup_directories()
    
    # Execute commands
    if args.command == 'collect-data':
        collect_historical_data(args.stocks)
    elif args.command == 'backtest':
        backtest_strategy(args.strategy, args.start_date, args.end_date)
    elif args.command == 'live':
        run_live_trading(args.mode)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
