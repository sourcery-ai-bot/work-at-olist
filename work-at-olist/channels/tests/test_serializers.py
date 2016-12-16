"""Serializers' test cases."""

from django.test import TestCase
from channels.models import Channel, Category
from channels.serializers import ChannelSerializer, CategorySerializer


class ChannelSerializerTest(TestCase):
    """ChannelSerializer's Test Cases."""

    def test_empty(self):
        """Tests creation of a empty ChannelSerializer."""
        expected_data = {'name': ''}

        serializer = ChannelSerializer()

        self.assertEqual(serializer.data, expected_data)

    def test_create(self):
        """Tests ChannelSerializer's creation."""
        expected_data = {'url': '/api/channels/test/', 'name': 'Test'}

        model = Channel(reference='test', name='Test')
        serializer = ChannelSerializer(model, context={'request': None})

        self.assertEqual(serializer.data, expected_data)


class CategorySerializerTest(TestCase):
    """CategorySerializer's Test Cases."""

    def test_empty(self):
        """Tests creation of a empty CategorySerializer."""
        expected_data = {'name': '', 'channel': None, 'parent': None}

        serializer = CategorySerializer()

        self.assertEqual(serializer.data, expected_data)

    def test_create(self):
        """Tests CategorySerializer's creation."""
        expected_data = {
            'url': '/api/categories/test/',
            'name': 'Test',
            'channel': '/api/channels/channel/',
            'parent': None
        }

        channel = Channel(reference='channel', name='Channel')
        category = Category(reference='test', name='Test', channel=channel)
        serializer = CategorySerializer(category, context={'request': None})

        self.assertEqual(serializer.data, expected_data)
