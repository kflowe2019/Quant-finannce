import pandas as pd
import os

def run_backtest(ticker, initial_capital=1000):
    price_file = f"data/{ticker}_history.csv"
    sent_file = "data/sentiment_history.csv"
    
    if not os.path.exists(price_file) or not os.path.exists(sent_file):
        print("❌ Data missing for backtest.")
        return

    df_price = pd.read_csv(price_file) # load the stock price history into df_price
    df_sent = pd.read_csv(sent_file) # load the AI verdict logs into df_sent
    df_sent = df_sent[df_sent['Ticker'] == ticker] # filter the logs only for thr specified stock ticker

    # Clean dates to standard time format, so that they match
    df_price['Date'] = pd.to_datetime(df_price['Date'], utc=True).dt.tz_localize(None).dt.date
    df_sent['Date'] = pd.to_datetime(df_sent['Timestamp']).dt.date
    
    # Merge the two history variables together into one price data
    df = pd.merge(df_price, df_sent[['Date', 'Label', 'Sentiment_Score']], on='Date', how='left')
    
    # --- TRADING LOGIC ---
    balance = initial_capital
    position = 0  # Number of shares held
    
    print(f"🚀 Starting Backtest for {ticker} with ${initial_capital}...")
    
    for i in range(len(df)): # goes through the data for every day
        price = df.iloc[i]['Close']
        mood = df.iloc[i]['Label']
        
        # AI says it's Positive and it's a buy
        if mood == 'Positive' and balance > price:
            position = balance // price
            balance -= (position * price)
            print(f"📅 {df.iloc[i]['Date']}: BOUGHT {position} shares at ${price:.2f}")
            
        # AI says it's Negative and it's a sell
        elif mood == 'Negative' and position > 0:
            balance += (position * price)
            print(f"📅 {df.iloc[i]['Date']}: SOLD everything at ${price:.2f}")
            position = 0

    # Calculate the total account value, and the profit
    final_value = balance + (position * df.iloc[-1]['Close'])
    profit = final_value - initial_capital
    print(f"\n--- RESULTS ---")
    print(f"Final Account Value: ${final_value:.2f}")
    print(f"Total Profit/Loss: {'🟢' if profit > 0 else '🔴'} ${profit:.2f}")

if __name__ == "__main__":
    run_backtest("AAPL") # run the test on Apple stocks