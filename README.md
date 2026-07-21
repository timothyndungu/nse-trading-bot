# NSE Trading Bot - AI-Powered Algorithmic Trading

An intelligent trading bot designed for the Nairobi Securities Exchange (NSE) that uses machine learning and technical analysis to execute automated trades.

## Features

- 📊 **Real-time Data Collection**: Fetches live NSE market data
- 🤖 **ML-Powered Predictions**: LSTM and XGBoost models for price forecasting
- 📈 **Technical Analysis**: Multiple indicators (RSI, MACD, Bollinger Bands, etc.)
- 🎯 **Algorithmic Trading**: Automated trade execution with risk management
- 📉 **Backtesting**: Test strategies against historical data
- 💼 **Portfolio Management**: Position sizing and diversification
- 🛡️ **Risk Controls**: Stop-loss, take-profit, drawdown limits
- 📱 **Monitoring Dashboard**: Real-time performance tracking
- 🔔 **Alerts & Logging**: Email/SMS notifications for trades

## Project Structure

```
nse-trading-bot/
├── data/
│   ├── raw/                    # Raw NSE data
│   ├── processed/              # Processed data for models
│   └── historical/             # Historical price data
├── src/
│   ├── data_collection/        # NSE data fetching
│   ├── models/                 # ML models (LSTM, XGBoost)
│   ├── strategies/             # Trading strategies
│   ├── indicators/             # Technical indicators
│   ├── trading_engine/         # Core trading logic
│   ├── broker_integration/     # Broker APIs
│   ├── risk_management/        # Risk controls
│   ├── backtesting/            # Backtest framework
│   └── utils/                  # Utility functions
├── config/
│   ├── settings.py             # Global configurations
│   ├── credentials.py          # API credentials (gitignored)
│   └── constants.py            # Trading constants
├── notebooks/                  # Jupyter notebooks for analysis
├── tests/                      # Unit tests
├── dashboard/                  # Web dashboard
├── logs/                       # Trading logs
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
└── main.py                     # Bot entry point
```

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup

1. Clone the repository:
```bash
git clone https://github.com/timothyndungu/nse-trading-bot.git
cd nse-trading-bot
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure credentials:
```bash
cp config/credentials.example.py config/credentials.py
# Edit config/credentials.py with your broker API keys
```

## Quick Start

### 1. Collect Historical Data
```python
python -m src.data_collection.nse_fetcher --download-historical
```

### 2. Train ML Models
```python
python -m src.models.train_models --stocks all --lookback 252
```

### 3. Backtest Strategy
```python
python -m src.backtesting.backtest --strategy momentum --start-date 2023-01-01 --end-date 2024-01-01
```

### 4. Run Live Trading
```python
python main.py --mode live
```

## Data Sources

### Free Data APIs
- **[Alpha Vantage](https://www.alphavantage.co/)** - Stock data (500 req/day free tier)
- **[yfinance](https://github.com/ranaroussi/yfinance)** - Yahoo Finance data (unlimited, community supported)
- **[NSE Kenya Direct](https://www.nse.co.ke)** - Official NSE website scraping

### Paid Data Sources
- **[IEX Cloud](https://iexcloud.io/)** - Professional market data ($99/month)
- **[Polygon.io](https://polygon.io/)** - Stock & crypto data
- **[Alpaca Markets](https://alpaca.markets/)** - Free paper trading + data

## Trading Strategies

### Implemented Strategies
1. **Momentum Trading** - Trades on price momentum using technical indicators
2. **Mean Reversion** - Exploits overbought/oversold conditions
3. **Trend Following** - Follows established price trends
4. **Statistical Arbitrage** - Multi-stock correlation trading
5. **ML-Predicted Entry/Exit** - AI model-based signals

## Configuration

Edit `config/settings.py` to customize:
- Trading symbols
- Position sizing rules
- Risk parameters (max drawdown, stop-loss %)
- Technical indicator parameters
- ML model hyperparameters

## Backtesting

Run backtests to validate strategies:
```python
from src.backtesting.backtest import Backtester
from src.strategies.momentum import MomentumStrategy

bt = Backtester(
    strategy=MomentumStrategy(),
    start_date='2023-01-01',
    end_date='2024-01-01',
    initial_capital=1000000
)
results = bt.run()
bt.plot_results()
```

## Monitoring & Logging

- All trades logged to `logs/trades.log`
- Performance metrics saved to `logs/performance.json`
- Real-time dashboard at `http://localhost:5000`

## Risk Management

- **Max Portfolio Drawdown**: 20%
- **Per-Trade Risk**: 2% of portfolio
- **Position Sizing**: Kelly Criterion or Fixed Fractional
- **Stop-Loss**: Automatic on all positions
- **Circuit Breaker**: Halts trading on excessive losses

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Disclaimer

⚠️ **This bot is for educational purposes only.** 
- Past performance doesn't guarantee future results
- Always backtest thoroughly before live trading
- Start with paper trading first
- Never risk more than you can afford to lose
- The NSE and your broker may have specific rules about algorithmic trading

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or feature requests: [GitHub Issues](https://github.com/timothyndungu/nse-trading-bot/issues)

## Resources

- [NSE Website](https://www.nse.co.ke)
- [Python Finance Libraries](https://pandas.pydata.org/)
- [Machine Learning Trading](https://www.coursera.org/learn/machine-learning-trading)
- [Technical Analysis Guide](https://www.investopedia.com/terms/t/technicalanalysis.asp)

---

**Last Updated**: 2026-07-21
