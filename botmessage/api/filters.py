import django_filters

from message.models import HistoryOfMessage


class HistoryMessageFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='telegram_user')

    class Meta:
        model = HistoryOfMessage
        fields = ('telegram_user',)
