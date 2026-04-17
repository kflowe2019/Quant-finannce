import requests
from bs4 import BeautifulSoup

def run_ticker_scraper(ticker):
    print(f"🔍 Searching for specific news on: {ticker}...")
    
    # We use CNBC's search URL format
    search_url = f"https://www.cnbc.com/search/?query={ticker}&qsearchterm={ticker}"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    
    if response.status_status != 200:
        print("❌ Failed to reach CNBC search.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # CNBC search results usually use different CSS classes than the homepage
    # This targets the 'SearchResult-searchResultTitle' class
    headlines = []
    results = soup.find_all('span', class_='SearchResult-searchResultTitle')
    
    for res in results[:5]: # Get the top 5 most recent search results
        headlines.append(res.get_text().strip())
        
    if not headlines:
        print(f"⚠️ No specific headlines found for {ticker}. Trying general news...")
        # (Optional: Fallback to general news if search fails)
        
    return headlines