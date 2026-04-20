import requests
from bs4 import BeautifulSoup

def run_ticker_scraper(ticker):
    print(f"🔍 Hunting for SPECIFIC {ticker} news on Google News...")
    
    # URL in RSS format with a stock ticker (like AAPL) in there and with the rule that only filters news within a day
    url = f"https://news.google.com/rss/search?q={ticker}+stock+when:1d&hl=en-US&gl=US&ceid=US:en"
    
    headers = {'User-Agent': 'Mozilla/5.0'} # sets a user agent to pretend it's a browser
    headlines = []

    try:
        response = requests.get(url, headers=headers, timeout=10) # visit URL
        # RSS is in XML format, so we use the xml parser, and e
        soup = BeautifulSoup(response.text, 'xml') 
        
        # Finds all of the <item> tags, since Google News uses <item> tags for every story
        items = soup.find_all('item')
        
        for item in items:
            title = item.title.text
            # Removes the " - Source Name" at the end of the title
            clean_title = title.split(' - ')[0]
            headlines.append(clean_title)
            
            if len(headlines) >= 10: break # Limit to top 10 articles, instead of like hundreds of articles, just to efficiency sakes
            
    except Exception as e:
        print(f"⚠️ Search error for {ticker}: {e}")

    if not headlines:
        print(f"💡 Still no specific news for {ticker}. Check ticker symbol.")
        return ["Market is currently stable with no major news updates."]

    return headlines