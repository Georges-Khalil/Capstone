import feedparser
import requests
import time
from bs4 import BeautifulSoup

RSS_FEED_URL = "https://www.lbcgroup.tv/Rss/latest-news/en"
LAST_PROCESSED_LINK = None  # Keeps track of the last seen article

def fetch_rss_feed():
    """Fetch and parse the RSS feed."""
    return feedparser.parse(RSS_FEED_URL)

def scrape_article_content(article_url):
    """Scrapes the full article content from the given URL."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(article_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Find the main content using the correct class
        article_body = soup.find("div", class_="LongDesc")
        if article_body:
            return article_body.get_text(separator="\n", strip=True)  # Extract and clean text
        
        return "Content not found"
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching content: {e}"

def process_feed():
    """Fetches new articles and processes them if they are new."""
    global LAST_PROCESSED_LINK
    feed = fetch_rss_feed()

    if not feed.entries:
        print("No articles found in RSS feed.")
        return

    latest_article = feed.entries[0]  # The newest article in the feed

    if LAST_PROCESSED_LINK == latest_article.link:
        print("No new articles.")
        return

    # Extract required fields
    article_data = {
        "title": latest_article.title,
        "description": latest_article.description,
        "link": latest_article.link,
        "pub_date": latest_article.published,
        "image": latest_article.media_content[0]["url"] if hasattr(latest_article, "media_content") else "No Image",
        "source": "LBCI",
        "content": scrape_article_content(latest_article.link)  # Scrape the full article
    }

    # Update last processed link **only after** processing is done
    LAST_PROCESSED_LINK = latest_article.link  

    print("\n===== New Article Found =====")
    for key, value in article_data.items():
        print(f"{key.capitalize()}: {value}")
    print("============================\n")

if __name__ == "__main__":
    print("Starting RSS Fetcher...\n")
    while True:
        process_feed()
        time.sleep(60)  # Check every 60 seconds
