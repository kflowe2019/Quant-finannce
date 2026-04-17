import pandas as pd
from predicter import analyze_sentiment

def add_sentiment_to_csv(ticker, headlines):
    print(f"📊 Marrying news data to {ticker} CSV...")
    
    # 1. Calculate an 'Average Sentiment' for today's news
    scores = []
    for h in headlines:
        sentiment, confidence = analyze_sentiment(h)
        # Convert to a number: Positive = 1, Negative = -1, Neutral = 0
        val = 1 if sentiment == "Positive" else -1 if sentiment == "Negative" else 0
        scores.append(val * confidence)
    
    avg_score = sum(scores) / len(scores) if scores else 0

    # 2. Open your existing CSV
    file_path = f"data/{ticker}_history.csv"
    df = pd.read_csv(file_path)

    # 3. Add the sentiment to the very last row (today's data)
    # Note: This is a simple version that adds it to the most recent entry
    df.loc[df.index[-1], 'Sentiment_Score'] = avg_score

    # 4. Save it back
    df.to_csv(file_path, index=False)
    print(f"✅ CSV Updated! Latest Sentiment Score: {avg_score:.2f}")

if __name__ == "__main__":
    # Test run
    sample_news = ["Apple sales are booming", "iPhone production delayed"]
    add_sentiment_to_csv("AAPL", sample_news)