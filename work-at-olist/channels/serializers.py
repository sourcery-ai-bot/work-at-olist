"""Serializers of the Channels' models."""

from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
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
        fields = ('url', 'name', 'channel', 'parent', 'children')
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
            },
            'children': {
                'view_name': 'api:category-detail',
                'lookup_field': 'reference'
            }
        }


class ParentCategorySerializer(serializers.HyperlinkedModelSerializer):
    """Parent Category Serializer used in the '/categories/relatives' endpoint.
    """
    parent = RecursiveField(allow_null=True)

    class Meta:
        model = Category
        fields = ('url', 'name', 'parent')
        extra_kwargs = {
            'url': {
                'view_name': 'api:category-detail',
                'lookup_field': 'reference'
            }
        }


class ChildrenCategorySerializer(serializers.HyperlinkedModelSerializer):
    """Children Category Serializer used in the '/categories/relatives'
    endpoint."""
    children = RecursiveField(required=False, allow_null=True, many=True)

    class Meta:
        model = Category
        fields = ('url', 'name', 'children')
        extra_kwargs = {
            'url': {
                'view_name': 'api:category-detail',
                'lookup_field': 'reference'
            }
        }


class CategoryRelativesSerializer(serializers.HyperlinkedModelSerializer):
    """Category Serializer used in the '/categories/relatives' endpoint. It
    uses Hyperlinked relation for the related Channel and nests parents and children
    Categories."""
    parent = ParentCategorySerializer()
    children = ChildrenCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('url', 'name', 'channel', 'parent', 'children')
        extra_kwargs = {
            'url': {
                'view_name': 'api:category-detail',
                'lookup_field': 'reference'
            },
            'channel': {
                'view_name': 'api:channel-detail',
                'lookup_field': 'reference'
            }
        }
