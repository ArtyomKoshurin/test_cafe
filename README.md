# Проект cafe_orders
Проект для заказа столиков с блюдами на сайте кафе.
Техническое задание: https://drive.google.com/drive/folders/1irsS023RO32RO4trOHMhW4rzEykMvbIt?hl=ru

# Установка и развертывание проекта на локальном сервере
1. Склонируйте репозиторий. 
2. Создайте и активируйте виртуальное окружение
```
python -m venv venv
source venv/Scripts/activate
```
3. Перейдите в директорию /cafe_reservation/
4. Установите зависимости из requirements.txt `pip install -r requirements.txt`
5. Создайте .env-файл со значениями SECRET_KEY, DEBUG и ALLOWED_HOSTS
6. Создайте и выполните миграции 
```
python manage.py makemigrations
python manage.py migrate
```
7. Загрузите тестовые данные для блюд `python manage.py testdataloader`
8. Запустите локальный сервер `python manage.py runserver`
9. Веб-сервис будет доступен по эндпоинту https://127.0.0.1:8000/orders/,
а его API - по эндпоинту https://127.0.0.1:8000/api/

# Примеры запросов к сервису:
Запросы к API можно протестировать через Postman или через браузер. 
Используйте тестовые данные блюд из файла data/test_dishes.csv
1. GET-запрос к https://127.0.0.1:8000/api/orders/ - перечень всех заказов
2. POST-запрос к http://127.0.0.1:8000/api/orders/ - создание заказа
Тело запроса:
```
{
    "table_number": 4,
    "items": [
        {
            "name": "Бургер",
            "price": 500
        }
    ]
}
```
3. PUT-запрос к http://127.0.0.1:8000/orders/2/ - изменение статуса заказа или его состава блюд (опционально).
Тело запроса при изменении статуса:
```
{
    "status": "Ready"
}
```
Тело запроса при изменении состава:
```
{
    "items": [
        {
            "name": "Овощи",
            "price": 700
        }
    ],
}
```
4. GET-запрос к http://127.0.0.1:8000/orders/?search=Ready - поиск всех заказов со статусом "Готов".

# Автор:
Кошурин Артём

