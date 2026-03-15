"""
Backtesting Engine
Executes trades based on strategy signals and tracks portfolio performance
"""

import pandas as pd
import numpy as np
from typing import Optional
from strategy import Strategy


class Backtester:
    """
    Backtesting engine that simulates trading based on strategy signals
    """
    
    def __init__(
        self,
        initial_capital: float = 100000.0,
        commission: float = 0.001,  # 0.1% commission per trade
        slippage: float = 0.0005,   # 0.05% slippage
    ):
        """
        Initialize the backtester
        
        Parameters:
        -----------
        initial_capital : float
            Starting capital for the portfolio
        commission : float
            Commission rate per trade (as decimal, e.g., 0.001 = 0.1%)
        slippage : float
            Slippage rate (as decimal)
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.results = None
        
    def run(self, data: pd.DataFrame, strategy: Strategy) -> pd.DataFrame:
        """
        Run backtest on historical data using the given strategy
        
        Parameters:
        -----------
        data : pd.DataFrame
            Historical OHLCV data
        strategy : Strategy
            Trading strategy to test
            
        Returns:
        --------
        pd.DataFrame
            DataFrame with portfolio values, positions, and trades
        """
        print(f"\n{'='*60}")
        print(f"Running backtest: {strategy.name}")
        print(f"{'='*60}")
        
        # Generate signals
        signals = strategy.generate_signals(data)
        
        # Initialize portfolio tracking
        portfolio = pd.DataFrame(index=signals.index)
        portfolio['price'] = signals['Close']
        portfolio['signal'] = signals['signal']
        
        # Track positions and cash
        portfolio['position'] = 0  # Number of shares held
        portfolio['cash'] = self.initial_capital
        portfolio['holdings'] = 0.0  # Value of shares held
        portfolio['total'] = self.initial_capital
        portfolio['returns'] = 0.0
        portfolio['trade'] = 0  # 1 for buy, -1 for sell, 0 for hold
        
        # Simulate trading
        position = 0  # Current position (number of shares)
        cash = self.initial_capital
        trades = []
        
        for i in range(1, len(portfolio)):
            current_price = portfolio['price'].iloc[i]
            prev_signal = portfolio['signal'].iloc[i-1]
            current_signal = portfolio['signal'].iloc[i]
            
            # Detect signal changes (crossovers)
            if prev_signal != current_signal:
                # Buy signal
                if current_signal == 1 and position == 0:
                    # Calculate shares to buy (use all available cash)
                    buy_price = current_price * (1 + self.slippage)
                    shares_to_buy = int(cash / (buy_price * (1 + self.commission)))
                    
                    if shares_to_buy > 0:
                        cost = shares_to_buy * buy_price * (1 + self.commission)
                        cash -= cost
                        position = shares_to_buy
                        portfolio.loc[portfolio.index[i], 'trade'] = 1
                        
                        trades.append({
                            'date': portfolio.index[i],
                            'type': 'BUY',
                            'price': buy_price,
                            'shares': shares_to_buy,
                            'cost': cost,
                            'cash': cash
                        })
                
                # Sell signal
                elif current_signal == -1 and position > 0:
                    sell_price = current_price * (1 - self.slippage)
                    proceeds = position * sell_price * (1 - self.commission)
                    cash += proceeds
                    
                    trades.append({
                        'date': portfolio.index[i],
                        'type': 'SELL',
                        'price': sell_price,
                        'shares': position,
                        'proceeds': proceeds,
                        'cash': cash
                    })
                    
                    position = 0
                    portfolio.loc[portfolio.index[i], 'trade'] = -1
            
            # Update portfolio values
            portfolio.loc[portfolio.index[i], 'position'] = position
            portfolio.loc[portfolio.index[i], 'cash'] = cash
            portfolio.loc[portfolio.index[i], 'holdings'] = position * current_price
            portfolio.loc[portfolio.index[i], 'total'] = cash + (position * current_price)
        
        # Calculate returns
        portfolio['returns'] = portfolio['total'].pct_change()
        portfolio['cumulative_returns'] = (1 + portfolio['returns']).cumprod() - 1
        
        # Store results
        self.results = portfolio
        self.trades = pd.DataFrame(trades)
        self.strategy_name = strategy.name
        
        # Print summary
        print(f"\nBacktest completed!")
        print(f"Total trades: {len(trades)}")
        print(f"Final portfolio value: ${portfolio['total'].iloc[-1]:,.2f}")
        print(f"Total return: {(portfolio['total'].iloc[-1] / self.initial_capital - 1) * 100:.2f}%")
        
        return portfolio
    
    def get_results(self) -> pd.DataFrame:
        """Get backtest results"""
        if self.results is None:
            raise ValueError("No backtest results available. Run backtest first.")
        return self.results
    
    def get_trades(self) -> pd.DataFrame:
        """Get trade history"""
        if not hasattr(self, 'trades'):
            raise ValueError("No trade history available. Run backtest first.")
        return self.trades


