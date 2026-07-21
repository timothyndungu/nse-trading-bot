"""
Technical Indicators Module
Calculates technical indicators for trading signals
"""

import pandas as pd
import numpy as np
from typing import Tuple


class TechnicalIndicators:
    """Calculate technical indicators for algorithmic trading"""
    
    @staticmethod
    def RSI(data: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI)
        
        Args:
            data: Price data (closing prices)
            period: RSI period (default 14)
            
        Returns:
            RSI values
        """
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def MACD(data: pd.Series, fast: int = 12, slow: int = 26, 
             signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Args:
            data: Price data
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period
            
        Returns:
            Tuple of (MACD, Signal line, Histogram)
        """
        ema_fast = data.ewm(span=fast).mean()
        ema_slow = data.ewm(span=slow).mean()
        
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal).mean()
        histogram = macd - signal_line
        
        return macd, signal_line, histogram
    
    @staticmethod
    def BollingerBands(data: pd.Series, period: int = 20, 
                      std_dev: float = 2.0) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate Bollinger Bands
        
        Args:
            data: Price data
            period: Period for moving average
            std_dev: Number of standard deviations
            
        Returns:
            Tuple of (Upper band, Middle band, Lower band)
        """
        middle_band = data.rolling(window=period).mean()
        std = data.rolling(window=period).std()
        
        upper_band = middle_band + (std_dev * std)
        lower_band = middle_band - (std_dev * std)
        
        return upper_band, middle_band, lower_band
    
    @staticmethod
    def SMA(data: pd.Series, period: int) -> pd.Series:
        """
        Calculate Simple Moving Average
        
        Args:
            data: Price data
            period: Moving average period
            
        Returns:
            SMA values
        """
        return data.rolling(window=period).mean()
    
    @staticmethod
    def EMA(data: pd.Series, period: int) -> pd.Series:
        """
        Calculate Exponential Moving Average
        
        Args:
            data: Price data
            period: EMA period
            
        Returns:
            EMA values
        """
        return data.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def ATR(high: pd.Series, low: pd.Series, close: pd.Series, 
           period: int = 14) -> pd.Series:
        """
        Calculate Average True Range
        
        Args:
            high: High prices
            low: Low prices
            close: Close prices
            period: ATR period
            
        Returns:
            ATR values
        """
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        
        return atr
    
    @staticmethod
    def Stochastic(high: pd.Series, low: pd.Series, close: pd.Series, 
                  period: int = 14) -> Tuple[pd.Series, pd.Series]:
        """
        Calculate Stochastic Oscillator
        
        Args:
            high: High prices
            low: Low prices
            close: Close prices
            period: Stochastic period
            
        Returns:
            Tuple of (K-line, D-line)
        """
        lowest_low = low.rolling(window=period).min()
        highest_high = high.rolling(window=period).max()
        
        k_line = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_line = k_line.rolling(window=3).mean()
        
        return k_line, d_line
    
    @staticmethod
    def VWAP(high: pd.Series, low: pd.Series, close: pd.Series, 
            volume: pd.Series) -> pd.Series:
        """
        Calculate Volume Weighted Average Price
        
        Args:
            high: High prices
            low: Low prices
            close: Close prices
            volume: Trading volume
            
        Returns:
            VWAP values
        """
        tp = (high + low + close) / 3
        vwap = (tp * volume).rolling(window=20).sum() / volume.rolling(window=20).sum()
        
        return vwap
    
    @staticmethod
    def create_signals_df(df: pd.DataFrame) -> pd.DataFrame:
        """
        Create a comprehensive signals dataframe with all indicators
        
        Args:
            df: OHLCV dataframe
            
        Returns:
            DataFrame with all indicators
        """
        signals = df.copy()
        
        # Add indicators
        signals['RSI'] = TechnicalIndicators.RSI(df['Close'])
        signals['SMA_20'] = TechnicalIndicators.SMA(df['Close'], 20)
        signals['SMA_50'] = TechnicalIndicators.SMA(df['Close'], 50)
        signals['SMA_200'] = TechnicalIndicators.SMA(df['Close'], 200)
        
        signals['MACD'], signals['MACD_Signal'], signals['MACD_Hist'] = \
            TechnicalIndicators.MACD(df['Close'])
        
        signals['BB_Upper'], signals['BB_Middle'], signals['BB_Lower'] = \
            TechnicalIndicators.BollingerBands(df['Close'])
        
        signals['ATR'] = TechnicalIndicators.ATR(df['High'], df['Low'], df['Close'])
        
        signals['K_Line'], signals['D_Line'] = \
            TechnicalIndicators.Stochastic(df['High'], df['Low'], df['Close'])
        
        signals['VWAP'] = TechnicalIndicators.VWAP(df['High'], df['Low'], 
                                                  df['Close'], df['Volume'])
        
        return signals


if __name__ == "__main__":
    # Example usage
    import yfinance as yf
    
    # Download sample data
    data = yf.download('AAPL', period='1y', progress=False)
    
    # Calculate all indicators
    signals = TechnicalIndicators.create_signals_df(data)
    
    print("Indicators calculated:")
    print(signals[['Close', 'RSI', 'MACD', 'SMA_20', 'SMA_50']].tail(10))
