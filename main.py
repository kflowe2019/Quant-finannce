import os
import yfinance as yf
from scraper import run_smart_scraper

def download_data(ticker):
    print(f"\n📊 Downloading price data for {ticker}...")
    df = yf.download(ticker, period="1mo", progress=False)
    if not os.path.exists('data'): os.makedirs('data')
    df.to_csv(f"data/{ticker}_history.csv")
    print(f"✅ Data saved to data/{ticker}_history.csv")

def get_verdict(ticker):
    print(f"🤖 AI Analysis for {ticker}:")
    # This calls your smart scraper (which now uses the AI)
    # Note: In a future version, we can make the scraper search 
    # specifically for the ticker name!
    run_smart_scraper() 

if __name__ == "__main__":
    # Add as many as you want here!
    watchlist = ["AAPL", "TSLA", "BTC-USD"]
    
    print(f"🌟 Starting AI Watchlist Analysis for: {watchlist}")
    
    for stock in watchlist:
        print(f"\n" + "="*30)
        download_data(stock)
        get_verdict(stock)
        print("="*30)
        
    print("\n🏁 All assets analyzed. Check your 'data' folder!")