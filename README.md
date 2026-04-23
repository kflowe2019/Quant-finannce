## Project Members

- **Kenneth Flowe**
- **Thomas Ghirmatsion**
- **Ivan Gorodinski**

# Quant-Finannce

AI-powered quantitative trading system that uses FinBERT sentiment analysis to gather trading data

## Overview

This project combines:
- **Web Scraping** - Fetches latest stock news from Google News
- **AI Sentiment Analysis** - Uses FinBERT to analyze news headlines
- **Backtesting** - Tests trading strategies based on AI signals
- **Visualization** - Charts price and sentiment history

## Project Structure

| File | Description |
|------|-------------|
| `main.py` | Main entry point - downloads data, analyzes sentiment, runs backtests |
| `scraper.py` | Scrapes stock news from Google News RSS feeds |
| `predicter.py` | Standalone sentiment analysis using FinBERT |
| `backtester.py` | Backtesting engine for trading strategies |
| `visualizer.py` | Creates price and sentiment charts |
| `data_manager.py` | Utility for updating CSV files with sentiment data |

## Installation

```bash
pip install -r requirements.txt
```

### Dependencies
- pandas
- yfinance
- transformers
- torch
- scikit-learn
- python-dotenv

### Run Full Analysis
```bash
python main.py
```

This will:
1. Download 1 month of price data for specified tickers
2. Scrape latest news for each ticker
3. Analyze sentiment using FinBERT
4. Log results to `data/sentiment_history.csv`
5. Run backtest and display results

### Analyze Single Headline
```bash
python predicter.py
```

### Visualize Results
```bash
python visualizer.py
```

## How It Works

1. **Data Collection**: Downloads stock prices via yfinance and scrapes news via Google News RSS
2. **Sentiment Analysis**: Uses FinBERT (financial BERT) to classify news as Positive/Negative/Neutral
3. **Trading Strategy**: 
   - BUY when AI sentiment is Positive
   - SELL when AI sentiment is Negative
4. **Backtesting**: Simulates trades to evaluate strategy performance

## Data Output

- `data/{ticker}_history.csv` - Price history for each ticker
- `data/sentiment_history.csv` - Master log of all sentiment analyses

## Requirements

- Python 3.8+
- Internet connection
