import feedparser
import requests
import time
from bs4 import BeautifulSoup

# Guardian RSS Feed URL
RSS_FEED_URL = "https://www.theguardian.com/world/rss"
LAST_PROCESSED_LINK = None  # Keeps track of the last seen article

def fetch_rss_feed():
    """Fetch and parse the RSS feed."""
    return feedparser.parse(RSS_FEED_URL)

def scrape_article_content(article_url):
    """Scrapes the full article content from a Guardian article."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(article_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Find the article content inside the correct div
        content_div = soup.find("div", class_="article-body-commercial-selector")

        if not content_div:
            return "Content not found"

        # Extract text from all <p> tags inside the content div
        paragraphs = content_div.find_all("p")
        article_text = "\n".join(p.get_text(strip=True) for p in paragraphs)

        return article_text if article_text else "Content not found"

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
        "source": "The Guardian",
        "content": scrape_article_content(latest_article.link)  # Scrape the full article
    }

    # Update last processed link **only after** processing is done
    LAST_PROCESSED_LINK = latest_article.link  

    print("\n===== New Article Found =====")
    for key, value in article_data.items():
        print(f"{key.capitalize()}: {value}")
    print("============================\n")

if __name__ == "__main__":
    print("Starting RSS Fetcher for The Guardian...\n")
    while True:
        process_feed()
        time.sleep(60)  # Check every 60 seconds
