from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.filters import HistoryMessageFilter
from api.permissions import IsAdminOrReadOnly
from api.serializers import CommandsSerializer, HistoryMessageSerializer
from message.models import BotCommand, HistoryOfMessage


class CommandsViewSet(viewsets.ModelViewSet):
    queryset = BotCommand.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    ordering_fields = ['command']
    serializer_class = CommandsSerializer


class HistoryMessageViewSet(viewsets.ModelViewSet):
    queryset = HistoryOfMessage.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter)
    filterset_class = HistoryMessageFilter
    ordering_fields = ['-pub_date']
    serializer_class = HistoryMessageSerializer
