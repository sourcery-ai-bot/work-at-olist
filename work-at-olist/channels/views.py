"""Views of the Channels app."""

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from channels.models import Channel, Category
from channels.serializers import ChannelSerializer, CategorySerializer


class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    """Channel's API ViewSet with list and detail endpoints."""

    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    lookup_field = 'reference'

    @detail_route(methods=['get'])
    def categories(self, request, reference):
        """Endpoint that lists all categories of a Channel."""
        channel = self.get_object()
        serializer = CategorySerializer(
            channel.categories.all(), context={'request': request}, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Category's API ViewSet with list and detail endpoints."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'reference'
