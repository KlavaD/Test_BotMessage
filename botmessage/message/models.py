from django.db import models

# from bot import wake_up, get_news, get_weather, help
from botmessage import settings
from message.validators import command_validator

COMMAND_TO_FUNCTION = (
    ('wake_up', 'команда для старта'),
    ('help', 'команда для вызова помощи'),
    ('get_news', 'команда для новостей'),
    ('get_weather', 'команда для погоды'),
)


class BotCommand(models.Model):
    command = models.TextField(
        help_text='Команда может быть только латинскими буквами',
        max_length=settings.FIELD_TEXT_LENGTH,
        verbose_name='Команда бота',
        unique=True,
        validators=[command_validator]
    )
    function = models.TextField(
        max_length=settings.FIELD_TEXT_LENGTH,
        verbose_name='Описание действий бота',
        choices=COMMAND_TO_FUNCTION,
        unique=True
    )
    message = models.TextField(
        verbose_name='Сообщение, которое отправляется пользователю',
    )

    def __str__(self):
        return self.command

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        ordering = ('command',)


class HistoryOfMessage(models.Model):
    telegram_user = models.CharField(
        max_length=settings.FIELD_TEXT_LENGTH,
        blank=False,
        null=False,
        verbose_name='Пользователь телеграмм'
    )
    message = models.TextField(
        verbose_name='Сообщение'
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата отправления',
        auto_now_add=True
    )

    def __str__(self):
        return self.message[:50]

    class Meta:
        verbose_name = 'История сообщений'
        verbose_name_plural = 'История сообщений'
        ordering = ('-pub_date',)
