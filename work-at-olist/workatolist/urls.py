"""URLs from workatolist project."""

from django.conf.urls import url, include
from channels import urls as channels_url

urlpatterns = [url(r'^api/v1/', include(channels_url, namespace='api'))]
