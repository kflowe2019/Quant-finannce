import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.dates as mdates

def create_market_chart(ticker):
    file_path = f"data/{ticker}_history.csv"
    
    if not os.path.exists(file_path):
        print(f"❌ No data found for {ticker}")
        return

    # 1. LOAD AND CLEAN
    df = pd.read_csv(file_path)
    
    # Drop yfinance's multi-level header if it exists
    if df.iloc[0, 0] == "Price" or "Ticker" in str(df.columns):
        df = df.iloc[1:].copy()

    # 2. THE DATE FIX (No more 1970!)
    if 'Date' not in df.columns:
        df = df.reset_index().rename(columns={'index': 'Date'})

    # Convert to datetime, strip timezones (Matplotlib hates mixed timezones)
    df['Date'] = pd.to_datetime(df['Date'], utc=True).dt.tz_localize(None)
    
    # 3. THE MATH FIX
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df = df.dropna(subset=['Close', 'Date'])
    
    # Sort by date to ensure the line flows left-to-right
    df = df.sort_values('Date')

    # 4. PLOTTING
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot the main price line
    ax.plot(df['Date'], df['Close'], label='Market Price', color='#1f77b4', linewidth=2, alpha=0.8)

    # 5. ADD THE AI BUBBLE
    last_row = df.iloc[-1]
    if 'AI_Sentiment_Label' in df.columns and pd.notna(last_row['AI_Sentiment_Label']):
        sentiment = last_row['AI_Sentiment_Label']
        mood_color = 'green' if sentiment == 'Positive' else 'red' if sentiment == 'Negative' else 'gray'
        
        ax.scatter(last_row['Date'], last_row['Close'], color=mood_color, s=250, 
                   label=f'AI Verdict: {sentiment}', edgecolors='black', zorder=5)
        
        ax.annotate(f"AI MOOD: {sentiment}", 
                     (last_row['Date'], last_row['Close']), 
                     textcoords="offset points", xytext=(0,15), ha='center', 
                     fontweight='bold', color=mood_color,
                     bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=mood_color, alpha=0.8))

    # 6. MAKE THE X-AXIS READABLE
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)

    plt.title(f"{ticker} Analysis: Price Action + AI Sentiment", fontsize=14, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout() # Prevents labels from getting cut off
    
    plt.savefig(f"data/{ticker}_final_report.png")
    print(f"✅ Time-travel fixed! Chart saved.")
    plt.show()

if __name__ == "__main__":
    create_market_chart("AAPL")