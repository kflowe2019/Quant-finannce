import os
import pandas as pd
import yfinance as yf
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import torch
from scraper import run_ticker_scraper
import csv
from datetime import datetime

# Logs the AI's final decisions into a log file
def log_sentiment(ticker, sentiment_score, label):
    log_file = "data/sentiment_history.csv" 
    os.makedirs("data", exist_ok=True) # create file form log_file if doesn't exist
    file_exists = os.path.isfile(log_file)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # grabs current timestamp
    
    with open(log_file, mode='a', newline='') as f: # open log file in append mode
        writer = csv.writer(f)
        if not file_exists: # writes the first row of the file if the file's new
            writer.writerow(['Timestamp', 'Ticker', 'Sentiment_Score', 'Label'])
        writer.writerow([timestamp, ticker, sentiment_score, label]) # write the new row with all of the details (current timestamp, the stock name ticker, the score, and the label)
    print(f"📝 Logged {ticker} sentiment ({label}) to master history.")

# Loads or downloads the FinBERT AI model, and loads the tokenizer
print("🧠 Loading the FinBERT AI model...")
finbert = BertForSequenceClassification.from_pretrained("prosusai/finbert")
tokenizer = BertTokenizer.from_pretrained("prosusai/finbert")
nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer) # combines the model and the tokenizer

# 
def analyze_sentiment(headlines):
    if not headlines: # if the headlines are empty, return a neutral score of 0
        return "Neutral", 0.0
    results = nlp(headlines)
    scores = [res['score'] if res['label'] == 'positive' else -res['score'] if res['label'] == 'negative' else 0 for res in results]
    avg_score = sum(scores) / len(scores)
    verdict = "Positive" if avg_score > 0.15 else "Negative" if avg_score < -0.15 else "Neutral"
    return verdict, avg_score

def process_watchlist(tickers):
    for ticker in tickers:
        print(f"\n" + "="*40)
        # 1. Get Price Data
        print(f"📊 Downloading price data for {ticker}...")
        data = yf.download(ticker, period="1mo", interval="1d")
        data.to_csv(f"data/{ticker}_history.csv")
        
        # 2. Get News & Analyze
        headlines = run_ticker_scraper(ticker)
        verdict, score = analyze_sentiment(headlines)
        print(f"🤖 Verdict for {ticker}: {verdict} ({score:.2f})")
        
        # 3. Log to History
        log_sentiment(ticker, score, verdict)
        
        # 4. Update the history file for the visualizer
        df = pd.read_csv(f"data/{ticker}_history.csv")
        df.loc[df.index[-1], 'AI_Sentiment_Label'] = verdict
        df.loc[df.index[-1], 'AI_Sentiment'] = score
        df.to_csv(f"data/{ticker}_history.csv", index=False)
        print(f"✅ CSV Updated.")

if __name__ == "__main__":
    watchlist = ['AAPL', 'TSLA', 'BTC-USD']
    process_watchlist(watchlist)
    print("\n🏁 All assets updated. Ready for visualization!")