from django.contrib import admin
from django.utils.safestring import mark_safe

from message.models import BotCommand, HistoryOfMessage


@admin.register(BotCommand)
class BotCommandAdmin(admin.ModelAdmin):
    list_display = ('pk', 'command', 'message')
    search_fields = ('name',)
    list_filter = ('command', 'message')
    empty_value_display = '-пусто-'


@admin.register(HistoryOfMessage)
class HistoryOfMessageAdmin(admin.ModelAdmin):
    @admin.display(description='Картинка')
    def take_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src={obj.image.url} width="80" height="60">'
            )
        return None

    list_display = ('telegram_user', 'message', 'take_image', 'pub_date',)
    search_fields = ('telegram_user',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
