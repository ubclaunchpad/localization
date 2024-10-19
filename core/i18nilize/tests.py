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

class ProcessTranslationsViewTests(APITestCase):

    def setUp(self):
        token = Token.objects.create()
        self.TEST_TOKEN = str(token.value)

    def test_no_token(self):
        translations_data = {
            'translations': []
        }
        response = self.client.post(reverse('process-translations'), translations_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Token is required.')
    
    def test_no_translations_data(self):
        translations_data = {}
        headers = {
            'HTTP_Token': self.TEST_TOKEN
        }
        response = self.client.post(reverse('process-translations'), translations_data, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Translations data is required.')
    
    def test_invalid_token(self):
        translations_data = {
            'translations': []
        }
        headers = {
            'HTTP_Token': 'invalid-token'
        }
        response = self.client.post(reverse('process-translations'), translations_data, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid token.')
    
    def test_missing_translations_key(self):
        translations_data = {
            'language': 'spanish',
            'hello': 'hola',
        }
        headers = {
            'HTTP_Token': self.TEST_TOKEN
        }
        response = self.client.post(reverse('process-translations'), translations_data, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Translations are improperly formatted.')
    
    def test_non_string_keys(self):
        translations_data = {
            'translations': [{
                1: 'spanish',
                'hello': 'hola',
            }]
        }
        headers = {
            'HTTP_Token': self.TEST_TOKEN
        }
        response = self.client.post(reverse('process-translations'), translations_data, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Translations are improperly formatted.')
    
    def test_non_string_values(self):
        translations_data = {
            'translations': [{
                'language': 1,
                'hello': 'hola',
            }]
        }
        headers = {
            'HTTP_Token': self.TEST_TOKEN
        }
        response = self.client.post(reverse('process-translations'), translations_data, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Translations are improperly formatted.')
    
    def test_missing_language_key(self):
        translations_data = {
            'translations': [{
                'hello': 'hola',
                'what': 'que',
            }]
        }
        headers = {
            'HTTP_Token': self.TEST_TOKEN
        }
        response = self.client.post(reverse('process-translations'), translations_data, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Translations are improperly formatted.')
    
    def test_updating_translation(self):
        translations_data = {
            'translations': [{
                'language': 'spanish',
                'hello': 'hola'
            }]
        }
        translations_data_updated = {
            'translations': [{
                'language': 'spanish',
                'hello': 'hola2'
            }]
        }
        headers = {
            'HTTP_Token': self.TEST_TOKEN
        }
        self.client.post(reverse('process-translations'), translations_data, **headers, format='json')
        response = self.client.post(reverse('process-translations'), translations_data_updated, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Use a PATCH request to make updates to translations.')
    
    def test_add_translations(self):
        translations_data = {
            'translations': [
                {
                    'language': 'spanish',
                    'hello': 'hola'
                },
                {
                    'language': 'french',
                    'hello': 'bonjour'
                },
                {
                    'language': 'italian',
                    'hello': 'bonjourno'
                }
            ]
        }
        headers = {
            'HTTP_Token': self.TEST_TOKEN
        }
        response = self.client.post(reverse('process-translations'), translations_data, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'All translations created successfully.')
        self.assertEqual(response.data['added_count'], 3)
    
    def test_no_new_additions(self):
        translations_data = {
            'translations': [
                {
                    'language': 'spanish',
                    'hello': 'hola'
                }
            ]
        }
        headers = {
            'HTTP_Token': self.TEST_TOKEN
        }
        self.client.post(reverse('process-translations'), translations_data, **headers, format='json')
        response = self.client.post(reverse('process-translations'), translations_data, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'No new translations to add.')
        self.assertEqual(response.data['added_count'], 0)
    
    def test_duplicate_additions(self):
        translations_data = {
            'translations': [
                {
                    'language': 'spanish',
                    'hello': 'hola'
                },
                {
                    'language': 'spanish',
                    'hello': 'hola',
                    'hello': 'hola'
                },
            ]
        }
        headers = {
            'HTTP_Token': self.TEST_TOKEN
        }
        response = self.client.post(reverse('process-translations'), translations_data, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'All translations created successfully.')
        self.assertEqual(response.data['added_count'], 1)