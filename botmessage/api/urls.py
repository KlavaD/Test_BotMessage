from django.urls import include, path
from rest_framework import routers

from api.views import CommandsViewSet, HistoryMessageViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'history', HistoryMessageViewSet, basename='history')
router_v1.register(r'commands', CommandsViewSet, basename='commands')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls)),
]
