import pandas as pd
import matplotlib.pyplot as plt

def create_market_chart(ticker):
    file_path = f"data/{ticker}_history.csv"
    
    # 1. Load the data
    df = pd.read_csv(file_path)
    print(f"Columns found in CSV: {df.columns.tolist()}") # This helps us debug!

    # 2. Identify the Sentiment Column
    # We check for common names we might have used
    sent_col = None
    for col in ['AI_Sentiment', 'Sentiment_Score', 'sentiment']:
        if col in df.columns:
            sent_col = col
            break
    
    if not sent_col:
        print(f"❌ Error: Could not find a sentiment column in {file_path}")
        print("Double check your data_manager.py to see what it named the column.")
        return

    # 3. Clean up the dates and timezones
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', utc=True) 
    
    # 4. Drop rows that are missing the data we need to graph
    df = df.dropna(subset=['Date', sent_col])

    if df.empty:
        print(f"⚠️ No matching data found (rows with both Price and Sentiment).")
        return

    # 5. Setup the plot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot Price (Left)
    color_price = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Stock Price ($)', color=color_price)
    ax1.plot(df['Date'], df['Close'], color=color_price, label='Price')

    # Plot Sentiment (Right)
    ax2 = ax1.twinx() 
    color_sent = 'tab:red'
    ax2.set_ylabel('AI Sentiment', color=color_sent)
    ax2.plot(df['Date'], df[sent_col], color=color_sent, linestyle='--', marker='o', label='AI Mood')
    ax2.set_ylim(-1.1, 1.1) 

    plt.title(f'Market Analysis: {ticker}')
    plt.savefig(f"data/{ticker}_chart.png")
    print(f"📈 Chart created successfully!")
    plt.show()

if __name__ == "__main__":
    create_market_chart("AAPL")