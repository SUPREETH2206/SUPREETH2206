"""
BBC News Headline Scraper
Task 3: Web Scraper for News Headlines
Objective: Scrape top headlines from BBC News website
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# --- Configuration ---
URL = "https://www.bbc.com/news"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5'  # Helps get English content
}
TIMEOUT = 10  # seconds
OUTPUT_FILE = "bbc_headlines.txt"

def fetch_html(url):
    """Fetch HTML content from URL with error handling"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

def extract_headlines(html):
    """Extract headlines from HTML using BeautifulSoup"""
    soup = BeautifulSoup(html, 'html.parser')

    # Updated selectors to make it more resilient to layout changes
    selectors = [
        'h3.gs-c-promo-heading__title', # A common selector for headlines on BBC
        'a.gs-c-promo-heading',  # Fallback selector for links with this class
        'h2', # General H2 tags
        'h3'  # General H3 tags
    ]

    headlines = []
    for selector in selectors:
        elements = soup.select(selector) # Use select for CSS selectors
        if elements:
            for el in elements:
                text = el.get_text(strip=True)
                if text and len(text.split()) > 2:  # Filter out short fragments
                    headlines.append(text)
            if headlines: # Stop at the first selector that finds headlines
              break

    return list(set(headlines))[:20]  # Remove duplicates and limit to top 20

def save_headlines(headlines, filename):
    """Save headlines to text file with timestamp"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"BBC News Headlines - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            for idx, headline in enumerate(headlines, 1):
                f.write(f"{idx}. {headline}\n")
        print(f"✅ Saved {len(headlines)} headlines to {filename}")
    except IOError as e:
        print(f"❌ Error writing to file: {e}")

def main():
    """Main execution function"""
    print("🔄 Fetching BBC News headlines...")

    html = fetch_html(URL)
    if not html:
        return

    headlines = extract_headlines(html)
    if not headlines:
        print("⚠️ No headlines found. The website structure may have changed.")
        return

    save_headlines(headlines, OUTPUT_FILE)

if __name__ == "__main__":
    main()
    # Fetch the HTML content again to inspect it
html_content = fetch_html(URL)

if html_content:
    print("HTML content fetched successfully. Inspecting the first 2000 characters to identify headline selectors.")
    print(html_content[:2000])
    # You would typically view the full source of the page in a browser's developer tools
    # to accurately determine the correct selectors.
else:
    print("Failed to fetch HTML content for inspection.")
