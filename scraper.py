import requests
from bs4 import BeautifulSoup

def get_crypto_news():
    url = "https://cryptopanic.com/news/" # Great for high-frequency sentiment
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # This looks for all news titles on the page
    headlines = soup.find_all('a', class_='title-text')
    
    print(f"--- Found {len(headlines)} recent headlines ---")
    for i, title in enumerate(headlines[:5]): # Just show the top 5
        print(f"{i+1}. {title.get_text(strip=True)}")

if __name__ == "__main__":
    get_crypto_news()