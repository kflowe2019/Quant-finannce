import os
import yfinance as yf
from scraper import run_ticker_scraper
from predicter import analyze_sentiment
from data_manager import update_csv_with_sentiment

def download_data(ticker):
    print(f"\n📊 Downloading price data for {ticker}...")
    # '1mo' gives the AI enough context, '1d' keeps the CSV clean
    df = yf.download(ticker, period="1mo", interval="1d", progress=False)
    
    if not os.path.exists('data'): 
        os.makedirs('data')
        
    file_path = f"data/{ticker}_history.csv"
    df.to_csv(file_path)
    print(f"✅ Data saved to {file_path}")

def get_ai_verdict(headlines):
    if not headlines:
        return "Neutral", 0.0
    
    print(f"🧠 AI is analyzing {len(headlines)} headlines...")
    
    scores = []
    for h in headlines:
        label, confidence = analyze_sentiment(h)
        # Convert label to math: Positive = 1, Negative = -1, Neutral = 0
        val = 1 if label == "Positive" else -1 if label == "Negative" else 0
        scores.append(val * confidence)
    
    # Average the scores into one 'Mood' number
    avg_score = sum(scores) / len(scores)
    
    # Determine the final label for the CSV
    final_label = "Positive" if avg_score > 0.1 else "Negative" if avg_score < -0.1 else "Neutral"
    
    return final_label, abs(avg_score)

if __name__ == "__main__":
    # Add any ticker you want here (e.g., "NVDA", "BTC-USD")
    watchlist = ["AAPL", "TSLA", "BTC-USD"]
    
    print(f"🚀 Starting Watchlist Analysis for: {watchlist}")
    
    for stock in watchlist:
        print(f"\n" + "="*40)
        
        # 1. Download Price
        download_data(stock)
        
        # 2. Scrape specific news for this ticker
        headlines = run_ticker_scraper(stock)
        
        # 3. Get AI sentiment score
        label, score = get_ai_verdict(headlines)
        print(f"🤖 Verdict for {stock}: {label} ({score:.2f})")
        
        # 4. Marry the data (Update the CSV)
        update_csv_with_sentiment(stock, label, score)
        
        print("="*40)

    print("\n🏁 All assets updated. Ready for visualization!")