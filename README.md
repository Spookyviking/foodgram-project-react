# Foodgram

## Технологический стек
[![Foodgram workflow](https://github.com/Spookyviking/foodgram-project-react/actions/workflows/Foodgram-workflow.yml/badge.svg)](https://github.com/Spookyviking/foodgram-project-react/actions/workflows/Foodgram-workflow.yml)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=008080)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)

## Приложение «Продуктовый помощник»
Cайт, на котором пользователи могут публиковать рецепты,
добавлять чужие рецепты в избранное и подписываться на публикации других авторов.
Сервис **«Список покупок»** позволит пользователям создавать список продуктов, которые
нужно купить для приготовления выбранных блюд.

## Описание проекта

### Главная страница
Содержимое главной страницы — список первых шести рецептов,
отсортированных по дате публикации (от новых к старым).
Остальные рецепты доступны на следующих страницах: внизу страницы есть пагинация.
### Страница рецепта
На странице — полное описание рецепта. Для авторизованных пользователей — 
возможность добавить рецепт в избранное и в список покупок, возможность
подписаться на автора рецепта.
### Страница пользователя
На странице — имя пользователя, все рецепты, опубликованные пользователем
и возможность подписаться на пользователя.

## Техническое описание проекта

К проекту по адресу  http://51.250.96.184/api/docs/  подключена документация **Foodgram**.
В ней описаны возможные запросы к API и структура ожидаемых ответов.
Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.

## Технологии:
* Python 3.7
* Django 3.1.14
* Docker
* Nginx
* Github Action

## Описание Workflow

Workflow состоит из четырёх шагов:
1. Проверка кода на соответствие PEP8 и запуск тестов проекта;
2. Сборка и публикация образа на DockerHub;
3. Автоматический деплой на удаленный сервер;
4. Отправка telegram-ботом уведомления в чат.

## Установка:
1. Клонируйте репозиторий на локальную машину.
   ```https://github.com/Spookyviking/foodgram-project-react.git```
2. Установите виртуальное окружение в папке проекта.
```
cd foodgram-project-react
python -m venv venv
```
3. Активируйте виртуальное окружение.
   ```source venv\Scripts\activate```
4. Установите зависимости.
```
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
```
- В папке с файлом manage.py выполнить команды:

```bash
python manage.py makemigrations users
python manage.py makemigrations recipes
python manage.py migrate
```
- Создать пользователя с неограниченными правами:

```bash
python manage.py createsuperuser
```
## Запуск проекта в контейнерах
При запуске создаются три контейнера:

 - контейнер базы данных **db**
 - контейнер приложения **backend**
 - контейнер web-сервера **nginx**
 
1. Перейдите в директорию `infra/`, заполните файл .env.template и после этого переименуйте его в .env
2. Выполните команду:
   ```docker-compose up -d --build```
3. Для остановки контейнеров из директории `infra/` выполните команду:
   ```docker-compose down -v```
4. Загрузка данных для примера из папки `infra/`
   ```docker-compose exec backend python manage.py loaddata dump.json```

## Deploy проекта на удаленный сервер
Предварительно для автоматического деплоя необходимо подготовить сервер:
1. Установить docker: ```sudo apt install docker.io```
2. Установите docker-compose:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
3. Скопируйте файлы docker-compose.yaml и nginx/default.conf из проекта на сервер в
home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно.
4. В Secrets GitHub Actions форкнутого репозитория добавить переменные окружения:
   * SSH_KEY - ssh private key для доступа к удаленному серверу
   * HOST - public id хоста
   * USER - имя user-а на удаленном сервере
   * PASSPHRASE - пароль подтверждения подключения по ssh-key
   * DOCKER_USERNAME - username на DockerHub
   * DOCKER_PASSWORD - пароль на DockerHub
   * POSTGRES_USER - имя пользователя для базы данных
   * POSTGRES_PASSWORD - пароль для подключения к базе
   * DB_ENGINE - настойка подключения django-проекта к postgresql
   * DB_NAME - имя базы данных
   * DB_HOST - название сервиса (контейнера)
   * DB_PORT - порт для подключения к БД
   * TELEGRAM_TOKEN - token telegram-бота
   * TELEGRAM_TO - id пользователя, которому будут приходить оповещения об успешном деплое
   * DJANGO_SU_ADMIN - имя создаваемого суперюзера в django-проекте
   * DJANGO_SU_EMAIL - эл. почта создаваемого суперюзера в django-проекте
   * DJANGO_SU_PASSWORD - пароль создаваемого суперюзера в django-проекте
   * LANGUAGE_CODE - язык проекта
   * TIME_ZONE - зона времени проекта


- Выполнить миграции и подключить статику

```bash
docker-compose exec python manage.py makemigrations users
docker-compose exec python manage.py makemigrations recipes
docker-compose exec python manage.py makemigrations core
docker-compose exec python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
```
- Подключиться внутрь окнтейнера можно с помощью команды:
```
docker exec -it <mycontainer> bash
```
## Как импортировать данные из своего csv файла?
Для начала убедитесь, что первая строчка вашего csv файла совпадает с названиями полей в модели. Если на первой строчке нет названия полей или они неправильные, исправьте, прежде чем приступать к импортированию.

### Импортирование с помощью скрипта
1. Заходим в shell:
```bash
docker-compose exec backend python manage.py shell
```
2. Импортируем нужные модели:
```python
from recipes.models import Ingredient, Tag
```
3. Импортируем скрипт:
```python
from scripts.import_data import create_models
```

4. Запускаем скрипт с тремя параметрами:

`file_path` — путь до вашего csv файла,

`model` — класс модели из импортированных ранее,

`print_errors` — нужно ли распечатать каждую ошибку подробно? (```True or False```)

Пример:
```python
create_models('../data/ingredients.csv', Ingredient, True)
```

## Ссылка на проект
Проект развернут по адресу http://51.250.96.184

Админка:
```
spookyviking
test@test.test
qwerty_1234
```

## Автор:
[Максим Остапенко](https://github.com/Spookyviking)
