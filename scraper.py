import requests
from bs4 import BeautifulSoup

def run_ticker_scraper(ticker):
    print(f"🔍 Hunting for {ticker} mentions in latest news...")
    
    # Using the 'Business' and 'Markets' sections which are rich in HTML headlines
    urls = [
        "https://www.cnbc.com/business/",
        "https://www.cnbc.com/markets/"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    headlines = []

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # CNBC uses 'Card-title' for headlines in these sections
            cards = soup.find_all('a', class_='Card-title')
            
            for card in cards:
                text = card.get_text().strip()
                # Only grab the headline if it actually mentions our ticker or company name
                # We'll check for the ticker (AAPL) or common names (Apple)
                if ticker.lower() in text.lower():
                    headlines.append(text)
                
                if len(headlines) >= 5: break # Don't overdo it
        except Exception as e:
            print(f"⚠️ Search error on {url}: {e}")

    if not headlines:
        print(f"💡 No direct {ticker} news found. Grabbing top market headlines instead.")
        # Fallback: Just grab the top 3 general headlines so the AI has SOMETHING to do
        fallback_cards = soup.find_all('a', class_='Card-title')
        for card in fallback_cards[:3]:
            headlines.append(card.get_text().strip())

    return headlines