import requests
from bs4 import BeautifulSoup
from predicter import analyze_sentiment # This connects your two files!

def run_smart_scraper():
    print("📰 Fetching headlines and running AI analysis...")
    url = "https://www.cnbc.com/world-markets/"
    headers = {'User-Agent': 'Mozilla/5.0'} 
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.find_all('a', class_='Card-title')

        print(f"\n--- Live Market Sentiment Analysis ---")
        
        # We'll just check the top 5 to keep it fast
        for i, article in enumerate(headlines[:5]):
            title = article.get_text(strip=True)
            
            # Here is where the magic happens: 
            # We send the headline to your predicter.py file
            sentiment, confidence = analyze_sentiment(title)
            
            # Visual feedback
            icon = "✅" if sentiment == "Positive" else "❌" if sentiment == "Negative" else "⚖️"
            
            print(f"{i+1}. {title}")
            print(f"   {icon} AI Score: {sentiment} ({confidence:.2%})\n")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_smart_scraper()