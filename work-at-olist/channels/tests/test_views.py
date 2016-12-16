"""Views' test cases."""

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class ChannelViewSetTest(TestCase):
    """ChannelViewSet's Test Cases."""

    fixtures = ['viewtests']

    def test_list(self):
        """Tests '/api/channels/' endpoint."""
        client = APIClient()

        response = client.get('/api/channels/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve(self):
        """Tests '/api/channels/{reference}' endpoint."""
        client = APIClient()

        response = client.get('/api/channels/walmart/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'walmart')


class CategoryViewSetTest(TestCase):
    """CategoryViewSet's Test Cases."""

    fixtures = ['viewtests']

    def test_list(self):
        """Tests '/api/categories/' endpoint."""
        client = APIClient()

        response = client.get('/api/categories/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 24)

    def test_retrieve(self):
        """Tests '/api/categories/{reference}' endpoint."""
        client = APIClient()

        response = client.get('/api/categories/walmart-games-xbox-one-games/',
                              format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Games')
