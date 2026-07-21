"""
Backtesting Framework
Tests trading strategies against historical data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Backtester:
    """Backtesting engine for trading strategies"""
    
    def __init__(self, strategy, data: pd.DataFrame, initial_capital: float = 1000000):
        """
        Initialize backtester
        
        Args:
            strategy: Trading strategy object
            data: Historical OHLCV data
            initial_capital: Starting capital in KES
        """
        self.strategy = strategy
        self.data = data.copy()
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.positions = {}
        self.trades = []
        self.portfolio_values = [initial_capital]
        self.results = None
        
    def run(self) -> dict:
        """
        Run the backtest
        
        Returns:
            Dictionary with backtest results
        """
        logger.info("Starting backtest...")
        
        # Generate signals
        signals_df = self.strategy.generate_signals(self.data)
        
        # Process each candle
        for idx, row in signals_df.iterrows():
            signal = row.get('Signal', 0)
            close_price = row['Close']
            
            # Execute trades based on signals
            if signal == 1:  # BUY
                self._open_position(idx, close_price)
            elif signal == -1:  # SELL
                self._close_position(idx, close_price)
            
            # Update portfolio value
            self._update_portfolio_value(close_price)
        
        # Close any remaining positions
        if self.positions:
            last_price = self.data['Close'].iloc[-1]
            for symbol in list(self.positions.keys()):
                self._close_position(self.data.index[-1], last_price, symbol)
        
        # Calculate results
        self.results = self._calculate_results()
        logger.info("Backtest completed")
        
        return self.results
    
    def _open_position(self, timestamp, price: float):
        """Open a new position"""
        position_size = self.current_capital * 0.1  # 10% per position
        quantity = int(position_size / price)
        
        if quantity > 0:
            self.positions['long'] = {
                'entry_price': price,
                'quantity': quantity,
                'timestamp': timestamp
            }
            logger.debug(f"BUY at {price:.2f} on {timestamp}")
    
    def _close_position(self, timestamp, price: float, symbol: str = 'long'):
        """Close a position"""
        if symbol in self.positions:
            pos = self.positions[symbol]
            pnl = (price - pos['entry_price']) * pos['quantity']
            pnl_pct = ((price - pos['entry_price']) / pos['entry_price']) * 100
            
            self.trades.append({
                'entry_timestamp': pos['timestamp'],
                'exit_timestamp': timestamp,
                'entry_price': pos['entry_price'],
                'exit_price': price,
                'quantity': pos['quantity'],
                'pnl': pnl,
                'pnl_pct': pnl_pct
            })
            
            self.current_capital += pnl
            del self.positions[symbol]
            
            logger.debug(f"SELL at {price:.2f} on {timestamp}, PnL: {pnl:.2f}")
    
    def _update_portfolio_value(self, current_price: float):
        """Update portfolio value based on current price"""
        portfolio_value = self.current_capital
        
        # Add unrealized P&L from open positions
        for pos in self.positions.values():
            unrealized_pnl = (current_price - pos['entry_price']) * pos['quantity']
            portfolio_value += unrealized_pnl
        
        self.portfolio_values.append(portfolio_value)
    
    def _calculate_results(self) -> dict:
        """Calculate backtest statistics"""
        equity_curve = np.array(self.portfolio_values)
        returns = np.diff(equity_curve) / equity_curve[:-1]
        
        total_return = (self.portfolio_values[-1] - self.initial_capital) / self.initial_capital
        
        # Max drawdown
        cummax = np.maximum.accumulate(equity_curve)
        drawdown = (equity_curve - cummax) / cummax
        max_drawdown = np.min(drawdown)
        
        # Win rate
        closed_trades = [t for t in self.trades if 'pnl' in t]
        wins = sum(1 for t in closed_trades if t['pnl'] > 0)
        win_rate = wins / len(closed_trades) if closed_trades else 0
        
        # Sharpe ratio
        sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252) if len(returns) > 0 else 0
        
        return {
            'total_return': total_return,
            'total_return_pct': total_return * 100,
            'final_capital': self.portfolio_values[-1],
            'max_drawdown': max_drawdown,
            'max_drawdown_pct': max_drawdown * 100,
            'sharpe_ratio': sharpe,
            'total_trades': len(self.trades),
            'win_rate': win_rate,
            'win_rate_pct': win_rate * 100,
            'profit_factor': self._calculate_profit_factor()
        }
    
    def _calculate_profit_factor(self) -> float:
        """Calculate profit factor"""
        total_wins = sum(t['pnl'] for t in self.trades if t['pnl'] > 0)
        total_losses = abs(sum(t['pnl'] for t in self.trades if t['pnl'] < 0))
        
        if total_losses == 0:
            return float('inf')
        return total_wins / total_losses
    
    def plot_results(self):
        """Plot backtest results"""
        plt.figure(figsize=(14, 6))
        plt.plot(self.portfolio_values)
        plt.title('Portfolio Value Over Time')
        plt.xlabel('Days')
        plt.ylabel('Value (KES)')
        plt.grid(True)
        plt.show()
    
    def get_results_dataframe(self) -> pd.DataFrame:
        """Get trades as DataFrame"""
        return pd.DataFrame(self.trades)
