"""
Data Handler Module
Fetches and manages historical stock data from Yahoo Finance
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List


class DataHandler:
    """Handles fetching and managing stock market data"""
    
    def __init__(self):
        self.data = {}
        
    def fetch_data(
        self, 
        symbol: str, 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None,
        period: str = "1y"
    ) -> pd.DataFrame:
        """
        Fetch historical stock data from Yahoo Finance
        
        Parameters:
        -----------
        symbol : str
            Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        start_date : str, optional
            Start date in 'YYYY-MM-DD' format
        end_date : str, optional
            End date in 'YYYY-MM-DD' format
        period : str, default='1y'
            Period to fetch if start_date not specified
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            
        Returns:
        --------
        pd.DataFrame
            DataFrame with OHLCV data
        """
        try:
            ticker = yf.Ticker(symbol)
            
            if start_date and end_date:
                df = ticker.history(start=start_date, end=end_date)
            else:
                df = ticker.history(period=period)
            
            if df.empty:
                raise ValueError(f"No data found for symbol {symbol}")
            
            # Store the data
            self.data[symbol] = df
            
            print(f"✓ Fetched {len(df)} days of data for {symbol}")
            print(f"  Date range: {df.index[0].date()} to {df.index[-1].date()}")
            
            return df
            
        except Exception as e:
            print(f"✗ Error fetching data for {symbol}: {str(e)}")
            raise
    
    def fetch_multiple(
        self, 
        symbols: List[str], 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: str = "1y"
    ) -> dict:
        """
        Fetch data for multiple symbols
        
        Parameters:
        -----------
        symbols : List[str]
            List of stock ticker symbols
        start_date : str, optional
            Start date in 'YYYY-MM-DD' format
        end_date : str, optional
            End date in 'YYYY-MM-DD' format
        period : str, default='1y'
            Period to fetch if start_date not specified
            
        Returns:
        --------
        dict
            Dictionary mapping symbols to DataFrames
        """
        results = {}
        for symbol in symbols:
            try:
                results[symbol] = self.fetch_data(symbol, start_date, end_date, period)
            except Exception as e:
                print(f"Skipping {symbol} due to error")
                continue
        
        return results
    
    def get_data(self, symbol: str) -> pd.DataFrame:
        """Get previously fetched data for a symbol"""
        if symbol not in self.data:
            raise ValueError(f"No data available for {symbol}. Fetch it first.")
        return self.data[symbol]
    
    def add_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add common technical indicators to the dataframe
        
        Parameters:
        -----------
        df : pd.DataFrame
            OHLCV dataframe
            
        Returns:
        --------
        pd.DataFrame
            DataFrame with added technical indicators
        """
        # Make a copy to avoid modifying original
        df = df.copy()
        
        # Simple Moving Averages
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        
        # Exponential Moving Averages
        df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
        
        # RSI (Relative Strength Index)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        return df


