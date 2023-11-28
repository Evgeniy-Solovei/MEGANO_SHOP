MEGANO SHOP
Интернет магазин по продаже товаров.
Проект разработан на фреймворке Django. За отображение страниц отвечает приложение frontend,
а обращение за данными происходит по API, который реализован с использованием Django Rest Framework.

Установка и запуск проекта
Клонировать репозиторий, создать и войти в виртуальное окружение
pip install -r requirements.txt - установка зависимостей
Установка frontend:
cd diploma-frontend && python setup.py sdist - создание архива с библиотекой фронтенда
pip install ./dist/diploma-frontend-0.6.tar.gz - установка фронтенда.

Создание бд и приложений:
cd ../megano && python manage.py make migrations - создание миграций
python manage.py migrate - миграция
python manage.py runserver - запуск сервера
В проекте созданы товары и заказы, а так же суперпользователь(админ):

superuser

Логин: admin

Пароль: admin

