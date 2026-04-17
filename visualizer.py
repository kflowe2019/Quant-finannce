import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.dates as mdates

def create_market_chart(ticker):
    price_file = f"data/{ticker}_history.csv"
    sent_file = "data/sentiment_history.csv"
    
    if not os.path.exists(price_file) or not os.path.exists(sent_file):
        print(f"❌ Missing data files. Run main.py first.")
        return

    # 1. LOAD DATA
    df_price = pd.read_csv(price_file)
    df_sent = pd.read_csv(sent_file)
    df_sent = df_sent[df_sent['Ticker'] == ticker] # Only this stock

    # 2. CLEAN DATES
    if 'Date' not in df_price.columns:
        df_price = df_price.reset_index().rename(columns={'index': 'Date'})
    
    df_price['Date'] = pd.to_datetime(df_price['Date'], utc=True).dt.tz_localize(None)
    df_sent['Timestamp'] = pd.to_datetime(df_sent['Timestamp'])
    
    # 3. CLEAN NUMBERS
    df_price['Close'] = pd.to_numeric(df_price['Close'], errors='coerce')
    df_price = df_price.dropna(subset=['Close', 'Date'])

    # 4. CREATE TWO-PANE CHART
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=False, 
                                   gridspec_kw={'height_ratios': [3, 1]})

    # --- TOP: PRICE ---
    ax1.plot(df_price['Date'], df_price['Close'], color='#1f77b4', linewidth=2, label="Price")
    ax1.set_title(f"{ticker} Dashboard: Price & AI Mood History", fontsize=16, fontweight='bold')
    ax1.set_ylabel("Price (USD)")
    ax1.grid(True, alpha=0.3)
    
    # Add the "Current" Sentiment Bubble
    last_row = df_sent.iloc[-1]
    mood_color = 'green' if last_row['Label'] == 'Positive' else 'red' if last_row['Label'] == 'Negative' else 'gray'
    ax1.scatter(df_price['Date'].iloc[-1], df_price['Close'].iloc[-1], color=mood_color, s=200, zorder=5)

    # --- BOTTOM: SENTIMENT HISTORY ---
    # Draw bars for each time you ran the script
    colors = ['green' if x == 'Positive' else 'red' if x == 'Negative' else 'gray' for x in df_sent['Label']]
    ax2.bar(df_sent['Timestamp'], df_sent['Sentiment_Score'], color=colors, width=0.05, label="AI Score")
    
    ax2.axhline(0, color='black', linewidth=0.8) # Baseline
    ax2.set_ylabel("AI Sentiment")
    ax2.set_ylim(-1, 1) # Scores are -1 to 1
    ax2.grid(True, alpha=0.3)

    # Format Dates
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    print(f"📊 Dashboard generated for {ticker}.")
    plt.show()

if __name__ == "__main__":
    create_market_chart("AAPL")