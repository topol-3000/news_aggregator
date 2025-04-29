from celery import Celery

from settings import settings

celery_app = Celery("tech_news_aggregator")

celery_app.conf.broker_url = str(settings.celery.broker_url)
celery_app.conf.result_backend = "rpc://"
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
celery_app.conf.accept_content = ["json"]
celery_app.conf.timezone = "Europe/Kyiv"
celery_app.conf.enable_utc = True
celery_app.conf.task_track_started = True
celery_app.conf.task_time_limit = 30 * 60  # 30 minutes

if settings.celery.with_ssl:
    celery_app.conf.broker_login_method = "PLAIN"
    celery_app.conf.broker_use_ssl = True
