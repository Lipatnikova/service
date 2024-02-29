# task_API
_Практикум SDET: задание API_


![Python Version](https://img.shields.io/badge/python-3.10-blue)
[![dependency - pytest](https://img.shields.io/badge/dependency-pytest-blue?logo=pytest&logoColor=white)](https://pypi.org/project/pytest)
[![dependency - Faker](https://img.shields.io/badge/dependency-Faker-blue)](https://pypi.org/project/Faker)
[![dependency - allure-pytest](https://img.shields.io/badge/dependency-allure--pytest-blue?logo=qameta&logoColor=white)](https://pypi.org/project/allure-pytest)

Тест-кейсы: [ТЕСТ-КЕЙСЫ](https://github.com/Lipatnikova/service/blob/task_API/TEST_CASES.md)

## Как работать с репозиторием на ПК:

1. Склонировать репозиторий `git clone "Clone using the web URL"`.
2. Перейти в директорию проекта.
3. Создать виртуальное окружение `python -m venv venv`.
4. Активировать виртуальное окружение для Windows: `venv\Scripts\activate.bat`; для Linux и MacOS: `source venv/bin/activate`.
5. Установить зависимости `pip install -r requirements.txt`.
6. Склонировать себе и развернуть [проект](https://github.com/sun6r0/test-service) (инструкция в репозитории)
6. Запустить тесты:
6. 1. Чтобы запустить тесты использовать команду `pytest -s -v`.
6. 2. Чтобы запустить тесты  с генерацией отчета Allure использовать команду `pytest -s -v --alluredir allure-results`.
6. 3. Чтобы запустить тесты  **параллельно** с генерацией отчета Allure использовать команду `pytest -s -v -n=2 --alluredir allure-results`.
7. Просмотреть отчет Allure `allure serve allure-results`.


## Задание для Python:

1. Склонировать себе и развернуть [проект](https://github.com/sun6r0/test-service) (инструкция в репозитории)
2. На языке программирования Python (версия 3.10) создать
проект из пяти API-автотестов для всех точек доступа к приложению (только положительные кейсы).
3. В проекте использовать:
- Python - requests
- Одну из библиотек для сериализации/десериализации: Python –
jsonschema, pydantic (все полученные данные должны быть обязательно (!)
десериализованы в объекты).
- Один из тестовых фреймворков: Python - pytest
4. Результаты на проверку оформить в виде Merge Request/Pull Request (!!!) ветки в которой 
вы вели разработку в главную на Gitlab/GitHub.
5. Дополнительное задание №1: Реализовать формирование отчетов Allure.
6. Дополнительное задание №2: Реализовать параллельный запуск тестов.
7. Дополнительное задание №3: Реализовать запуск в системе CI/CD.
