import yfinance as yf
import os

def download_stock_data(ticker, period="2y"):
    print(f"🚀 Starting download for {ticker}...")
    
    # 1. Pull the data from Yahoo Finance
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    
    # 2. Make sure the 'data' folder exists
    if not os.path.exists('data'):
        os.makedirs('data')
        
    # 3. Save it to your data folder
    file_path = f"data/{ticker}_history.csv"
    df.to_csv(file_path)
    
    print(f"✅ Success! Saved {len(df)} days of data to {file_path}")

if __name__ == "__main__":
    # You can change "AAPL" to "TSLA", "BTC-USD", etc.
    download_stock_data("AAPL")