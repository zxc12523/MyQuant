# Trading Strategies Explained

This document explains the trading strategies included in the framework and when to use them.

## 📚 Strategy Overview

### 1. Moving Average Crossover Strategy

**Type**: Trend Following

**How it Works**:
- Calculates two moving averages: a short-term (fast) and a long-term (slow)
- **Buy Signal**: When the short MA crosses above the long MA (Golden Cross)
- **Sell Signal**: When the short MA crosses below the long MA (Death Cross)

**Parameters**:
- `short_window`: Period for short-term MA (default: 20 days)
- `long_window`: Period for long-term MA (default: 50 days)

**Best Used When**:
- Markets are trending (up or down)
- You want to capture medium to long-term trends
- Avoiding choppy, sideways markets

**Pros**:
- Simple and easy to understand
- Good for capturing major trends
- Reduces noise with smoothing

**Cons**:
- Lags behind price action
- Generates false signals in sideways markets
- May miss early entry points

**Example**:
```python
strategy = MovingAverageCrossover(short_window=20, long_window=50)
```

---

### 2. RSI Mean Reversion Strategy

**Type**: Mean Reversion

**How it Works**:
- Uses the Relative Strength Index (RSI) to identify overbought/oversold conditions
- RSI ranges from 0 to 100
- **Buy Signal**: When RSI < 30 (oversold - price likely to bounce back up)
- **Sell Signal**: When RSI > 70 (overbought - price likely to fall back down)

**Parameters**:
- `rsi_period`: Lookback period for RSI calculation (default: 14 days)
- `oversold`: Threshold for oversold condition (default: 30)
- `overbought`: Threshold for overbought condition (default: 70)

**Best Used When**:
- Markets are range-bound (moving sideways)
- Stock tends to revert to its mean price
- Looking for short-term trading opportunities

**Pros**:
- Works well in sideways markets
- Clear entry/exit signals
- Can catch price extremes

**Cons**:
- Poor performance in strong trends
- Can stay overbought/oversold for extended periods
- May generate many false signals

**Example**:
```python
strategy = RSIMeanReversion(rsi_period=14, oversold=30, overbought=70)
```

---

### 3. Momentum Strategy

**Type**: Momentum/Trend Following

**How it Works**:
- Measures the rate of price change over a lookback period
- **Buy Signal**: When momentum exceeds positive threshold (strong upward movement)
- **Sell Signal**: When momentum falls below negative threshold (strong downward movement)

**Parameters**:
- `lookback_period`: Period to calculate momentum (default: 20 days)
- `threshold`: Minimum momentum to trigger signal (default: 0.02 or 2%)

**Best Used When**:
- Markets show strong directional movement
- You want to ride momentum waves
- Stocks are breaking out or breaking down

**Pros**:
- Captures strong price movements
- Can generate high returns in trending markets
- Adapts to market volatility

**Cons**:
- Can whipsaw in choppy markets
- May enter late in a trend
- Requires careful threshold tuning

**Example**:
```python
strategy = MomentumStrategy(lookback_period=20, threshold=0.02)
```

---

### 4. Bollinger Bands Strategy

**Type**: Mean Reversion / Volatility

**How it Works**:
- Creates bands around a moving average based on standard deviation
- Bands expand during high volatility, contract during low volatility
- **Buy Signal**: When price touches or crosses below the lower band
- **Sell Signal**: When price touches or crosses above the upper band

**Parameters**:
- `window`: Period for moving average (default: 20 days)
- `num_std`: Number of standard deviations for bands (default: 2.0)

**Best Used When**:
- Markets are range-bound
- You want to exploit volatility
- Price tends to revert to the mean

**Pros**:
- Adapts to volatility automatically
- Visual and intuitive
- Works well for mean reversion

**Cons**:
- Can give false signals in strong trends
- Bands can "walk" during trends
- Requires understanding of volatility

**Example**:
```python
strategy = BollingerBandsStrategy(window=20, num_std=2.0)
```

---

## 🎯 Choosing the Right Strategy

### Market Conditions Guide

| Market Condition | Best Strategy | Why |
|-----------------|---------------|-----|
| **Strong Uptrend** | Moving Average Crossover, Momentum | Captures sustained directional movement |
| **Strong Downtrend** | Moving Average Crossover | Helps exit positions early |
| **Sideways/Range-bound** | RSI Mean Reversion, Bollinger Bands | Profits from price oscillations |
| **High Volatility** | Bollinger Bands | Adapts to changing volatility |
| **Low Volatility** | Momentum | Catches breakouts from consolidation |

### Strategy Comparison

| Strategy | Complexity | Trade Frequency | Best Market | Risk Level |
|----------|-----------|----------------|-------------|------------|
| MA Crossover | Low | Low | Trending | Medium |
| RSI Mean Reversion | Medium | Medium-High | Range-bound | Medium-High |
| Momentum | Medium | Medium | Trending | High |
| Bollinger Bands | Medium | Medium | Range-bound | Medium |

---

## 💡 Tips for Success

1. **Backtest Multiple Periods**: Test strategies across different time periods and market conditions
2. **Combine Strategies**: Consider using multiple strategies together for confirmation
3. **Adjust Parameters**: Tune parameters based on the specific stock and timeframe
4. **Consider Transaction Costs**: Always include commission and slippage in backtests
5. **Risk Management**: Use stop-losses and position sizing in real trading
6. **Avoid Overfitting**: Don't optimize too much on historical data
7. **Paper Trade First**: Test strategies with paper trading before using real money

---

## 🔬 Advanced Concepts

### Parameter Optimization
You can test different parameter combinations to find optimal settings:

```python
for short in [10, 20, 30]:
    for long in [50, 100, 200]:
        strategy = MovingAverageCrossover(short, long)
        # Run backtest and compare results
```

### Combining Indicators
Create custom strategies that combine multiple indicators:

```python
# Buy only when both MA crossover AND RSI is oversold
# This provides confirmation and reduces false signals
```

---

## ⚠️ Important Reminders

- **Past performance ≠ Future results**: Historical backtests don't guarantee future profits
- **Market conditions change**: A strategy that worked in the past may not work in the future
- **Risk management is crucial**: Always use stop-losses and proper position sizing
- **Start small**: Test with small amounts before scaling up
- **Keep learning**: Markets evolve, and so should your strategies


