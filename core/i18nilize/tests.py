from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Token

# Create your tests here.
class TokenViewTests(APITestCase):

    def setUp(self):
        self.create_url = reverse('create-token') 

    def test_create_token(self):
        """
        Ensure that a POST request creates a token successfully and returns it
        """
        response = self.client.post(self.create_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('value', response.data)
        self.assertIn('created_at', response.data)
        self.assertEqual(Token.objects.count(), 1)
        token = Token.objects.first()
        self.assertEqual(token.id, response.data['id'])
        self.assertEqual(str(token.value), response.data['value'])

    def test_retrieve_existing_token(self):
        """
        Ensure that a GET request retrieves an existing token
        """
        token = Token.objects.create()
        retrieve_url = reverse('read-token', args=[str(token.value)])

        response = self.client.get(retrieve_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], token.id)
        self.assertEqual(response.data['value'], str(token.value))
        self.assertEqual(response.data['created_at'], token.created_at.isoformat())

    def test_retrieve_nonexistent_token(self):
        """
        Ensure that a GET request for a non-existent token returns a 404 error
        """
        retrieve_url = reverse('read-token', args=['123e4567-e89b-12d3-a456-426614174000']) #random uuid

        response = self.client.get(retrieve_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Token not found.')