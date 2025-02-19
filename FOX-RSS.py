import feedparser
import time

RSS_FEED_URL = "https://moxie.foxnews.com/google-publisher/latest.xml"
LAST_PROCESSED_LINK = None  # Keeps track of the last seen article

def fetch_rss_feed():
    """Fetch and parse the RSS feed."""
    return feedparser.parse(RSS_FEED_URL)

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
        "description": latest_article.get("summary", "No Description"),
        "link": latest_article.link,
        "pub_date": latest_article.get("published", "No Date"),
        "image": latest_article.media_content[0]["url"] if hasattr(latest_article, "media_content") else "No Image",
        "source": "Fox News",
        "content": latest_article.get("content", [{"value": "No Content"}])[0]["value"]  # Extract content
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
