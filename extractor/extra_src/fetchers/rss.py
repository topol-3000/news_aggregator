import feedparser
import logging
from datetime import datetime, UTC

from airflow.sdk import Variable

logger = logging.getLogger(__name__)

def fetch_pravda_articles() ->  list[dict]:
    """
    Fetches and parses RSS feed from Ukrainska Pravda.
    Returns a list of articles with keys: title, link, summary, published.

    Returns:
         list[dict]: Parsed articles from the feed.
    """
    url = Variable.get("rss_ukrainska_pravda_feed")
    try:
        feed = feedparser.parse(url)

        if feed.bozo:
            logger.warning(f"Malformed feed (bozo=True): {feed.bozo_exception}")
            return []

        if not feed.entries:
            logger.info("Feed parsed successfully but contains no entries.")
            return []

        articles = []
        for entry in feed.entries:
            article = {
                "title": entry.get("title", "").strip(),
                "link": entry.get("link", "").strip(),
                "summary": entry.get("summary", "").strip(),
                "published": entry.get("published", datetime.now(UTC).isoformat()),
            }
            articles.append(article)

        logger.info(f"Fetched {len(articles)} articles from RSS feed.")
        return articles

    except Exception as e:
        logger.exception("Failed to fetch or parse the RSS feed.")
        return []
