import logging
import os
from http import HTTPStatus
from random import randint

import requests
import telegram
from dotenv import load_dotenv
from requests import RequestException
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters

from configs import configure_logging
from exceptions import UrlNotAvailable
from message.models import BotCommand

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'
NEWS_URL = 'https://newsapi.org/v2/everything?'
NEWS_KEY = os.getenv('NEWS_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')
NEWS_COUNT = 10
WEATHER_KEY = os.getenv('WEATHER_KEY')
LOGGING_START = 'Бот запущен запущен!'
LOGGING_FINISH = 'Бот завершил работу.'
LOGGING_ERROR = 'Сбой в работе программы {error}'
LOGGING_CONNECTION_ERROR = (
    'Возникла ошибка при загрузке страницы {url}{error}'
)
ERROR_TOKEN = 'Нет токена {token}'


def send_message(bot, message, chat_id, reply_markup=None):
    """Отправляет сообщение в Telegram чат."""
    try:
        logging.info(f'начали отправку сообщения "{message}" в Telegram')
        bot.send_message(chat_id, message, reply_markup=reply_markup)
        logging.info(f'отправлено сообщение "{message}"')
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


def get_weather(update, context, command_message):
    """Функция запроса города"""
    send_message(
        context.bot,
        '{}' + command_message.format(update.message.chat.first_name),
        update.effective_chat.id)


def get_weather_in(update, context):
    """Функция для получения погоды в определенном городе"""
    message = update.message
    params = {
        'APPID': WEATHER_KEY,
        'q': message.text,
        'units': 'metric'
    }
    try:
        response = get_api_answer(WEATHER_URL, params)
        text = (
            'Сейчас температура воздуха в городе {city} составляет '
            '{temp} градусов'.format(
                temp=response.json()['main']['temp'],
                city=message.text,
            )
        )
    except UrlNotAvailable as error:
        logging.error('Возникла ошибка {error}'.format(error=error))
        text = '{error} {city}, Попробуйте ввести другой город'.format(
            error=error,
            city=message.text
        )
    send_message(context.bot, text, update.effective_chat.id)


def get_news(update, context, command_message):
    """Функция для получения
     1 рандомной новости из NEWS_COUNT последних на сайте tass.ru"""
    params = {
        'domains': 'tass.ru',
        'language': 'ru',
        'sortBy': 'publishedAt',
        'pageSize': NEWS_COUNT,
        'apiKey': NEWS_KEY,
    }
    response = get_api_answer(NEWS_URL, params)
    text = (
            command_message + '{}'.format(
        response.json()['articles'][randint(0, NEWS_COUNT - 1)]['url']
    )
    )
    send_message(context.bot, text, update.effective_chat.id)


def wake_up(update, context, command_message):
    commands = BotCommand.objects.all()
    name_buttons = []
    for command in commands:
        name_buttons.append('\\' + command.command)
    button = ReplyKeyboardMarkup([name_buttons],
                                 resize_keyboard=True)
    send_message(
        context.bot,
        '{}' + command_message.format(update.message.chat.first_name),
        update.effective_chat.id,
        reply_markup=button
    )


def help(update, context, command_message):
    # Отправляем пользователю информацию о том, как пользоваться ботом.
    #     help_text = """
    # Вот список команд, которые можно использовать:
    #
    # Команды:
    # /start - начать диалог со мной
    # /help - получить справку
    # /weather - Температура сейчас в городе ...
    # /news - Прочитать новость
    #     """
    send_message(context.bot, command_message, update.effective_chat.id)


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


def main():
    configure_logging()
    logging.info(LOGGING_START)
    if not check_tokens():
        raise KeyError()
    updater = Updater(token=BOT_TOKEN)
    commands = BotCommand.objects.all()
    for command in commands:
        print(command.command,
              command.function(command.message))
        updater.dispatcher.add_handler(
            CommandHandler(
                command.command,
                command.function(command.message)
            )
        )
    # updater.dispatcher.add_handler(CommandHandler('help', help))
    # updater.dispatcher.add_handler(CommandHandler('weather', get_weather))
    # updater.dispatcher.add_handler(CommandHandler('news', get_news))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, get_weather_in))

    # try:
    #     updater.start_polling()
    # except Exception as error:
    #     logging.exception(
    #         LOGGING_ERROR.format(error=error)
    #     )
    # updater.idle()


if __name__ == '__main__':
    main()
