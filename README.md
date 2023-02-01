# GBdev2Python
Repository for GB Python for team training development.

## Стек
- Python > 3.8
	- Django  4.1
- VSCode
- SQLLite 3

## Лицензия

MIT

## Как запускать celery и периодические задачи
- В файл ```config/.env``` добавить переменную ```NEWS_API_TOKEN``` со значением ключа от API: https://newsapi.org/
- Запустить Redis, порт по умолчанию 6379 или переназначить CELERY_BROKER_URL и CELERY_RESULT_BACKEND в настройках).
- Вызвать последовательно следующие команды в разных терминалах:
	- celery -A config worker -l info -P eventlet;
	- celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler.
- Profit