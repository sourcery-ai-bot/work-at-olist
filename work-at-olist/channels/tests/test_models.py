"""Models' test cases of the Channels app."""

from django.test import TestCase
from channels.models import BaseModel, Channel, Category


def create_channel(reference, name):
    """Create a Channel."""
    return Channel.objects.create(reference=reference, name=name)


def create_category(reference, name, channel, parent=None):
    """Create a Category."""
    return Category.objects.create(
        reference=reference, name=name, channel=channel, parent=parent)


class BaseModelTest(TestCase):
    """BaseModel's Test Cases."""

    def test_generate_reference(self):
        """Tests BaseModel's reference genaration method."""
        test_data = [{
            'name': 'test',
            'prefixes': None,
            'output': 'test'
        }, {
            'name': 'test',
            'prefixes': [],
            'output': 'test'
        }, {
            'name': 'Test',
            'prefixes': None,
            'output': 'test'
        }, {
            'name': 'test-test',
            'prefixes': None,
            'output': 'test-test'
        }, {
            'name': 'MyTest',
            'prefixes': ['Level1'],
            'output': 'level1-mytest'
        }, {
            'name': 'MyTest',
            'prefixes': ['Level1', 'Level2', 'Level-3'],
            'output': 'level1-level2-level-3-mytest'
        }]

        for item in test_data:
            reference = BaseModel.generate_reference(item['name'],
                                                     item['prefixes'])
            self.assertEqual(reference, item['output'])


class ChannelTest(TestCase):
    """Channel's Test Cases."""

    def test_str(self):
        """Tests Channel's string representation."""
        channel = create_channel('test_channel', 'Test Channel')
        self.assertEqual(channel.__str__(), channel.reference)


class CategoryTest(TestCase):
    """Category's Test Cases."""

    def test_str(self):
        """Tests Category's string representation."""
        channel = create_channel('test_channel', 'Test Channel')
        category = create_category('test_category', 'Test Category', channel)
        self.assertEqual(category.__str__(), category.reference)
