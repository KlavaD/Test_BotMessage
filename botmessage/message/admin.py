from django.contrib import admin

from message.models import BotCommand, HistoryOfMessage


@admin.register(BotCommand)
class BotCommandAdmin(admin.ModelAdmin):
    list_display = ('pk', 'command', 'message')
    search_fields = ('name',)
    list_filter = ('command', 'message')
    empty_value_display = '-пусто-'


@admin.register(HistoryOfMessage)
class HistoryOfMessageAdmin(admin.ModelAdmin):
    list_display = ('telegram_user', 'message', 'pub_date')
    search_fields = ('telegram_user',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
