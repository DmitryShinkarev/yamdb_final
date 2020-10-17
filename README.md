# API_YamDB

![CI](https://github.com/DmitryShinkarev/yamdb_final/workflows/CI/badge.svg)


REST API для сервиса YaMDb — базы отзывов о фильмах, книгах и музыке.

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title). 
Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором. Читатели могут оставить текстовый отзыв на произведение и выставить оценку от 1 до 10. 
Из общего количества оценок высчитывается для произведения.

Аутентификация по JWT-токену

Поддерживает методы GET, POST, PUT, PATCH, DELETE / Предоставляет данные в формате JSON

## Стек технологий
- проект написан на Python с использованием Django REST Framework
- библиотека Simple JWT - работа с JWT-токеном
- библиотека django-filter - фильтрация запросов
- базы данны - PostgreSQL
- автоматическое развертывание проекта - Docker, docker-compose

## Запуск проекта с помощью Docker (база данных PostgreSQL):

1) Клонируйте проект из репозитория
```
git clone git@github.com:DmitryShinkarev/infra_sp2.git
```
2) В корневой директории проекта создайте файл .env в котором нужно прописать следующие переменные вида:
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```
3) Соберите Docker образ с помощью файлов Dockerfile и docker-compose.yaml
```
docker-compose up --build
```
4) в новом териминале подключитесь к запущеному контейнеру yamdb_web
```
docker container ls
```
```
docker exec -it <CONTAINER_ID> sh
```
5) В контейнере выполняем миграцию, добавляем суперпользователя и заполняем базу с помощью файла fixtures.json
```
python manage.py migrate

python manage.py createsuperuser

python manage.py loaddata fixtures.json
```
____________________________________
Проект будет запущен на http://0.0.0.0:8000/

Полная документация ([redoc.yaml](git@github.com:DmitryShinkarev/infra_sp2.git)) доступна по адресу http://0.0.0.0:8000/redoc/

## Запуск тестов

С помощью команды *pytest* в терминале контейнера можно запустить тесты для проверки работы модулей.

## Алгоритм регистрации пользователей
- Пользователь отправляет запрос с параметрами *email* и *username* на */auth/email/*.
- YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес *email* .
- Пользователь отправляет запрос с параметрами *email* и *confirmation_code* на */auth/token/*, в ответе на запрос ему приходит token (JWT-токен).

## Ресурсы API YaMDb

- Ресурс AUTH: аутентификация.
- Ресурс USERS: пользователи.
- Ресурс TITLES: произведения, к которым пишут отзывы (определённый фильм, книга или песня).
- Ресурс CATEGORIES: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс GENRES: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс REVIEWS: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс COMMENTS: комментарии к отзывам. Комментарий привязан к определённому отзыву.
______________________________________________________________________
### Пример http-запроса (POST) для создания нового комментария к отзыву:
```
url = 'http://0.0.0.0:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/'
data = {'text': 'Your comment'}
headers = {'Authorization': 'Bearer your_token'}
request = requests.post(url, data=data, headers=headers)
```
### Ответ API_YamDB:
```
Статус- код 200

{
 "id": 0,
 "text": "string",
 "author": "string",
 "pub_date": "2020-08-20T14:15:22Z"
}
```

