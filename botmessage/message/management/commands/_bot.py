import logging
import os
import re
from http import HTTPStatus
from logging.handlers import RotatingFileHandler
from random import randint

import requests
import telegram
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from requests import RequestException
from telegram import ReplyKeyboardMarkup

from botmessage import settings
from exceptions import UrlNotAvailable
from message.models import BotCommand, HistoryOfMessage

load_dotenv()

BASE_DIR = settings.BASE_DIR

WEATHER_URL = settings.WEATHER_URL
NEWS_URL = settings.NEWS_URL

NEWS_KEY = os.getenv('NEWS_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHER_KEY = os.getenv('WEATHER_KEY')

LOGGING_FINISH = 'Бот завершил работу.'

LOGGING_CONNECTION_ERROR = (
    'Возникла ошибка при загрузке страницы {url}{error}'
)
ERROR_TOKEN = 'Нет токена {token}'
PATTERN = r'/(?P<command>\w+)'


def configure_logging():
    rotating_handler = RotatingFileHandler(
        settings.LOG_FILE,
        encoding='utf-8',
        maxBytes=10 ** 6,
        backupCount=5
    )
    logging.basicConfig(
        datefmt=settings.DT_FORMAT,
        format=settings.LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )


def send_message(bot, message, update, reply_markup=None):
    """Отправляет сообщение в Telegram чат."""
    try:
        logging.info(f'начали отправку сообщения "{message}" в Telegram')
        bot.send_message(
            update.effective_chat.id,
            message,
            reply_markup=reply_markup)
        logging.info(f'отправлено сообщение "{message}"')
        HistoryOfMessage.objects.create(
            user=update.effective_user.name,
            message=message
        )
        logging.info('Сообщение записано в БД')
        return True
    except telegram.error.TelegramError(
            'При отправке сообщения произошла ошибка') as error:
        logging.error(error)
        return False


def get_api_answer(url, params):
    """Функция для получения ответа от url с параметрами params"""
    logging.info(
        'Начали запрос к API {url}'.format(url=url))
    try:
        response = requests.get(url, params)
    except RequestException as error:
        raise ConnectionError(
            LOGGING_CONNECTION_ERROR.format(
                error=error,
                url=url
            )
        )
    if response.status_code == HTTPStatus.NOT_FOUND:
        raise UrlNotAvailable('Упс, похоже такого города нет')
    return response


def get_message(update):
    return (get_object_or_404(
        BotCommand,
        command=re.search(PATTERN, update.message.text).group('command'),
    ).message)


def get_weather(update, context):
    """Функция запроса города"""
    send_message(
        context.bot,
        '{}'.format(update.message.chat.first_name + ' ' + get_message(update)),
        update)


def get_weather_in(update, context):
    """Функция для получения погоды в определенном городе"""
    message = update.message.text
    params = {
        'APPID': WEATHER_KEY,
        'q': message,
        'units': 'metric'
    }
    try:
        response = get_api_answer(WEATHER_URL, params)
        text = (
            'Сейчас температура воздуха в городе {city} составляет '
            '{temp} градусов'.format(
                temp=response.json()['main']['temp'],
                city=message,
            )
        )
    except UrlNotAvailable as error:
        logging.error('Возникла ошибка {error}'.format(error=error))
        text = '{error} {city}, Попробуйте ввести другой город'.format(
            error=error,
            city=message
        )
    send_message(context.bot, text, update)


def get_news(update, context):
    """Функция для получения
     1 рандомной новости из NEWS_COUNT последних на сайте tass.ru"""
    params = {
        'domains': 'tass.ru',
        'language': 'ru',
        'sortBy': 'publishedAt',
        'pageSize': settings.NEWS_COUNT,
        'apiKey': NEWS_KEY,
    }
    response = get_api_answer(NEWS_URL, params)
    command_message = get_message(update)
    text = (
            command_message + '{}'.format(
        response.json()['articles'][randint(0, settings.NEWS_COUNT - 1)]['url']
    )
    )
    send_message(context.bot, text, update)


def wake_up(update, context):
    commands = BotCommand.objects.all()
    name_buttons = []
    for command in commands:
        name_buttons.append('/' + command.command)
    button = ReplyKeyboardMarkup([name_buttons],
                                 resize_keyboard=True)
    send_message(
        context.bot,
        '{}'.format(update.effective_user.name) + ' ' + get_message(update),
        update,
        reply_markup=button
    )


def help(update, context):
    # Отправляем пользователю информацию о том, как пользоваться ботом.
    send_message(context.bot, get_message(update), update)


def check_tokens():
    """Проверяет доступность переменных окружения."""
    tokens = (
        ('news', NEWS_KEY),
        ('weather', WEATHER_KEY),
        ('bot', BOT_TOKEN),
    )
    flag = True
    for token_name, token in tokens:
        if not token:
            flag = False
            logging.critical(ERROR_TOKEN.format(token=token_name))
    return flag
