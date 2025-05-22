from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging

logger = logging.getLogger(__name__)

def filter_existing_articles(articles:  list[dict]) ->  list[dict]:
    """
    Filters out articles that already exist in the database based on the `link` field.

    Args:
        articles ( list[dict]): List of article dictionaries, each with a `link` key.

    Returns:
         list[dict]: New articles that are not yet in the `articles` table.
    """
    if not articles:
        logging.info("No articles provided for filtering.")
        return []

    links = [article["link"] for article in articles if "link" in article]
    if not links:
        logging.warning("No valid links found in the provided articles.")
        return articles

    try:
        pg_hook = PostgresHook(postgres_conn_id="articles_db")

        with pg_hook.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT link FROM articles WHERE link = ANY(%s);",
                    (links,)
                )
                existing_links = {row[0] for row in cursor.fetchall()}

        new_articles = [article for article in articles if article.get("link") not in existing_links]
        logging.info(f"Filtered out {len(articles) - len(new_articles)} existing articles.")
        logging.info(f"{len(new_articles)} of {len(articles)} are going to be processed.")
        return new_articles

    except Exception as e:
        logging.exception("Error while filtering existing articles from the database.")
        return []
