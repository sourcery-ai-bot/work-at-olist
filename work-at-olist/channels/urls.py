"""URLs from Channels app."""

from rest_framework import routers
from channels.views import ChannelViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'channels', ChannelViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = router.urls
