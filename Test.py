import feedparser

RSS_FEED_URL = "https://moxie.foxnews.com/google-publisher/latest.xml"

def fetch_rss_feed():
    """Fetch and parse the RSS feed."""
    return feedparser.parse(RSS_FEED_URL)

feed = fetch_rss_feed()

if feed.entries:
    latest_article = feed.entries[0]
    print(latest_article.keys())  # Print all available attributes
else:
    print("No articles found.")
