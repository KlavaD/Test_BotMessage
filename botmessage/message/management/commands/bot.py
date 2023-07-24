import logging
import os

from django.core.management.base import BaseCommand
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters

from message.management.commands._bot import (
    configure_logging,
    check_tokens,
    get_weather_in,
    get_weather,
    get_news,
    wake_up,
    help,
)
from message.models import BotCommand

LOGGING_START = 'Бот запущен запущен!'
BOT_TOKEN = os.getenv('BOT_TOKEN')
LOGGING_ERROR = 'Сбой в работе программы {error}'
COMMAND_TO_FUNCTION = {
    'wake_up': wake_up,
    'help': help,
    'get_news': get_news,
    'get_weather': get_weather,
}

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        configure_logging()
        logging.info(LOGGING_START)
        if not check_tokens():
            raise KeyError()
        updater = Updater(token=BOT_TOKEN)
        commands = BotCommand.objects.all()
        for command in commands:
            updater.dispatcher.add_handler(
                CommandHandler(
                    command.command,
                    COMMAND_TO_FUNCTION[command.function]
                )
            )
        updater.dispatcher.add_handler(
            MessageHandler(Filters.text, get_weather_in))

        try:
            updater.start_polling()
            self.stdout.write(self.style.SUCCESS('Бот запущен'))
        except Exception as error:
            logging.exception(
                LOGGING_ERROR.format(error=error)
            )
        updater.idle()
        self.stdout.write(self.style.SUCCESS('Бот остановлен'))

