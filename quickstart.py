"""
Quick Start Example
A simple script to get you started with backtesting
"""

from data_handler import DataHandler
from strategy import MovingAverageCrossover
from backtest import Backtester
from performance import PerformanceAnalyzer
from visualizer import Visualizer


def quick_backtest(symbol='AAPL', period='1y', initial_capital=100000):
    """
    Run a quick backtest with Moving Average Crossover strategy
    
    Parameters:
    -----------
    symbol : str
        Stock ticker symbol (e.g., 'AAPL', 'MSFT', 'GOOGL', 'TSLA')
    period : str
        Time period ('1mo', '3mo', '6mo', '1y', '2y', '5y')
    initial_capital : float
        Starting capital in dollars
    """
    
    print(f"\n{'='*60}")
    print(f"Quick Backtest: {symbol}")
    print(f"{'='*60}\n")
    
    # Step 1: Fetch data
    print(f"📊 Fetching {period} of data for {symbol}...")
    data_handler = DataHandler()
    data = data_handler.fetch_data(symbol, period=period)
    data = data_handler.add_technical_indicators(data)
    
    # Step 2: Create strategy
    strategy = MovingAverageCrossover(short_window=20, long_window=50)
    print(f"📈 Using strategy: {strategy.name}")
    
    # Step 3: Run backtest
    backtester = Backtester(
        initial_capital=initial_capital,
        commission=0.001,  # 0.1%
        slippage=0.0005    # 0.05%
    )
    portfolio = backtester.run(data, strategy)
    
    # Step 4: Analyze performance
    analyzer = PerformanceAnalyzer(
        results=portfolio,
        trades=backtester.get_trades(),
        initial_capital=initial_capital
    )
    analyzer.print_report()
    analyzer.compare_to_buy_and_hold(data)
    
    # Step 5: Visualize
    print("\n📊 Generating charts...")
    signals = strategy.generate_signals(data)
    visualizer = Visualizer(portfolio, backtester.get_trades(), signals)
    visualizer.plot_all(strategy_name=f"{strategy.name} - {symbol}")
    
    print(f"\n✅ Backtest complete!\n")
    
    return portfolio, analyzer


if __name__ == "__main__":
    # Example 1: Test Apple stock for 1 year
    quick_backtest('AAPL', period='1y', initial_capital=100000)
    
    # Example 2: Test other stocks (uncomment to try)
    # quick_backtest('MSFT', period='2y', initial_capital=50000)
    # quick_backtest('GOOGL', period='1y', initial_capital=100000)
    # quick_backtest('TSLA', period='1y', initial_capital=100000)


