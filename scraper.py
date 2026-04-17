import requests
from bs4 import BeautifulSoup

def run_ticker_scraper(ticker):
    print(f"🔍 Hunting for SPECIFIC {ticker} news on Google News...")
    
    # URL for specific ticker search in RSS format
    url = f"https://news.google.com/rss/search?q={ticker}+stock+when:1d&hl=en-US&gl=US&ceid=US:en"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    headlines = []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        # RSS is XML, so we use the xml parser
        soup = BeautifulSoup(response.text, 'xml') 
        
        # Google News RSS uses <item> tags for each story
        items = soup.find_all('item')
        
        for item in items:
            title = item.title.text
            # Clean up the title (remove the " - Source Name" at the end)
            clean_title = title.split(' - ')[0]
            headlines.append(clean_title)
            
            if len(headlines) >= 10: break # Limit to top 10 for speed
            
    except Exception as e:
        print(f"⚠️ Search error for {ticker}: {e}")

    if not headlines:
        print(f"💡 Still no specific news for {ticker}. Check ticker symbol.")
        return ["Market is currently stable with no major news updates."]

    return headlines