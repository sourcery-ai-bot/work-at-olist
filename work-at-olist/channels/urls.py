"""URLs from Channels app."""

from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from channels.views import ChannelViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'channels', ChannelViewSet)
router.register(r'categories', CategoryViewSet)

channel_router = nested_routers.NestedSimpleRouter(
    router, r'channels', lookup='channels')
channel_router.register(r'categories', CategoryViewSet)

urlpatterns = [
    url(r'', include(router.urls)), url(r'', include(channel_router.urls))
]
