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
    df_price = pd.read_csv(price_file) # load the stock price history into df_price
    df_sent = pd.read_csv(sent_file) # load the AI verdict logs into df_sent
    df_sent = df_sent[df_sent['Ticker'] == ticker] # filter the logs only for thr specified stock ticker

    # remove any timezone information
    if 'Date' not in df_price.columns:
        df_price = df_price.reset_index().rename(columns={'index': 'Date'})
    
    # Clean dates to the same time format, so that they match
    df_price['Date'] = pd.to_datetime(df_price['Date'], utc=True).dt.tz_localize(None)
    df_sent['Timestamp'] = pd.to_datetime(df_sent['Timestamp'])
    
    # Makes the close price interpreted as a number and delete any rows that don't have a close price or a date. 
    df_price['Close'] = pd.to_numeric(df_price['Close'], errors='coerce')
    df_price = df_price.dropna(subset=['Close', 'Date'])

    # Sets up a new two-pane chart
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=False, 
                                   gridspec_kw={'height_ratios': [3, 1]})

    ax1.plot(df_price['Date'], df_price['Close'], color='#1f77b4', linewidth=2, label="Price") # plot a line on the graph based on the data
    ax1.set_title(f"{ticker} Dashboard: Price & AI Mood History", fontsize=16, fontweight='bold') # adds a title
    ax1.set_ylabel("Price (USD)") # Label the y-axis
    ax1.grid(True, alpha=0.3)
    
    # Add the Sentiment dot and bubble at the very end of the line
    last_row = df_sent.iloc[-1]
    mood_color = 'green' if last_row['Label'] == 'Positive' else 'red' if last_row['Label'] == 'Negative' else 'gray'
    ax1.scatter(df_price['Date'].iloc[-1], df_price['Close'].iloc[-1], color=mood_color, s=200, zorder=5)

    # Draw bars on the bar chart for each time the script is ran, changing colors depending on the AI's verdict
    colors = ['green' if x == 'Positive' else 'red' if x == 'Negative' else 'gray' for x in df_sent['Label']]
    ax2.bar(df_sent['Timestamp'], df_sent['Sentiment_Score'], color=colors, width=0.05, label="AI Score")
    
    ax2.axhline(0, color='black', linewidth=0.8) # Baseline (separating positive and negative)
    ax2.set_ylabel("AI Sentiment") # y-axis label
    ax2.set_ylim(-1, 1) # y-axis limits. Scores range from -1 to 1
    ax2.grid(True, alpha=0.3)

    # Format the dates as month-day and rotate it
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.xticks(rotation=45)
    
    plt.tight_layout() # adjust spacing
    print(f"📊 Dashboard generated for {ticker}.")
    plt.show()

if __name__ == "__main__":
    create_market_chart("AAPL") # creates the chart for Apple stocks (AAPL)