"""Views' test cases."""

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class BaseViewSetTest(TestCase):
    """Base class for ViewSet test cases."""

    def setUp(self):
        self.client = APIClient()


class ChannelViewSetTest(BaseViewSetTest):
    """ChannelViewSet's test cases."""

    fixtures = ['viewtests']

    def test_list(self):
        """Tests '/api/v1/channels/' endpoint."""
        response = self.client.get('/api/v1/channels/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve(self):
        """Tests '/api/v1/channels/{reference}' endpoint."""
        response = self.client.get('/api/v1/channels/walmart/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'walmart')

    def test_retrieve_non(self):
        """Tests '/api/v1/channels/{reference}' endpoint against a nonexistent
        reference."""
        response = self.client.get('/api/v1/channels/amazon/', format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CategoryViewSetTest(BaseViewSetTest):
    """CategoryViewSet's test cases."""

    fixtures = ['viewtests']

    def test_list(self):
        """Tests '/api/v1/categories/' endpoint."""
        response = self.client.get('/api/v1/categories/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 24)

    def test_retrieve(self):
        """Tests '/api/v1/categories/{reference}' endpoint."""
        response = self.client.get(
            '/api/v1/categories/walmart-games-xbox-one-games/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Games')

    def test_retrieve_non(self):
        """Tests '/api/v1/categories/{reference}' endpoint against a
        nonexistent reference."""
        response = self.client.get('/api/v1/categories/amazon-books/',
                                   format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_relatives(self):
        """Tests 'api/v1/categories/{reference}/relatives/ endpoint."""
        response = self.client.get(
            '/api/v1/categories/walmart-games-xbox-one/relatives/',
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'XBOX One')

    def test_relatives_non(self):
        """Tests 'api/v1/categories/{reference}/relatives/ endpoint against a
        nonexistent reference."""
        response = self.client.get(
            '/api/v1/categories/amazon-books/relatives/', format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_nested_list(self):
        """Tests '/api/v1/channels/{reference}/categories/' endpoint."""
        response = self.client.get('/api/v1/channels/walmart/categories/',
                                   format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 24)

    def test_nested_list_non(self):
        """Tests '/api/v1/channels/{reference}/categories/' endpoint against a
        nonexistent channel's reference."""
        response = self.client.get('/api/v1/channels/amazon/categories/',
                                   format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_nested_retrieve(self):
        """Tests '/api/v1/channels/{reference}/categories/{reference}'
        endpoint."""
        response = self.client.get(
            '/api/v1/channels/walmart/categories/walmart-games-xbox-one-games/',
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Games')

    def test_nested_retrieve_non(self):
        """Tests '/api/v1/channels/{reference}/categories/{reference}'
        endpoint against a nonexistent channel's reference."""
        response = self.client.get(
            '/api/v1/channels/amazon/categories/walmart-games/', format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_nested_relatives(self):
        """Tests 'api/v1/channels/{reference}/categories/{reference}/relatives/
        endpoint."""
        response = self.client.get(
            '/api/v1/channels/walmart/categories/walmart-games-xbox-one/relatives/',
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'XBOX One')

    def test_nested_relatives_non(self):
        """Tests 'api/v1/channels/{reference}/categories/{reference}/relatives/
        endpoint against a nonexistent channel's reference."""
        response = self.client.get(
            '/api/v1/channels/amazon/categories/walmart-games/relatives/',
            format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
