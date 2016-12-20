"""Serializers' test cases."""

from django.test import TestCase
from channels import models, serializers


class ChannelSerializerTest(TestCase):
    """ChannelSerializer's Test Cases."""

    fixtures = ['serializerstests']

    def test_create(self):
        """Tests ChannelSerializer's creation."""
        expected_data = {'url': '/api/v1/channels/test/', 'name': 'Test'}

        model = models.Channel.objects.get(reference='test')
        serializer = serializers.ChannelSerializer(
            model, context={'request': None})

        self.assertEqual(serializer.data, expected_data)

    def test_validate(self):
        """Tests ChannelSerializer's validation."""
        data = {'name': 'Channel'}

        serializer = serializers.ChannelSerializer(
            data=data)

        self.assertTrue(serializer.is_valid())


class CategorySerializerTest(TestCase):
    """CategorySerializer's Test Cases."""

    fixtures = ['serializerstests']

    def test_create(self):
        """Tests CategorySerializer's creation."""
        expected_data = {
            'url': '/api/v1/categories/test-root-one-two/',
            'name': 'Two',
            'channel': '/api/v1/channels/test/',
            'parent': '/api/v1/categories/test-root-one/',
            'children': []
        }

        category = models.Category.objects.get(reference='test-root-one-two')
        serializer = serializers.CategorySerializer(
            category, context={'request': None})

        self.assertEqual(serializer.data, expected_data)

    def test_validate(self):
        """Tests CategorySerializer's validation."""
        data = {
            'name': 'Category',
            'channel': '/api/v1/channels/test/',
            'parent': '/api/v1/categories/test-root/',
            'children': []
        }

        serializer = serializers.CategorySerializer(
            data=data)

        self.assertTrue(serializer.is_valid())


class ParentCategorySerializer(TestCase):
    """ParentCategorySerializer's Test Cases."""

    fixtures = ['serializerstests']

    def test_create(self):
        """Tests ParentCategorySerializer's creation."""
        expected_data = {
            'url': '/api/v1/categories/test-root-one-two/',
            'name': 'Two',
            'parent': {
                'url': '/api/v1/categories/test-root-one/',
                'name': 'One',
                'parent': {
                    'url': '/api/v1/categories/test-root/',
                    'name': 'Root',
                    'parent': None
                }
            }
        }

        category = models.Category.objects.get(reference='test-root-one-two')

        serializer = serializers.ParentCategorySerializer(
            category, context={'request': None})

        self.assertEqual(serializer.data, expected_data)

    def test_validate(self):
        """Tests ParentCategorySerializer's validation."""
        data = {
            'name': 'Category',
            'parent': {
                'name': 'Category',
                'parent': None
            }
        }

        serializer = serializers.ParentCategorySerializer(
            data=data)

        self.assertTrue(serializer.is_valid())


class ChildrenCategorySerializer(TestCase):
    """ChildrenCategorySerializer's Test Cases."""

    fixtures = ['serializerstests']

    def test_create(self):
        """Tests ChildrenCategorySerializer's creation."""
        expected_data = {
            'url': '/api/v1/categories/test-root/',
            'name': 'Root',
            'children': [{
                'url': '/api/v1/categories/test-root-one/',
                'name': 'One',
                'children': [{
                    'url': '/api/v1/categories/test-root-one-two/',
                    'name': 'Two',
                    'children': []
                }, {
                    'url': '/api/v1/categories/test-root-one-two-two/',
                    'name': 'Two Two',
                    'children': []
                }]
            }]
        }

        category = models.Category.objects.get(reference='test-root')

        serializer = serializers.ChildrenCategorySerializer(
            category, context={'request': None})

        self.assertEqual(serializer.data, expected_data)

    def test_validate(self):
        """Tests ChildrenCategorySerializer's validation."""
        data = {
            'name': 'Category',
            'children': [{
                'name': 'One',
                'children': []
            }, {
                'name': 'Two',
                'children': []
            }]
        }

        serializer = serializers.ChildrenCategorySerializer(
            data=data)

        self.assertTrue(serializer.is_valid())


class CategoryRelativesSerializer(TestCase):
    """CategoryRelativesSerializer's Test Cases."""

    fixtures = ['serializerstests']

    def test_create(self):
        """Tests CategoryRelativesSerializer's creation."""
        expected_data = {
            'url': '/api/v1/categories/test-root-one/',
            'name': 'One',
            'channel': '/api/v1/channels/test/',
            'parent': {
                'url': '/api/v1/categories/test-root/',
                'name': 'Root',
                'parent': None
            },
            'children': [{
                'url': '/api/v1/categories/test-root-one-two/',
                'name': 'Two',
                'children': []
            }, {
                'url': '/api/v1/categories/test-root-one-two-two/',
                'name': 'Two Two',
                'children': []
            }]
        }

        category = models.Category.objects.get(reference='test-root-one')

        serializer = serializers.CategoryRelativesSerializer(
            category, context={'request': None})

        self.assertEqual(serializer.data, expected_data)

    def test_validate(self):
        """Tests CategoryRelativesSerializer's validation."""
        data = {
            'name': 'Category',
            'channel': '/api/v1/channels/test/',
            'parent': {
                'name': 'Category',
                'parent': None
            },
            'children': [{
                'name': 'One',
                'children': []
            }, {
                'name': 'Two',
                'children': []
            }]
        }

        serializer = serializers.CategoryRelativesSerializer(
            data=data)

        self.assertTrue(serializer.is_valid())
