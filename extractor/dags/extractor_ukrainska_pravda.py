from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.exceptions import AirflowSkipException

from extra_src.fetchers.rss import fetch_pravda_articles
from extra_src.categorizers.rule import enrich_with_tags
from extra_src.database.saver import save_articles
from extra_src.database.filter_existed_articles import filter_existing_articles


@dag(
    dag_id="Extractor_Ukrainska_Pravda",
    description="Extracts the news from www.pravda.com.ua",
    schedule=None,
    start_date=datetime(2025, 5, 22),
    catchup=False,
    tags=["RSS Extractors"],
    default_args={
        "depends_on_past": False,
        "retries": 5,
        "retry_delay": timedelta(minutes=5),
    },
)
def pravda_extractor_dag():
    @task
    def fetch() -> list[dict]:
        articles = fetch_pravda_articles()
        if not articles:
            print("No articles found. Skipping downstream tasks.")
            raise AirflowSkipException("No articles to process.")
        return articles

    @task
    def filter_existed_articles(articles: list[dict]) -> list[dict]:
        new_articles = filter_existing_articles(articles)
        if not new_articles:
            print("No new articles found. Skipping downstream tasks.")
            raise AirflowSkipException("No articles to process.")
        return new_articles

    @task
    def enrich_new_articles_with_tags(articles: list[dict]) -> list[dict]:
        return enrich_with_tags(articles)

    @task
    def save_to_db(articles: list[dict]) -> None:
        save_articles(articles)

    save_to_db(enrich_new_articles_with_tags(filter_existed_articles(fetch())))


dag = pravda_extractor_dag()
