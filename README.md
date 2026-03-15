:# Stock Trading Strategy Backtesting Framework

A comprehensive Python-based framework for testing and analyzing stock trading strategies with real market data.

## 🚀 Features

- **Multiple Trading Strategies**: Pre-built strategies including Moving Average Crossover, RSI Mean Reversion, Momentum, and Bollinger Bands
- **Real Market Data**: Automatic fetching of historical stock data from Yahoo Finance
- **Comprehensive Backtesting**: Realistic simulation with commission and slippage modeling
- **Performance Metrics**: Calculate returns, Sharpe ratio, max drawdown, win rate, and more
- **Beautiful Visualizations**: Charts showing equity curves, drawdowns, and trade signals
- **Easy to Extend**: Simple base classes to create your own custom strategies

## 📋 Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## 🔧 Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## 🎯 Quick Start

Run the main example script:

```bash
python main.py
```

This will:
1. Fetch historical data for AAPL (Apple Inc.)
2. Test 4 different trading strategies
3. Display performance metrics for each
4. Generate visualization charts
5. Compare all strategies

## 📊 Available Strategies

### 1. Moving Average Crossover
- **How it works**: Buy when short-term MA crosses above long-term MA, sell when it crosses below
- **Parameters**: `short_window` (default: 20), `long_window` (default: 50)
- **Best for**: Trending markets

### 2. RSI Mean Reversion
- **How it works**: Buy when RSI < 30 (oversold), sell when RSI > 70 (overbought)
- **Parameters**: `rsi_period` (default: 14), `oversold` (default: 30), `overbought` (default: 70)
- **Best for**: Range-bound markets

### 3. Momentum Strategy
- **How it works**: Buy when price momentum is positive, sell when negative
- **Parameters**: `lookback_period` (default: 20), `threshold` (default: 0.02)
- **Best for**: Strong trending markets

### 4. Bollinger Bands
- **How it works**: Buy at lower band, sell at upper band (mean reversion)
- **Parameters**: `window` (default: 20), `num_std` (default: 2.0)
- **Best for**: Mean-reverting markets

## 💡 Usage Examples

### Test a Single Strategy

```python
from data_handler import DataHandler
from strategy import MovingAverageCrossover
from backtest import Backtester
from performance import PerformanceAnalyzer
from visualizer import Visualizer

# Fetch data
data_handler = DataHandler()
data = data_handler.fetch_data('AAPL', start_date='2023-01-01', end_date='2024-12-31')
data = data_handler.add_technical_indicators(data)

# Create strategy
strategy = MovingAverageCrossover(short_window=20, long_window=50)

# Run backtest
backtester = Backtester(initial_capital=100000, commission=0.001)
portfolio = backtester.run(data, strategy)

# Analyze performance
analyzer = PerformanceAnalyzer(portfolio, backtester.get_trades(), 100000)
analyzer.print_report()

# Visualize
signals = strategy.generate_signals(data)
visualizer = Visualizer(portfolio, backtester.get_trades(), signals)
visualizer.plot_all(strategy_name=strategy.name)
```

### Create Your Own Strategy

```python
from strategy import Strategy
import pandas as pd

class MyCustomStrategy(Strategy):
    def __init__(self, param1, param2):
        super().__init__("My Custom Strategy")
        self.param1 = param1
        self.param2 = param2
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        # Your strategy logic here
        # Set df['signal'] to:
        #   1 for buy
        #  -1 for sell
        #   0 for hold
        
        df['signal'] = 0
        # ... your logic ...
        
        df['position'] = df['signal'].diff()
        self.signals = df
        return df
```

## 📈 Performance Metrics

The framework calculates:

- **Total Return**: Overall percentage gain/loss
- **Annualized Return**: Return normalized to yearly basis
- **Volatility**: Standard deviation of returns (annualized)
- **Sharpe Ratio**: Risk-adjusted return metric
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Calmar Ratio**: Return vs drawdown ratio
- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Ratio of gross profit to gross loss
- **Number of Trades**: Total completed trades

## 🎨 Visualizations

The framework generates:

1. **Price Chart with Trade Signals**: Shows buy/sell points on price chart
2. **Equity Curve**: Portfolio value over time
3. **Drawdown Chart**: Visualizes portfolio drawdowns
4. **Returns Distribution**: Histogram of daily returns

## 🔍 Module Overview

- `data_handler.py`: Fetches and manages stock data from Yahoo Finance
- `strategy.py`: Base strategy class and pre-built strategy implementations
- `backtest.py`: Backtesting engine that simulates trading
- `performance.py`: Calculates performance metrics and generates reports
- `visualizer.py`: Creates charts and visualizations
- `main.py`: Example script demonstrating framework usage

## ⚙️ Configuration

Customize backtesting parameters:

```python
backtester = Backtester(
    initial_capital=100000,  # Starting capital
    commission=0.001,        # 0.1% per trade
    slippage=0.0005         # 0.05% slippage
)
```

## 📝 Notes

- Data is fetched from Yahoo Finance (free, no API key required)
- Commission and slippage are applied to simulate realistic trading costs
- Strategies use simple position sizing (all-in or all-out)
- Past performance does not guarantee future results

## 🤝 Contributing

Feel free to extend this framework with:
- New trading strategies
- Additional performance metrics
- More sophisticated position sizing
- Portfolio optimization
- Multi-asset support

## ⚠️ Disclaimer

This framework is for educational purposes only. Do not use it for actual trading without thorough testing and understanding of the risks involved.


