"""URLs from workatolist project."""

from django.conf.urls import url, include
from django.views.generic import RedirectView
from rest_framework_swagger.views import get_swagger_view
from channels import urls as channels_url

schema_view = get_swagger_view(title='WAO API')

urlpatterns = [
    url(r'^api/v1/', include(channels_url, namespace='api')),
    url(r'^api-docs/', schema_view),
    url(r'^', RedirectView.as_view(url='/api-docs/'))
]
