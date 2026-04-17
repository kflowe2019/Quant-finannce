import pandas as pd
import os

def run_backtest(ticker, initial_capital=1000):
    price_file = f"data/{ticker}_history.csv"
    sent_file = "data/sentiment_history.csv"
    
    if not os.path.exists(price_file) or not os.path.exists(sent_file):
        print("❌ Data missing for backtest.")
        return

    # Load data
    df_price = pd.read_csv(price_file)
    df_sent = pd.read_csv(sent_file)
    df_sent = df_sent[df_sent['Ticker'] == ticker]

    # Clean dates so they match
    df_price['Date'] = pd.to_datetime(df_price['Date'], utc=True).dt.tz_localize(None).dt.date
    df_sent['Date'] = pd.to_datetime(df_sent['Timestamp']).dt.date
    
    # Merge sentiment into price data
    df = pd.merge(df_price, df_sent[['Date', 'Label', 'Sentiment_Score']], on='Date', how='left')
    
    # --- TRADING LOGIC ---
    balance = initial_capital
    position = 0  # Number of shares held
    
    print(f"🚀 Starting Backtest for {ticker} with ${initial_capital}...")
    
    for i in range(len(df)):
        price = df.iloc[i]['Close']
        mood = df.iloc[i]['Label']
        
        # BUY SIGNAL: AI is Positive & we have cash
        if mood == 'Positive' and balance > price:
            position = balance // price
            balance -= (position * price)
            print(f"📅 {df.iloc[i]['Date']}: BOUGHT {position} shares at ${price:.2f}")
            
        # SELL SIGNAL: AI is Negative & we have shares
        elif mood == 'Negative' and position > 0:
            balance += (position * price)
            print(f"📅 {df.iloc[i]['Date']}: SOLD everything at ${price:.2f}")
            position = 0

    # Final Evaluation
    final_value = balance + (position * df.iloc[-1]['Close'])
    profit = final_value - initial_capital
    print(f"\n--- RESULTS ---")
    print(f"Final Account Value: ${final_value:.2f}")
    print(f"Total Profit/Loss: {'🟢' if profit > 0 else '🔴'} ${profit:.2f}")

if __name__ == "__main__":
    run_backtest("AAPL")