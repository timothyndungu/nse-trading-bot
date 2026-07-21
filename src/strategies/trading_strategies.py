"""
Trading Strategies Module
Implements various algorithmic trading strategies
"""

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple


class BaseStrategy(ABC):
    """Base class for all trading strategies"""
    
    def __init__(self, name: str):
        self.name = name
        self.signals = None
        
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals
        
        Args:
            data: OHLCV data with indicators
            
        Returns:
            DataFrame with signals (1 = BUY, -1 = SELL, 0 = HOLD)
        """
        pass
    
    def get_position(self, signal: int) -> str:
        """Convert numeric signal to position"""
        if signal == 1:
            return 'BUY'
        elif signal == -1:
            return 'SELL'
        else:
            return 'HOLD'


class MomentumStrategy(BaseStrategy):
    """
    Momentum trading strategy using RSI and MACD
    Trades on price momentum
    """
    
    def __init__(self):
        super().__init__("Momentum")
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate momentum signals
        
        Buy: RSI < 50 and MACD > Signal, or price above SMA20
        Sell: RSI > 70 or MACD < Signal
        """
        signals = data.copy()
        signals['Signal'] = 0
        
        # RSI conditions
        rsi_buy = signals['RSI'] < 50
        rsi_sell = signals['RSI'] > 70
        
        # MACD conditions
        macd_buy = signals['MACD'] > signals['MACD_Signal']
        macd_sell = signals['MACD'] < signals['MACD_Signal']
        
        # Price vs SMA conditions
        sma_buy = signals['Close'] > signals['SMA_20']
        
        # Generate signals
        signals.loc[rsi_buy & macd_buy & sma_buy, 'Signal'] = 1  # BUY
        signals.loc[rsi_sell | macd_sell, 'Signal'] = -1  # SELL
        
        return signals


class MeanReversionStrategy(BaseStrategy):
    """
    Mean reversion strategy using Bollinger Bands
    Trades on deviation from moving average
    """
    
    def __init__(self):
        super().__init__("Mean Reversion")
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate mean reversion signals
        
        Buy: Price at lower Bollinger Band (oversold)
        Sell: Price at upper Bollinger Band (overbought)
        """
        signals = data.copy()
        signals['Signal'] = 0
        
        # RSI extremes
        rsi_oversold = signals['RSI'] < 30
        rsi_overbought = signals['RSI'] > 70
        
        # Bollinger Bands touch
        at_lower_band = signals['Close'] < signals['BB_Lower']
        at_upper_band = signals['Close'] > signals['BB_Upper']
        
        # Generate signals
        signals.loc[at_lower_band & rsi_oversold, 'Signal'] = 1  # BUY
        signals.loc[at_upper_band & rsi_overbought, 'Signal'] = -1  # SELL
        
        return signals


class TrendFollowingStrategy(BaseStrategy):
    """
    Trend following strategy using moving averages
    Trades in the direction of established trends
    """
    
    def __init__(self):
        super().__init__("Trend Following")
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trend following signals
        
        Buy: SMA20 > SMA50 > SMA200 (uptrend)
        Sell: SMA20 < SMA50 < SMA200 (downtrend)
        """
        signals = data.copy()
        signals['Signal'] = 0
        
        # Trend conditions
        uptrend = (signals['SMA_20'] > signals['SMA_50']) & \
                 (signals['SMA_50'] > signals['SMA_200'])
        downtrend = (signals['SMA_20'] < signals['SMA_50']) & \
                   (signals['SMA_50'] < signals['SMA_200'])
        
        # Price above SMA20 for uptrend confirmation
        price_above_sma = signals['Close'] > signals['SMA_20']
        price_below_sma = signals['Close'] < signals['SMA_20']
        
        # Generate signals
        signals.loc[uptrend & price_above_sma, 'Signal'] = 1  # BUY
        signals.loc[downtrend & price_below_sma, 'Signal'] = -1  # SELL
        
        return signals


class BreakoutStrategy(BaseStrategy):
    """
    Breakout strategy using Bollinger Bands
    Trades on price breakouts from consolidation
    """
    
    def __init__(self):
        super().__init__("Breakout")
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate breakout signals
        
        Buy: Price breaks above upper Bollinger Band
        Sell: Price breaks below lower Bollinger Band
        """
        signals = data.copy()
        signals['Signal'] = 0
        
        # Price breakouts
        previous_close = signals['Close'].shift(1)
        bb_upper_previous = signals['BB_Upper'].shift(1)
        bb_lower_previous = signals['BB_Lower'].shift(1)
        
        # Breakout conditions
        above_breakout = (previous_close <= bb_upper_previous) & \
                        (signals['Close'] > signals['BB_Upper'])
        below_breakout = (previous_close >= bb_lower_previous) & \
                        (signals['Close'] < signals['BB_Lower'])
        
        # Volume confirmation
        volume_spike = signals['Volume'] > signals['Volume'].rolling(20).mean() * 1.5
        
        # Generate signals
        signals.loc[above_breakout & volume_spike, 'Signal'] = 1  # BUY
        signals.loc[below_breakout & volume_spike, 'Signal'] = -1  # SELL
        
        return signals


class EnsembleStrategy(BaseStrategy):
    """
    Ensemble strategy combining multiple strategies
    Uses weighted voting from multiple strategies
    """
    
    def __init__(self, strategies: List[BaseStrategy], weights: List[float] = None):
        super().__init__("Ensemble")
        self.strategies = strategies
        
        if weights is None:
            weights = [1.0 / len(strategies)] * len(strategies)
        self.weights = weights
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate ensemble signals using weighted voting
        """
        signals = data.copy()
        signals['Ensemble_Signal'] = 0.0
        
        # Get signals from each strategy
        for strategy, weight in zip(self.strategies, self.weights):
            strategy_signals = strategy.generate_signals(data)
            signals['Ensemble_Signal'] += strategy_signals['Signal'] * weight
        
        # Convert weighted average to final signal
        signals['Signal'] = 0
        signals.loc[signals['Ensemble_Signal'] > 0.3, 'Signal'] = 1  # BUY
        signals.loc[signals['Ensemble_Signal'] < -0.3, 'Signal'] = -1  # SELL
        
        return signals


def create_strategy(strategy_name: str) -> BaseStrategy:
    """Factory function to create strategy instances"""
    
    strategies = {
        'momentum': MomentumStrategy,
        'mean_reversion': MeanReversionStrategy,
        'trend_following': TrendFollowingStrategy,
        'breakout': BreakoutStrategy
    }
    
    if strategy_name.lower() not in strategies:
        raise ValueError(f"Unknown strategy: {strategy_name}")
    
    return strategies[strategy_name.lower()]()


if __name__ == "__main__":
    import sys
    sys.path.insert(0, '../')
    from indicators.technical_indicators import TechnicalIndicators
    import yfinance as yf
    
    # Example usage
    data = yf.download('AAPL', period='1y', progress=False)
    signals_df = TechnicalIndicators.create_signals_df(data)
    
    # Test each strategy
    strategies = ['momentum', 'mean_reversion', 'trend_following', 'breakout']
    
    for strategy_name in strategies:
        strategy = create_strategy(strategy_name)
        signals = strategy.generate_signals(signals_df)
        
        # Count signals
        buys = (signals['Signal'] == 1).sum()
        sells = (signals['Signal'] == -1).sum()
        
        print(f"\n{strategy.name} Strategy:")
        print(f"  Buy signals: {buys}")
        print(f"  Sell signals: {sells}")
        print(f"  Latest signal: {strategy.get_position(signals['Signal'].iloc[-1])}")
