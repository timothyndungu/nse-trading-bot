"""
Risk Management Module
Manages portfolio risk and position sizing
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


class RiskManager:
    """Handles risk management for trading operations"""
    
    def __init__(self, initial_capital: float, max_drawdown: float = 0.20,
                 risk_per_trade: float = 0.02, max_positions: int = 10):
        """
        Initialize Risk Manager
        
        Args:
            initial_capital: Starting capital in KES
            max_drawdown: Maximum acceptable portfolio drawdown (20%)
            risk_per_trade: Risk per trade as % of portfolio (2%)
            max_positions: Maximum concurrent positions
        """
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.max_drawdown = max_drawdown
        self.risk_per_trade = risk_per_trade
        self.max_positions = max_positions
        self.positions = {}
        self.trade_history = []
        
    def calculate_position_size(self, entry_price: float, stop_loss_price: float,
                              method: str = 'fixed_fractional') -> float:
        """
        Calculate position size based on risk parameters
        
        Args:
            entry_price: Entry price
            stop_loss_price: Stop loss price
            method: Sizing method ('fixed_fractional' or 'kelly')
            
        Returns:
            Position size in units
        """
        risk_amount = self.current_capital * self.risk_per_trade
        price_risk = abs(entry_price - stop_loss_price)
        
        if price_risk == 0:
            return 0
        
        position_size = risk_amount / price_risk
        
        if method == 'fixed_fractional':
            return position_size
        elif method == 'kelly':
            # Kelly Criterion (simplified)
            return position_size * 0.25  # Use 25% of Kelly for safety
        else:
            return position_size
    
    def check_portfolio_health(self, current_portfolio_value: float) -> Dict:
        """
        Check if portfolio is within acceptable risk limits
        
        Args:
            current_portfolio_value: Current portfolio value
            
        Returns:
            Dictionary with health metrics
        """
        peak_value = max(self.initial_capital, current_portfolio_value)
        drawdown = (peak_value - current_portfolio_value) / peak_value
        
        health = {
            'current_value': current_portfolio_value,
            'peak_value': peak_value,
            'drawdown': drawdown,
            'drawdown_pct': drawdown * 100,
            'is_healthy': drawdown <= self.max_drawdown,
            'warning': False,
            'halt_trading': False
        }
        
        # Set warning thresholds
        if drawdown > self.max_drawdown * 0.75:
            health['warning'] = True
        
        if drawdown > self.max_drawdown:
            health['halt_trading'] = True
        
        return health
    
    def can_open_position(self, symbol: str) -> bool:
        """
        Check if a new position can be opened
        
        Args:
            symbol: Stock symbol
            
        Returns:
            True if position can be opened
        """
        # Check max positions limit
        active_positions = sum(1 for pos in self.positions.values() 
                             if pos['status'] == 'open')
        
        if active_positions >= self.max_positions:
            return False
        
        # Check if already has position in this symbol
        if symbol in self.positions and self.positions[symbol]['status'] == 'open':
            return False
        
        return True
    
    def set_stop_loss(self, entry_price: float, stop_loss_pct: float = 0.05) -> float:
        """
        Calculate stop loss price
        
        Args:
            entry_price: Entry price
            stop_loss_pct: Stop loss percentage (5%)
            
        Returns:
            Stop loss price
        """
        return entry_price * (1 - stop_loss_pct)
    
    def set_take_profit(self, entry_price: float, take_profit_pct: float = 0.10) -> float:
        """
        Calculate take profit price
        
        Args:
            entry_price: Entry price
            take_profit_pct: Take profit percentage (10%)
            
        Returns:
            Take profit price
        """
        return entry_price * (1 + take_profit_pct)
    
    def calculate_win_rate(self) -> float:
        """Calculate win rate from trade history"""
        if not self.trade_history:
            return 0
        
        wins = sum(1 for trade in self.trade_history if trade['pnl'] > 0)
        return wins / len(self.trade_history)
    
    def calculate_sharpe_ratio(self, returns: pd.Series, risk_free_rate: float = 0.05) -> float:
        """
        Calculate Sharpe Ratio
        
        Args:
            returns: Series of portfolio returns
            risk_free_rate: Risk-free rate (annual)
            
        Returns:
            Sharpe Ratio
        """
        if len(returns) < 2:
            return 0
        
        excess_returns = returns - (risk_free_rate / 252)
        return excess_returns.mean() / excess_returns.std() * np.sqrt(252)
    
    def calculate_max_drawdown(self, equity_curve: pd.Series) -> float:
        """
        Calculate maximum drawdown from equity curve
        
        Args:
            equity_curve: Series of portfolio values
            
        Returns:
            Maximum drawdown percentage
        """
        running_max = equity_curve.expanding().max()
        drawdown = (equity_curve - running_max) / running_max
        return drawdown.min()
    
    def calculate_win_loss_ratio(self) -> float:
        """Calculate average win to average loss ratio"""
        if not self.trade_history:
            return 0
        
        wins = [t['pnl'] for t in self.trade_history if t['pnl'] > 0]
        losses = [abs(t['pnl']) for t in self.trade_history if t['pnl'] < 0]
        
        if not losses:
            return float('inf')
        
        avg_win = np.mean(wins) if wins else 0
        avg_loss = np.mean(losses)
        
        return avg_win / avg_loss if avg_loss > 0 else 0
    
    def calculate_profit_factor(self) -> float:
        """Calculate profit factor (total gains / total losses)"""
        if not self.trade_history:
            return 0
        
        total_wins = sum(t['pnl'] for t in self.trade_history if t['pnl'] > 0)
        total_losses = abs(sum(t['pnl'] for t in self.trade_history if t['pnl'] < 0))
        
        if total_losses == 0:
            return float('inf')
        
        return total_wins / total_losses
    
    def record_trade(self, symbol: str, entry_price: float, exit_price: float,
                    quantity: int, trade_type: str = 'long'):
        """
        Record a completed trade
        
        Args:
            symbol: Stock symbol
            entry_price: Entry price
            exit_price: Exit price
            quantity: Quantity traded
            trade_type: Trade type ('long' or 'short')
        """
        if trade_type == 'long':
            pnl = (exit_price - entry_price) * quantity
        else:
            pnl = (entry_price - exit_price) * quantity
        
        pnl_pct = ((exit_price - entry_price) / entry_price) * 100
        
        trade = {
            'symbol': symbol,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'quantity': quantity,
            'pnl': pnl,
            'pnl_pct': pnl_pct,
            'type': trade_type
        }
        
        self.trade_history.append(trade)
        self.current_capital += pnl


class PositionManager:
    """Manages individual positions"""
    
    def __init__(self):
        self.positions = {}
    
    def open_position(self, symbol: str, entry_price: float, quantity: int,
                     stop_loss: float, take_profit: float):
        """Open a new position"""
        self.positions[symbol] = {
            'entry_price': entry_price,
            'quantity': quantity,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'status': 'open',
            'current_price': entry_price,
            'unrealized_pnl': 0
        }
    
    def update_position(self, symbol: str, current_price: float):
        """Update position with current market price"""
        if symbol not in self.positions:
            return
        
        pos = self.positions[symbol]
        pos['current_price'] = current_price
        pos['unrealized_pnl'] = (current_price - pos['entry_price']) * pos['quantity']
    
    def close_position(self, symbol: str, exit_price: float) -> Dict:
        """Close a position"""
        if symbol not in self.positions:
            return None
        
        pos = self.positions[symbol]
        realized_pnl = (exit_price - pos['entry_price']) * pos['quantity']
        
        pos['status'] = 'closed'
        pos['exit_price'] = exit_price
        pos['realized_pnl'] = realized_pnl
        
        return pos
    
    def check_stop_loss(self, symbol: str, current_price: float) -> bool:
        """Check if position should be stopped out"""
        if symbol not in self.positions:
            return False
        
        pos = self.positions[symbol]
        return current_price <= pos['stop_loss']
    
    def check_take_profit(self, symbol: str, current_price: float) -> bool:
        """Check if position should take profit"""
        if symbol not in self.positions:
            return False
        
        pos = self.positions[symbol]
        return current_price >= pos['take_profit']


if __name__ == "__main__":
    # Example usage
    risk_mgr = RiskManager(initial_capital=1000000)
    
    # Calculate position size
    position_size = risk_mgr.calculate_position_size(
        entry_price=100,
        stop_loss_price=95
    )
    print(f"Position size: {position_size:.2f} units")
    
    # Check stop loss and take profit
    stop_loss = risk_mgr.set_stop_loss(entry_price=100, stop_loss_pct=0.05)
    take_profit = risk_mgr.set_take_profit(entry_price=100, take_profit_pct=0.10)
    
    print(f"Stop loss: {stop_loss:.2f}")
    print(f"Take profit: {take_profit:.2f}")
    
    # Check portfolio health
    health = risk_mgr.check_portfolio_health(950000)
    print(f"\nPortfolio health:")
    print(f"  Drawdown: {health['drawdown_pct']:.2f}%")
    print(f"  Healthy: {health['is_healthy']}")
