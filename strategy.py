"""
Strategy Base Class and Implementations
Defines trading strategies for backtesting
"""

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import Literal


class Strategy(ABC):
    """Base class for all trading strategies"""
    
    def __init__(self, name: str):
        self.name = name
        self.signals = None
        
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on the strategy
        
        Parameters:
        -----------
        data : pd.DataFrame
            OHLCV data with technical indicators
            
        Returns:
        --------
        pd.DataFrame
            DataFrame with 'signal' column: 1 (buy), -1 (sell), 0 (hold)
        """
        pass
    
    def __str__(self):
        return f"{self.name} Strategy"


class MovingAverageCrossover(Strategy):
    """
    Moving Average Crossover Strategy
    
    Buy when short MA crosses above long MA
    Sell when short MA crosses below long MA
    """
    
    def __init__(self, short_window: int = 20, long_window: int = 50):
        super().__init__("Moving Average Crossover")
        self.short_window = short_window
        self.long_window = long_window
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        # Calculate moving averages
        df['SMA_Short'] = df['Close'].rolling(window=self.short_window).mean()
        df['SMA_Long'] = df['Close'].rolling(window=self.long_window).mean()
        
        # Generate signals
        df['signal'] = 0
        df.loc[df['SMA_Short'] > df['SMA_Long'], 'signal'] = 1  # Buy signal
        df.loc[df['SMA_Short'] < df['SMA_Long'], 'signal'] = -1  # Sell signal
        
        # Detect crossovers (only trade on the cross, not while above/below)
        df['position'] = df['signal'].diff()
        
        self.signals = df
        return df


class RSIMeanReversion(Strategy):
    """
    RSI Mean Reversion Strategy
    
    Buy when RSI < oversold threshold (default 30)
    Sell when RSI > overbought threshold (default 70)
    """
    
    def __init__(self, rsi_period: int = 14, oversold: int = 30, overbought: int = 70):
        super().__init__("RSI Mean Reversion")
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.overbought = overbought
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        # Calculate RSI if not already present
        if 'RSI' not in df.columns:
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
        
        # Generate signals
        df['signal'] = 0
        df.loc[df['RSI'] < self.oversold, 'signal'] = 1  # Buy when oversold
        df.loc[df['RSI'] > self.overbought, 'signal'] = -1  # Sell when overbought
        
        df['position'] = df['signal'].diff()
        
        self.signals = df
        return df


class MomentumStrategy(Strategy):
    """
    Momentum Strategy
    
    Buy when price momentum is positive
    Sell when price momentum is negative
    """
    
    def __init__(self, lookback_period: int = 20, threshold: float = 0.02):
        super().__init__("Momentum")
        self.lookback_period = lookback_period
        self.threshold = threshold
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        # Calculate momentum (rate of change)
        df['momentum'] = df['Close'].pct_change(periods=self.lookback_period)
        
        # Generate signals
        df['signal'] = 0
        df.loc[df['momentum'] > self.threshold, 'signal'] = 1  # Buy on positive momentum
        df.loc[df['momentum'] < -self.threshold, 'signal'] = -1  # Sell on negative momentum
        
        df['position'] = df['signal'].diff()
        
        self.signals = df
        return df


class BollingerBandsStrategy(Strategy):
    """
    Bollinger Bands Mean Reversion Strategy
    
    Buy when price touches lower band
    Sell when price touches upper band
    """
    
    def __init__(self, window: int = 20, num_std: float = 2.0):
        super().__init__("Bollinger Bands")
        self.window = window
        self.num_std = num_std
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        # Calculate Bollinger Bands
        df['BB_Middle'] = df['Close'].rolling(window=self.window).mean()
        bb_std = df['Close'].rolling(window=self.window).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * self.num_std)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * self.num_std)
        
        # Generate signals
        df['signal'] = 0
        df.loc[df['Close'] <= df['BB_Lower'], 'signal'] = 1  # Buy at lower band
        df.loc[df['Close'] >= df['BB_Upper'], 'signal'] = -1  # Sell at upper band
        
        df['position'] = df['signal'].diff()
        
        self.signals = df
        return df


