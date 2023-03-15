# GBdev2Python
Repository for GB Python for team training development.

## Стек
- Python > 3.8
	- Django  4.1
- VSCode
- SQLLite 3

## Лицензия
MIT

## Как запускать фикстуры
- python manage.py loaddata ./newsapp/fixtures/001_news.json
- python manage.py loaddata ./employerapp/fixtures/customuser_01.json
- python manage.py loaddata ./employerapp/fixtures/skill_01.json
- python manage.py loaddata ./employerapp/fixtures/towns_01.json
- python manage.py loaddata ./employerapp/fixtures/typeEmployment_01.json
- python manage.py loaddata ./employerapp/fixtures/employer_01.json
- python manage.py loaddata ./employerapp/fixtures/vacancyHeader_01.json

## Как запускать celery и периодические задачи
- В файл ```config/.env``` добавить переменную ```NEWS_API_TOKEN``` со значением ключа от API: https://newsapi.org/
- Запустить Redis, порт по умолчанию 6379 или переназначить CELERY_BROKER_URL и CELERY_RESULT_BACKEND в настройках).
- Вызвать последовательно следующие команды в разных терминалах:
	- celery -A config worker -l info -P eventlet;
	- celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler.
- Profit


## Как запускать тесты
- Ставим зависимости из ./test-requirements.txt и качаем selenium webdriver (!Версии, подходящей к версии Chrome!): https://chromedriver.chromium.org/downloads (По-умолчанию копируем chromedriver.exe в C:\chromedriver для винды и **надо сгуглить** для Unix подобных систем + дать права на запуск всем юзерам через chmod)
- Для запуска всех тестов в корне: python manage.py test
- Для избирательного пуска тестов пишем путь через точки, например: python manage.py test hhapp.tests.test_index_page_load_correct.TestCaseIndexPage.test_register_and_login_applicant