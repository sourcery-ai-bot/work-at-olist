"""Serializers of the Channels' models."""

from rest_framework import serializers
from channels.models import Channel, Category


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    """Channel Serializer. It uses Hyperlinked reference."""

    class Meta:
        model = Channel
        fields = ('url', 'name')
        extra_kwargs = {
            'url': {
                'view_name': 'api:channel-detail',
                'lookup_field': 'reference'
            }
        }


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """Category Serializer. It uses Hyperlinked reference and relations."""

    class Meta:
        model = Category
        fields = ('url', 'name', 'channel', 'parent')
        extra_kwargs = {
            'url': {
                'view_name': 'api:category-detail',
                'lookup_field': 'reference'
            },
            'channel': {
                'view_name': 'api:channel-detail',
                'lookup_field': 'reference'
            },
            'parent': {
                'view_name': 'api:category-detail',
                'lookup_field': 'reference'
            }
        }
