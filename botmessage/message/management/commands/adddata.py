from django.core.management.base import BaseCommand, CommandError

from message.models import BotCommand

commands = (
    (
        'start', 'wake_up',
        ('Привет. Я-бот! И я могу отправить тебе отправить '
         'погоду в нужном городе или рассказать случайную новость.')
    ),
    ('help', 'help',
     """
     Вот список команд, которые можно использовать:

Команды:
/start - начать диалог со мной
/help - получить справку
/weather - Температура сейчас в городе ...
/news - Прочитать новость"""
     ),
    ('weather', 'get_weather',
     'В каком городе вы хотите узнать погоду?'),
    ('news', 'get_news',
     'Новости: '),
)
result = []


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        global result, commands
        try:
            for command, function, message in commands:
                data, status = BotCommand.objects.get_or_create(
                    command=command,
                    function=function,
                    message=message
                )
            print('Команды созданы!')
        except Exception as error:
            raise CommandError(f'Сбой при импорте: {error}')

        self.stdout.write(
            self.style.SUCCESS('Первичное наполнение БД прошло успешно')
        )
