from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging
import psycopg2.extras

logger = logging.getLogger(__name__)

def save_articles(articles: list[dict]) -> None:
    """
    Saves a list of articles to the PostgreSQL database.
    Skips duplicates based on the unique `link` column.

    Args:
        articles (List[Dict]): List of article dictionaries with keys:
            - title
            - link (must be unique)
            - summary
            - published
            - tags (list of strings)
    """
    if not articles:
        return

    pg_hook = PostgresHook(postgres_conn_id="articles_db")
    insert_query = """
        INSERT INTO articles (title, link, summary, published, tags)
        VALUES %s
        ON CONFLICT (link) DO NOTHING;
    """

    # Prepare list of tuples for bulk insert
    records = [
        (
            article['title'],
            article['link'],
            article['summary'],
            article['published'],
            article.get('tags', [])  # Should be a list for Postgres ARRAY
        )
        for article in articles
    ]

    try:
        with pg_hook.get_conn() as conn:
            with conn.cursor() as cursor:
                psycopg2.extras.execute_values(
                    cursor, insert_query, records, template=None, page_size=100
                )
            conn.commit()
        _log_pretty_records(records)
    except Exception as e:
        logging.exception("Failed to save articles to the database.")


def _log_pretty_records(records: list[tuple], truncate: int = 80) -> None:
    """
    Logs a pretty summary of article records.

    Args:
        records: List of tuples (title, link, summary, published, tags)
        truncate: Max length of title/summary before truncation
    """
    logging.info(f"Inserted {len(records)} articles into the database.")
    for i, (title, link, summary, published, tags) in enumerate(records, start=1):
        logger.info(
            f"\n[{i}] {published}\n"
            f"Title:   {title[:truncate]}{'...' if len(title) > truncate else ''}\n"
            f"Summary: {summary[:truncate]}{'...' if len(summary) > truncate else ''}\n"
            f"Tags:    {', '.join(tags) if tags else '—'}\n"
            f"Link:    {link}"
        )
