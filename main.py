"""
Main Script - Stock Trading Strategy Backtesting Framework
Demonstrates how to use the framework with example strategies
"""

from data_handler import DataHandler
from strategy import (
    MovingAverageCrossover, 
    RSIMeanReversion, 
    MomentumStrategy, 
    BollingerBandsStrategy
)
from backtest import Backtester
from performance import PerformanceAnalyzer
from visualizer import Visualizer


def main():
    """Main function to run backtesting examples"""
    
    print("="*60)
    print("STOCK TRADING STRATEGY BACKTESTING FRAMEWORK")
    print("="*60)
    
    # Configuration
    SYMBOL = 'AAPL'  # Stock symbol to test
    START_DATE = '2023-01-01'
    END_DATE = '2024-12-31'
    INITIAL_CAPITAL = 100000  # $100,000
    
    # Step 1: Fetch Data
    print(f"\n📊 Fetching data for {SYMBOL}...")
    data_handler = DataHandler()
    data = data_handler.fetch_data(SYMBOL, start_date=START_DATE, end_date=END_DATE)
    
    # Add technical indicators
    data = data_handler.add_technical_indicators(data)
    
    # Step 2: Define Strategies to Test
    strategies = [
        MovingAverageCrossover(short_window=20, long_window=50),
        RSIMeanReversion(rsi_period=14, oversold=30, overbought=70),
        MomentumStrategy(lookback_period=20, threshold=0.02),
        BollingerBandsStrategy(window=20, num_std=2.0)
    ]
    
    # Step 3: Run Backtests
    results_summary = []
    
    for strategy in strategies:
        print(f"\n{'='*60}")
        print(f"Testing Strategy: {strategy.name}")
        print(f"{'='*60}")
        
        # Initialize backtester
        backtester = Backtester(
            initial_capital=INITIAL_CAPITAL,
            commission=0.001,  # 0.1% commission
            slippage=0.0005    # 0.05% slippage
        )
        
        # Run backtest
        portfolio = backtester.run(data, strategy)
        
        # Analyze performance
        analyzer = PerformanceAnalyzer(
            results=portfolio,
            trades=backtester.get_trades(),
            initial_capital=INITIAL_CAPITAL
        )
        
        # Print performance report
        analyzer.print_report()
        analyzer.compare_to_buy_and_hold(data)
        
        # Store results for comparison
        metrics = analyzer.get_metrics()
        results_summary.append({
            'Strategy': strategy.name,
            'Total Return (%)': metrics['Total Return (%)'],
            'Sharpe Ratio': metrics['Sharpe Ratio'],
            'Max Drawdown (%)': metrics['Max Drawdown (%)'],
            'Win Rate (%)': metrics['Win Rate (%)'],
            'Number of Trades': metrics['Number of Trades']
        })
        
        # Visualize results
        print(f"\n📈 Generating charts for {strategy.name}...")
        signals = strategy.generate_signals(data)
        visualizer = Visualizer(
            results=portfolio,
            trades=backtester.get_trades(),
            data=signals
        )
        visualizer.plot_all(strategy_name=strategy.name)
    
    # Step 4: Compare All Strategies
    print(f"\n{'='*60}")
    print("STRATEGY COMPARISON")
    print(f"{'='*60}\n")
    
    import pandas as pd
    from tabulate import tabulate
    
    comparison_df = pd.DataFrame(results_summary)
    print(tabulate(comparison_df, headers='keys', tablefmt='grid', showindex=False))
    
    # Find best strategy
    best_strategy = comparison_df.loc[comparison_df['Total Return (%)'].idxmax()]
    print(f"\n🏆 Best Strategy: {best_strategy['Strategy']}")
    print(f"   Total Return: {best_strategy['Total Return (%)']:.2f}%")
    print(f"   Sharpe Ratio: {best_strategy['Sharpe Ratio']:.2f}")
    
    print(f"\n{'='*60}")
    print("Backtesting Complete!")
    print(f"{'='*60}\n")


def test_single_strategy():
    """Quick test with a single strategy"""
    
    print("\n🚀 Quick Test - Single Strategy\n")
    
    # Fetch data
    data_handler = DataHandler()
    data = data_handler.fetch_data('AAPL', period='1y')
    data = data_handler.add_technical_indicators(data)
    
    # Test Moving Average Crossover
    strategy = MovingAverageCrossover(short_window=20, long_window=50)
    
    # Run backtest
    backtester = Backtester(initial_capital=100000)
    portfolio = backtester.run(data, strategy)
    
    # Analyze
    analyzer = PerformanceAnalyzer(
        results=portfolio,
        trades=backtester.get_trades(),
        initial_capital=100000
    )
    analyzer.print_report()
    analyzer.compare_to_buy_and_hold(data)
    
    # Visualize
    signals = strategy.generate_signals(data)
    visualizer = Visualizer(portfolio, backtester.get_trades(), signals)
    visualizer.plot_all(strategy_name=strategy.name)


if __name__ == "__main__":
    # Run full comparison of all strategies
    main()
    
    # Or run quick test with single strategy
    # test_single_strategy()


