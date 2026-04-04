import requests
from bs4 import BeautifulSoup

def get_market_news():
    print("📰 Fetching latest headlines from CNBC...")
    
    # CNBC is generally easier to scrape for beginners
    url = "https://www.cnbc.com/world-markets/"
    headers = {'User-Agent': 'Mozilla/5.0'} 
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # CNBC uses the class 'Card-title' for their news links
        headlines = soup.find_all('a', class_='Card-title')
        
        if not headlines:
            print("⚠️ Still no luck. Let's try one more fallback...")
            headlines = soup.find_all('div', class_='MarketCard-header')

        print(f"\n--- Top {len(headlines[:10])} Market Headlines ---")
        for i, article in enumerate(headlines[:10]):
            title = article.get_text(strip=True)
            print(f"{i+1}. {title}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    get_market_news()