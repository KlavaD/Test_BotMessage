from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAdminOrReadOnly


class UpdateListViewSet(mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
