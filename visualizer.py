"""
Visualization Module
Creates charts and plots for backtest results
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Optional
import seaborn as sns

# Set style
sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (14, 10)


class Visualizer:
    """Creates visualizations for backtesting results"""
    
    def __init__(self, results: pd.DataFrame, trades: pd.DataFrame, data: pd.DataFrame):
        """
        Initialize visualizer
        
        Parameters:
        -----------
        results : pd.DataFrame
            Backtest results
        trades : pd.DataFrame
            Trade history
        data : pd.DataFrame
            Original price data with signals
        """
        self.results = results
        self.trades = trades
        self.data = data
        
    def plot_all(self, strategy_name: str = "Strategy", save_path: Optional[str] = None):
        """
        Create comprehensive visualization with multiple subplots
        
        Parameters:
        -----------
        strategy_name : str
            Name of the strategy
        save_path : str, optional
            Path to save the figure
        """
        fig, axes = plt.subplots(4, 1, figsize=(14, 12))
        fig.suptitle(f'{strategy_name} - Backtest Results', fontsize=16, fontweight='bold')
        
        # 1. Price and Trade Signals
        ax1 = axes[0]
        ax1.plot(self.data.index, self.data['Close'], label='Price', linewidth=1.5, color='black', alpha=0.7)
        
        # Plot buy signals
        buy_trades = self.trades[self.trades['type'] == 'BUY']
        if len(buy_trades) > 0:
            ax1.scatter(buy_trades['date'], buy_trades['price'], 
                       marker='^', color='green', s=100, label='Buy', zorder=5)
        
        # Plot sell signals
        sell_trades = self.trades[self.trades['type'] == 'SELL']
        if len(sell_trades) > 0:
            ax1.scatter(sell_trades['date'], sell_trades['price'], 
                       marker='v', color='red', s=100, label='Sell', zorder=5)
        
        ax1.set_title('Price and Trade Signals', fontweight='bold')
        ax1.set_ylabel('Price ($)')
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        
        # 2. Portfolio Value
        ax2 = axes[1]
        ax2.plot(self.results.index, self.results['total'], 
                label='Portfolio Value', linewidth=2, color='blue')
        ax2.axhline(y=self.results['total'].iloc[0], color='gray', 
                   linestyle='--', label='Initial Capital', alpha=0.5)
        ax2.fill_between(self.results.index, self.results['total'], 
                         self.results['total'].iloc[0], alpha=0.3)
        ax2.set_title('Portfolio Value Over Time', fontweight='bold')
        ax2.set_ylabel('Portfolio Value ($)')
        ax2.legend(loc='best')
        ax2.grid(True, alpha=0.3)
        
        # 3. Drawdown
        ax3 = axes[2]
        cumulative = self.results['total']
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max * 100
        
        ax3.fill_between(self.results.index, drawdown, 0, 
                        color='red', alpha=0.3, label='Drawdown')
        ax3.plot(self.results.index, drawdown, color='darkred', linewidth=1)
        ax3.set_title('Drawdown', fontweight='bold')
        ax3.set_ylabel('Drawdown (%)')
        ax3.legend(loc='best')
        ax3.grid(True, alpha=0.3)
        
        # 4. Returns Distribution
        ax4 = axes[3]
        returns = self.results['returns'].dropna() * 100
        ax4.hist(returns, bins=50, color='purple', alpha=0.7, edgecolor='black')
        ax4.axvline(returns.mean(), color='red', linestyle='--', 
                   linewidth=2, label=f'Mean: {returns.mean():.3f}%')
        ax4.set_title('Daily Returns Distribution', fontweight='bold')
        ax4.set_xlabel('Daily Return (%)')
        ax4.set_ylabel('Frequency')
        ax4.legend(loc='best')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Chart saved to {save_path}")
        
        plt.show()
        
    def plot_equity_curve(self, save_path: Optional[str] = None):
        """Plot simple equity curve"""
        plt.figure(figsize=(12, 6))
        plt.plot(self.results.index, self.results['total'], linewidth=2)
        plt.title('Equity Curve', fontsize=14, fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value ($)')
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Chart saved to {save_path}")
        
        plt.show()
        
    def plot_trades_on_price(self, save_path: Optional[str] = None):
        """Plot price chart with buy/sell markers"""
        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index, self.data['Close'], label='Price', linewidth=1.5, color='black')
        
        # Buy signals
        buy_trades = self.trades[self.trades['type'] == 'BUY']
        if len(buy_trades) > 0:
            plt.scatter(buy_trades['date'], buy_trades['price'], 
                       marker='^', color='green', s=150, label='Buy', zorder=5)
        
        # Sell signals
        sell_trades = self.trades[self.trades['type'] == 'SELL']
        if len(sell_trades) > 0:
            plt.scatter(sell_trades['date'], sell_trades['price'], 
                       marker='v', color='red', s=150, label='Sell', zorder=5)
        
        plt.title('Price Chart with Trade Signals', fontsize=14, fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('Price ($)')
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Chart saved to {save_path}")
        
        plt.show()

