"""Models' test cases of the Channels app."""

from django.test import TestCase
from channels.models import Channel, Category


def create_channel(reference, name):
    """Create a Channel."""
    return Channel.objects.create(reference=reference, name=name)


def create_category(reference, name, channel, parent=None):
    """Create a Category."""
    return Category.objects.create(
        reference=reference, name=name, channel=channel, parent=parent)


class ChannelTest(TestCase):
    """Channel's Test Cases."""

    def test_channel_str(self):
        """Tests Channel's string representation."""
        channel = create_channel('test_channel', 'Test Channel')
        self.assertEqual(channel.__str__(), channel.reference)


class CategoryTest(TestCase):
    """Category's Test Cases."""

    def test_category_str(self):
        """Tests Category's string representation."""
        channel = create_channel('test_channel', 'Test Channel')
        category = create_category('test_category', 'Test Category', channel)
        self.assertEqual(category.__str__(), category.reference)
