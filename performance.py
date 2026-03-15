"""
Performance Analysis Module
Calculates performance metrics and generates reports
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional
from tabulate import tabulate


class PerformanceAnalyzer:
    """Analyzes backtest performance and calculates metrics"""
    
    def __init__(self, results: pd.DataFrame, trades: pd.DataFrame, initial_capital: float):
        """
        Initialize performance analyzer
        
        Parameters:
        -----------
        results : pd.DataFrame
            Backtest results with portfolio values
        trades : pd.DataFrame
            Trade history
        initial_capital : float
            Initial capital
        """
        self.results = results
        self.trades = trades
        self.initial_capital = initial_capital
        self.metrics = {}
        
    def calculate_metrics(self) -> Dict:
        """
        Calculate comprehensive performance metrics
        
        Returns:
        --------
        Dict
            Dictionary of performance metrics
        """
        results = self.results
        trades = self.trades
        
        # Basic returns
        total_return = (results['total'].iloc[-1] / self.initial_capital - 1) * 100
        
        # Annualized return
        days = (results.index[-1] - results.index[0]).days
        years = days / 365.25
        annualized_return = ((results['total'].iloc[-1] / self.initial_capital) ** (1/years) - 1) * 100 if years > 0 else 0
        
        # Volatility (annualized)
        daily_returns = results['returns'].dropna()
        volatility = daily_returns.std() * np.sqrt(252) * 100  # Annualized
        
        # Sharpe Ratio (assuming 0% risk-free rate)
        sharpe_ratio = (annualized_return / volatility) if volatility > 0 else 0
        
        # Maximum Drawdown
        cumulative = results['total']
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max * 100
        max_drawdown = drawdown.min()
        
        # Win Rate and Trade Statistics
        if len(trades) > 0:
            # Pair buy and sell trades
            buy_trades = trades[trades['type'] == 'BUY'].reset_index(drop=True)
            sell_trades = trades[trades['type'] == 'SELL'].reset_index(drop=True)
            
            num_trades = min(len(buy_trades), len(sell_trades))
            
            if num_trades > 0:
                wins = 0
                total_profit = 0
                total_loss = 0
                
                for i in range(num_trades):
                    buy_cost = buy_trades.loc[i, 'cost']
                    sell_proceeds = sell_trades.loc[i, 'proceeds']
                    profit = sell_proceeds - buy_cost
                    
                    if profit > 0:
                        wins += 1
                        total_profit += profit
                    else:
                        total_loss += abs(profit)
                
                win_rate = (wins / num_trades) * 100
                avg_win = total_profit / wins if wins > 0 else 0
                avg_loss = total_loss / (num_trades - wins) if (num_trades - wins) > 0 else 0
                profit_factor = total_profit / total_loss if total_loss > 0 else float('inf')
            else:
                num_trades = 0
                win_rate = 0
                avg_win = 0
                avg_loss = 0
                profit_factor = 0
        else:
            num_trades = 0
            win_rate = 0
            avg_win = 0
            avg_loss = 0
            profit_factor = 0
        
        # Calmar Ratio (annualized return / max drawdown)
        calmar_ratio = abs(annualized_return / max_drawdown) if max_drawdown != 0 else 0
        
        # Store metrics
        self.metrics = {
            'Total Return (%)': round(total_return, 2),
            'Annualized Return (%)': round(annualized_return, 2),
            'Volatility (%)': round(volatility, 2),
            'Sharpe Ratio': round(sharpe_ratio, 2),
            'Max Drawdown (%)': round(max_drawdown, 2),
            'Calmar Ratio': round(calmar_ratio, 2),
            'Number of Trades': num_trades,
            'Win Rate (%)': round(win_rate, 2),
            'Average Win ($)': round(avg_win, 2),
            'Average Loss ($)': round(avg_loss, 2),
            'Profit Factor': round(profit_factor, 2),
            'Final Portfolio Value ($)': round(results['total'].iloc[-1], 2),
            'Total Days': days
        }
        
        return self.metrics
    
    def print_report(self):
        """Print a formatted performance report"""
        if not self.metrics:
            self.calculate_metrics()
        
        print(f"\n{'='*60}")
        print(f"PERFORMANCE REPORT")
        print(f"{'='*60}\n")
        
        # Format metrics for display
        report_data = []
        for key, value in self.metrics.items():
            if isinstance(value, float):
                if '$' in key:
                    report_data.append([key, f"${value:,.2f}"])
                elif '%' in key:
                    report_data.append([key, f"{value:.2f}%"])
                else:
                    report_data.append([key, f"{value:.2f}"])
            else:
                report_data.append([key, value])
        
        print(tabulate(report_data, headers=['Metric', 'Value'], tablefmt='grid'))
        print()
        
    def get_metrics(self) -> Dict:
        """Get calculated metrics"""
        if not self.metrics:
            self.calculate_metrics()
        return self.metrics
    
    def compare_to_buy_and_hold(self, data: pd.DataFrame):
        """
        Compare strategy performance to buy-and-hold
        
        Parameters:
        -----------
        data : pd.DataFrame
            Original price data
        """
        buy_hold_return = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100
        strategy_return = self.metrics.get('Total Return (%)', 0)
        
        print(f"\n{'='*60}")
        print(f"STRATEGY vs BUY & HOLD")
        print(f"{'='*60}\n")
        
        comparison = [
            ['Strategy Return', f"{strategy_return:.2f}%"],
            ['Buy & Hold Return', f"{buy_hold_return:.2f}%"],
            ['Difference', f"{(strategy_return - buy_hold_return):.2f}%"],
            ['Outperformance', 'YES ✓' if strategy_return > buy_hold_return else 'NO ✗']
        ]
        
        print(tabulate(comparison, headers=['Metric', 'Value'], tablefmt='grid'))
        print()


