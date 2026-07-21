"""
NSE Data Collection Module
Fetches real-time and historical data from NSE and other sources
"""

import yfinance as yf
import requests
from datetime import datetime, timedelta
import pandas as pd
import logging
from typing import List, Dict, Optional
import time

logger = logging.getLogger(__name__)


class NSEDataCollector:
    """
    Collects data from NSE and alternative sources
    """
    
    def __init__(self):
        self.stocks = []
        self.data_cache = {}
        
    def get_nse_stocks_yfinance(self, tickers: List[str]) -> Dict:
        """
        Fetch NSE stock data using yfinance (works for NSE stocks listed globally)
        
        Args:
            tickers: List of NSE stock tickers
            
        Returns:
            Dictionary with historical data for each ticker
        """
        data = {}
        
        for ticker in tickers:
            try:
                # NSE tickers on yfinance are formatted as TICKER.NS
                yf_ticker = f"{ticker}.NS"
                logger.info(f"Fetching data for {yf_ticker}...")
                
                stock = yf.Ticker(yf_ticker)
                
                # Get historical data - 3 years
                hist = stock.history(period="3y")
                
                if hist.empty:
                    logger.warning(f"No data found for {ticker}")
                    continue
                    
                data[ticker] = {
                    'historical': hist,
                    'info': stock.info,
                    'last_updated': datetime.now()
                }
                
                # Be respectful with API calls
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error fetching data for {ticker}: {str(e)}")
                continue
                
        return data
    
    def get_real_time_data(self, ticker: str) -> Dict:
        """
        Get real-time data for a single stock
        
        Args:
            ticker: Stock ticker
            
        Returns:
            Dictionary with current price and basic info
        """
        try:
            stock = yf.Ticker(f"{ticker}.NS")
            current_data = stock.history(period="1d")
            
            if current_data.empty:
                return None
                
            latest = current_data.iloc[-1]
            
            return {
                'ticker': ticker,
                'price': latest['Close'],
                'open': latest['Open'],
                'high': latest['High'],
                'low': latest['Low'],
                'volume': latest['Volume'],
                'timestamp': current_data.index[-1]
            }
            
        except Exception as e:
            logger.error(f"Error fetching real-time data for {ticker}: {str(e)}")
            return None
    
    def scrape_nse_website(self) -> Dict:
        """
        Scrape NSE website for real-time market data
        NOTE: This is a template. NSE may have terms restricting scraping.
        Use official NSE APIs when available.
        
        Returns:
            Dictionary with market data
        """
        try:
            url = "https://www.nse.co.ke"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            logger.info("Successfully connected to NSE website")
            # Parse data as needed
            
            return response.text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error scraping NSE website: {str(e)}")
            return None
    
    def download_historical_data(self, tickers: List[str], 
                                start_date: str, 
                                end_date: str) -> pd.DataFrame:
        """
        Download historical data for backtesting
        
        Args:
            tickers: List of stock tickers
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            DataFrame with historical OHLCV data
        """
        combined_data = pd.DataFrame()
        
        for ticker in tickers:
            try:
                logger.info(f"Downloading {ticker} from {start_date} to {end_date}")
                
                yf_ticker = f"{ticker}.NS"
                data = yf.download(yf_ticker, start=start_date, end=end_date, 
                                 progress=False)
                
                if data.empty:
                    logger.warning(f"No data for {ticker}")
                    continue
                
                data['Ticker'] = ticker
                combined_data = pd.concat([combined_data, data])
                
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error downloading {ticker}: {str(e)}")
                continue
        
        return combined_data
    
    def get_intraday_data(self, ticker: str, interval: str = '5m') -> pd.DataFrame:
        """
        Get intraday data for real-time trading signals
        
        Args:
            ticker: Stock ticker
            interval: Time interval ('1m', '5m', '15m', '30m', '60m')
            
        Returns:
            DataFrame with intraday OHLCV data
        """
        try:
            yf_ticker = f"{ticker}.NS"
            data = yf.download(yf_ticker, period="1d", interval=interval, 
                             progress=False)
            return data
            
        except Exception as e:
            logger.error(f"Error fetching intraday data for {ticker}: {str(e)}")
            return pd.DataFrame()
    
    def save_data_to_csv(self, data: pd.DataFrame, filename: str):
        """Save data to CSV file"""
        try:
            data.to_csv(f'data/raw/{filename}')
            logger.info(f"Data saved to data/raw/{filename}")
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
    
    def load_data_from_csv(self, filename: str) -> pd.DataFrame:
        """Load data from CSV file"""
        try:
            data = pd.read_csv(f'data/raw/{filename}', index_col=0, 
                             parse_dates=True)
            logger.info(f"Data loaded from data/raw/{filename}")
            return data
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return pd.DataFrame()


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/data_collection.log'),
            logging.StreamHandler()
        ]
    )


if __name__ == "__main__":
    setup_logging()
    
    # Example usage
    collector = NSEDataCollector()
    
    # Fetch some popular NSE stocks
    popular_stocks = ['EQUITY', 'KCBGROUP', 'SAFARICOM', 'EABL', 'BAT']
    
    print("Fetching NSE stock data...")
    data = collector.get_nse_stocks_yfinance(popular_stocks)
    
    # Print summary
    for ticker, stock_data in data.items():
        print(f"\n{ticker}:")
        print(f"  Data points: {len(stock_data['historical'])}")
        print(f"  Latest price: {stock_data['historical']['Close'].iloc[-1]:.2f} KES")
        print(f"  52-week high: {stock_data['historical']['High'].max():.2f} KES")
        print(f"  52-week low: {stock_data['historical']['Low'].min():.2f} KES")
