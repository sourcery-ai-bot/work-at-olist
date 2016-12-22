"""Views of the Channels app."""

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from channels import models, serializers


class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    """Channel's API ViewSet with list and detail endpoints."""

    queryset = models.Channel.objects.all()
    serializer_class = serializers.ChannelSerializer
    lookup_field = 'reference'
    search_fields = ('reference', 'name')
    ordering_fields = ('reference', 'name')
    ordering = ('reference', )


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Category's API ViewSet with list and detail endpoints."""

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'reference'
    search_fields = ('reference', 'name', 'channel__reference',
                     'channel__name')
    ordering_fields = ('reference', 'name', 'channel__reference',
                       'channel__name')
    ordering = ('channel__reference', 'reference')

    def get_queryset(self):
        """Retrieves the queryset using the 'channel_pk' if present."""
        if 'channels_reference' in self.kwargs:
            return self.queryset.filter(
                channel__reference=self.kwargs['channels_reference'])
        return self.queryset

    @detail_route(methods=['get'])
    def relatives(self, request, reference, channels_reference=None):
        """Endpoint that retrieves a category with its ancestors and chidren."""
        category = self.get_object()
        serializer = serializers.CategoryRelativesSerializer(
            category, context={'request': request})
        return Response(serializer.data)
