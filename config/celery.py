import os

from celery import Celery

from newsapp.tasks import save_news_to_database

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = Celery("newsapp")
application.config_from_object("django.conf:settings", namespace="CELERY")
application.autodiscover_tasks()


@application.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(14_400.00, get_news.s(), name="Get news and save to db")


@application.task
def get_news():
    print(f"saved {save_news_to_database()} news total")
