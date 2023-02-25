__all__ = (
    "NewsApiProcessor",
    "save_news_to_database",
)

import os
import sys

import django
import requests

# if "zoneinfo" in sys.modules:
# import zoneinfo
# elif "backports.zoneinfo" in sys.modules:
from backports import zoneinfo

from datetime import datetime
from http import HTTPStatus

from django.utils import timezone

from config.settings import NEWS_API_TOKEN

# TODO Если кто-то знает как почистить этот хлам и оставить скрипт работоспособным - прошу помочь
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from newsapp.models import News


class NewsApiProcessor:
    def __init__(self, api_url: str, request_params: dict):
        self.api_url = api_url
        self.request_params = request_params
        self._tz = "Europe/Moscow"
        self._default_image_path = "news_image_not_found.svg"

    def _get_news_from_api(self):
        response = requests.get(url=self.api_url, params=self.request_params)
        print(response.url)
        if response.status_code == HTTPStatus.OK:
            self._news = response.json().get("articles") or {}
        else:
            self._news = {}

    def clean_news(self):
        for idx in range(len(self._news)):
            self._news[idx]["source"] = self._news[idx]["source"].get("name")
            self._news[idx]["publishedAt"] = self.clean_datetime(self._news[idx].get("publishedAt"))
            self._news[idx]["urlToImage"] = self._news[idx].get("urlToImage", self._default_image_path)

    def clean_datetime(self, dt_as_string: str) -> datetime:
        if dt_as_string is None:
            return timezone.localtime()
        t = datetime.strptime(dt_as_string, "%Y-%m-%dT%H:%M:%SZ")
        t = datetime(t.year, t.month, t.day, t.hour, t.minute, t.second, tzinfo=zoneinfo.ZoneInfo(self._tz))
        return t

    def get_news(self) -> dict:
        self._get_news_from_api()
        if self._news:
            self.clean_news()
        return self._news


def save_news_to_database() -> int:
    news_interface = NewsApiProcessor(
        api_url="https://newsapi.org/v2/everything",
        request_params={
            "apiKey": NEWS_API_TOKEN,
            "q": "recruitment+hr",
            "language": "en",
            "sortBy": "PublishedAt",
            "pageSize": 10,
            "page": 1,
        },
    )

    created_news_objects = News.objects.bulk_create(
        [
            News(
                title=news_obj.get("title"),
                description=news_obj.get("description"),
                author=news_obj.get("author"),
                content=news_obj.get("content"),
                url=news_obj.get("url"),
                source=news_obj.get("source"),
                image=news_obj.get("urlToImage", "not_found.svg"),
                published_at=news_obj.get("publishedAt"),
                created=news_obj.get("publishedAt"),
            )
            for news_obj in news_interface.get_news()
        ]
    )
    return len(created_news_objects)


if __name__ == "__main__":
    save_news_to_database()
