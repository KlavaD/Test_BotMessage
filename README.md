# Telegram-бот + Django веб-сервис

Автор - 
*   [Клавдия Дунаева](https://www.t.me/klodunaeva)
**Бот обрабатывает следующие команды:**

* /start - бот приветствует пользователя и рассказывает о своих функциях.
* /help - бот выводит список доступных команд.
* /weather - бот показывает текущую погоду в указанном городе.
* /news - бот отправляет пользователю случайную новость с сайта [tass.ru](https://tass.ru/).

**Django веб-сервис**

Взаимодействует с ранее разработанным Telegram-ботом и предоставляет следующие функциональные возможности:

* Просмотр истории сообщений
* Редактирование сообщений бота через веб-сервис. 
* Администраторы должны иметь возможность изменить текст сообщения и/или команду, которая вызывает определенную реакцию у бота.
* Аутентификация и авторизация пользователей. Администраторы имеют доступ к редактированию сообщений , а обычные пользователи смогут только просматривать историю сообщений.

* **Инструменты и стек:**

Python3.7+,
[Django3.2+](https://www.djangoproject.com/),
[DRF](https://www.django-rest-framework.org/),
[Telegram](https://github.com/python-telegram-bot/python-telegram-bot),


**Как запустить проект:**

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/KlavaD/Test_BotMessage
```

### Вариант 1 (с Docker)

* Перейти в папку infra

* Создать файл .env

DB_ENGINE=django.db.backends.postgresql\
DB_NAME=postgres\
POSTGRES_USER=postgres\
POSTGRES_PASSWORD=postgres\
DB_HOST=db\
DB_PORT=5432\
BOT_TOKEN - Токен вашего бота\
WEATHER_KEY - Токен для получения погоды с сайта\
[openweathermap](https://openweathermap.org/api)\
NEWS_KEY - Токен для получения новостей\
[newsapi](https://newsapi.org/)\

* Запустить docker-compose

```
docker-compose up -d --build
```
* Выполнить команды:

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
* Загрузить первичные данные

```
docker-compose exec web python manage.py adddata
```
* Запустить Бота:

```
docker-compose exec web python manage.py bot
```

### Вариант 2

* Создать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

```
source env/bin/activate
```

* Если у вас windows

```
venv\Scripts\activate
```

* Обновить pip:

```
python3 -m pip install --upgrade pip
```

* Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

* Создать в папке botmessage файл .env с переменными окружения:

BOT_TOKEN - Токен вашего бота\
WEATHER_KEY - Токен для получения погоды с сайта\
[openweathermap](https://openweathermap.org/api)\
NEWS_KEY - Токен для получения новостей\
[newsapi](https://newsapi.org/)\

* Выполнить миграции:

```
python3 manage.py migrate
```

* Запустить проект:

```
python3 manage.py runserver
```
* Заполнить начальные данные:

```
python manage.py adddata
```
* Запустить Бота:

```
python manage.py bot
```

## Примеры запросов: ##

*Через docker эндпоинты без* :8000

Посмотреть документацию:
>**GET** http://127.0.0.1:8000/api/schema/redoc/

Регистрация нового пользователя:
>**POST** http://127.0.0.1:8000/api/users/

Получение токена для пользователя (вход):
>**POST** http://127.0.0.1:8000/api/auth/token/login/

Получить список команд:
>**GET** http://127.0.0.1:8000/api/commands/

Изменить команду:
>**PATCH** http://127.0.0.1:8000/api/commands/{id}/

Изменить команду:
>**PATCH** http://127.0.0.1:8000/api/commands/{id}/

Посмотреть историю сообщений:
>**GET** http://127.0.0.1:8000/api/history/
