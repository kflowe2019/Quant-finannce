import yfinance as yf

def get_data(ticker):
    print(f"Fetching data for {ticker}...")
    stock = yf.Ticker(ticker)
    # Get 1 year of daily data
    hist = stock.history(period="1y")
    print(hist.head()) # Shows the first 5 rows
    return hist

if __name__ == "__main__":
    data = get_data("AAPL")
    print("Successfully fetched stock data!")