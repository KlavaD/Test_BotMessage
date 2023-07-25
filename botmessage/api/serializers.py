from rest_framework import serializers

from message.models import BotCommand, HistoryOfMessage


class CommandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotCommand
        fields = ('id', 'command', 'function', 'message')


class HistoryMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryOfMessage
        fields = ('id', 'telegram_user', 'message')
