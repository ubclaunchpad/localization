from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Token, Translation
from .services.translation_processor import bulk_create_translations, bulk_update_translations, get_translations_by_language


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
        retrieve_url = reverse('read-token', args=['123e4567-e89b-12d3-a456-426614174000'])  # random uuid

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

    def test_token_does_not_exist(self):
        translations_data = {
            'translations': [{
                'language': 'spanish',
                'hello': 'hola',
            }]
        }
        headers = {
            'HTTP_Token': 'c84234c3-b507-4ed0-a6eb-8b10116cdef1'
        }
        response = self.client.post(reverse('process-translations'), translations_data, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Missing valid token.')

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
        self.assertEqual(response.data['message'], 'All translations created successfully.')
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

    def test_create_bulk_translations_rollback(self):
        """
        Tests atomic transaction in post to rollback changes.
        """
        invalid_translations = [
            ("hello", "hola", "spanish"),
            ("bye", "chau", "spanish"),
            ("another_word", None, "spanish")
        ]
        token = Token.objects.get(value=self.TEST_TOKEN)
        success, added_count = bulk_create_translations(token, invalid_translations)
        self.assertEqual(success, False)
        self.assertEqual(added_count, 0)
        translations = Translation.objects.all()
        self.assertEqual(len(translations), 0)

    def test_patch_translation_valid(self):
        """
        Test patch endpoint with one updated translation.
        """
        translations_data = {
            'translations': [
                {
                    'language': 'spanish',
                    'hello': 'hola',
                },
                {
                    'language': 'french',
                    'hello': 'bonjour',
                    'goodbye': 'adieu',
                }
            ]
        }
        headers = {
            'HTTP_Token': self.TEST_TOKEN
        }
        response = self.client.post(reverse('process-translations'), translations_data, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        modified_translations_data = {
            'translations': [
                {
                    'language': 'spanish',
                    'hello': 'hola2',
                },
                {
                    'language': 'french',
                    'hello': 'pizza',
                }
            ]
        }
        response = self.client.patch(reverse('process-translations'), modified_translations_data, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'All translations updated successfully.')
        self.assertEqual(response.data['updated_count'], 2)

    def test_patch_extra_translation(self):
        """
        Tests when user attempts to add a new translation using patch endpoint.
        """
        translations_data = {
            'translations': [
                {
                    'language': 'spanish',
                    'hello': 'hola',
                },
            ]
        }
        headers = {
            'HTTP_Token': self.TEST_TOKEN
        }
        response = self.client.patch(reverse('process-translations'), translations_data, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Use a POST request to make new translations.')

    def test_update_translations_rollback(self):
        """
        Tests atomic transaction in patch to rollback changes.
        """
        invalid_translations = [
            ("hello", "hola", "spanish"),
            ("bye", "chau", "spanish"),
            ("another_word", None, "spanish")
        ]
        token = Token.objects.get(value=self.TEST_TOKEN)
        success, added_count = bulk_update_translations(token, invalid_translations)
        self.assertEqual(success, False)
        self.assertEqual(added_count, 0)
        translations = Translation.objects.all()
        self.assertEqual(len(translations), 0)

    def test_get_translations_no_translations_found(self):
        translations_data = {
            'translations': [
                {
                    'language': 'spanish',
                    'hello': 'hola'
                }
            ]
        }
        query_params = {
            'language': 'french'
        }

        headers = {
            'HTTP_Token': self.TEST_TOKEN
        }

        # create spanish translations
        response = self.client.post(reverse('process-translations'), translations_data, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      
        # fetch french translations
        response = self.client.get(reverse('process-translations'), **headers, query_params=query_params)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'No translations found for french.')

    def test_get_translations_by_language(self):
        translations_data = {
            'translations': [
                {
                    'language': 'spanish',
                    'hello': 'hola'
                }
            ]
        }
        query_params = {
            'language': 'spanish'
        }
        
        expected_response_data = {
            'hello': 'hola'
        }

        headers = {
            'HTTP_Token': self.TEST_TOKEN
        }

        # create spanish translations
        response = self.client.post(reverse('process-translations'), translations_data, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # fetch spanish translations
        response = self.client.get(reverse('process-translations'), **headers, query_params=query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response_data)

class TranslationViewTests(APITestCase):
    

    def setUp(self):
        token = Token.objects.create()
        self.TEST_TOKEN = str(token.value)

    def test_no_token(self):
        query_params = {
            'language': 'Spanish',
            'hello': 'hola'
        }
        response = self.client.post(reverse('translation'), query_params=query_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Token is required.')

        response = self.client.patch(reverse('translation'), query_params=query_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Token is required.')

        response = self.client.get(reverse('translation'), query_params=query_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Token is required.')

        response = self.client.delete(reverse('translation'), query_params=query_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Token is required.')

    def test_token_does_not_exist(self):
        query_params = {
            'language': 'Spanish',
            'hello': 'hola'
        }
        headers = {
            'token': 'c84234c3-b507-4ed0-a6eb-8b10116cdef1'
        }
        response = self.client.post(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Missing valid token.')

        response = self.client.patch(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Missing valid token.')

        response = self.client.get(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Missing valid token.')

        response = self.client.delete(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Missing valid token.')

    def test_empty_query_params(self):
        query_params = {}
        headers = {
            'token': self.TEST_TOKEN
        }

        response = self.client.post(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing required fields in query params.')

        response = self.client.patch(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing required fields in query params.')

        response = self.client.get(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing required fields in query params.')

        response = self.client.delete(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing required fields in query params.')

    def test_invalid_token(self):
        query_params = {
            'language': 'Spanish',
            'hello': 'hola'
        }
        headers = {
            'token': 'invalid-token'
        }

        response = self.client.post(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid token.')

        response = self.client.patch(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid token.')

        response = self.client.delete(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid token.')

        response = self.client.get(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid token.')

    def test_multiple_translations(self):
        query_params = {
            'language': 'Spanish',
            'hello': 'hola',
            'bye': 'adios'
        }
        headers = {
            'token': self.TEST_TOKEN
        }

        response = self.client.post(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'query params should only include language and one translation pair!')

        response = self.client.patch(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'query params should only include language and one translation pair!')

        response = self.client.delete(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'query params should only include language and one translation pair!')

    def test_non_string_keys(self):
        query_params = {
            'language': 'spanish',
            23: 'hola'
        }
        headers = {
            'token': self.TEST_TOKEN
        }

        response = self.client.post(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Translation pair must be in string format!')

        response = self.client.patch(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Translation pair must be in string format!')

        response = self.client.delete(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Translation pair must be in string format!')

    def test_non_string_values(self):
        query_params = {
            'language': 'Spanish',
            'hello': 2,
        }
        headers = {
            'token': self.TEST_TOKEN
        }

        response = self.client.post(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Translation pair must be in string format!')

        response = self.client.patch(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Translation pair must be in string format!')

        response = self.client.delete(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Translation pair must be in string format!')

    def test_missing_language_key(self):
        query_params = {
            'hello': 'hola',
        }
        headers = {
            'token': self.TEST_TOKEN
        }

        response = self.client.post(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing required fields in query params.')

        response = self.client.patch(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing required fields in query params.')

        response = self.client.get(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing required fields in query params.')

        response = self.client.delete(reverse('translation'), query_params=query_params, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing required fields in query params.')

    def test_updating_translation_with_post(self):
        query_params = {
                'language': 'spanish',
                'hello': 'hola'
        }
        query_params_updated = {
            'language': 'spanish',
            'hello': 'Caramba'
        }
        query_params_get = {
            'language': 'spanish',
            'original_word': 'hello'
        }
        data_get = {
            "language": 'spanish',
            "original_word": 'hello',
            "translated_word": 'hola'
        }
        headers = {
            'token': self.TEST_TOKEN
        }

        # create translation
        self.client.post(reverse('translation'), query_params=query_params, headers=headers, format='json')
        response = self.client.get(reverse('translation'), query_params=query_params_get, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, data_get)

        # try to update translation with post
        response = self.client.post(reverse('translation'),query_params=query_params_updated, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Use a PATCH request to make updates to translations.')

        # assert that the translation remains the same
        response = self.client.get(reverse('translation'), query_params=query_params_get, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, data_get)

    def test_add_translations(self):
        query_params = {
            'language': 'spanish',
            'hello': 'hola'
        }
        headers = {
            'token': self.TEST_TOKEN
        }
        data = {
            "message": "Translation created successfuly!",
            "language": 'spanish',
            "original_word": 'hello',
            "translated_word": 'hola'
        }
        query_params_get = {
            'language': 'spanish',
            'original_word': 'hello'
        }
        data_get = {
            "language": 'spanish',
            "original_word": 'hello',
            "translated_word": 'hola'
        }

        # validate post request
        response = self.client.post(reverse('translation'), query_params=query_params, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.data, data)

        # validate get request
        response = self.client.get(reverse('translation'), query_params=query_params_get, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, data_get)

    def test_duplicate_additions(self):
        query_params = {
            'language': 'spanish',
            'hello': 'hola'
        }
        headers = {
            'token': self.TEST_TOKEN
        }
        self.client.post(reverse('translation'), query_params=query_params, headers=headers, format='json')
        response = self.client.post(reverse('translation'), query_params=query_params, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Existing translation already exists!')

    def test_patch_translation_valid(self):
        """
        Test patch endpoint with one updated translation.
        """
        query_params = {
                'language': 'spanish',
                'hello': 'hola'
        }
        query_params_updated = {
            'language': 'spanish',
            'hello': 'Caramba'
        }
        query_params_get = {
            'language': 'spanish',
            'original_word': 'hello'
        }
        data_get = {
            "language": 'spanish',
            "original_word": 'hello',
            "translated_word": 'hola'
        }
        patch_data = {
            "message": "Translation updated successfuly!",
            "language": 'spanish',
            "original_word": 'hello',
            "original_translated_word": 'hola',
            "updated_translated_word": 'Caramba'
        }
        headers = {
            'token': self.TEST_TOKEN
        }

        # post request
        self.client.post(reverse('translation'), query_params=query_params, headers=headers, format='json')

        # validate get request
        response = self.client.get(reverse('translation'), query_params=query_params_get, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, data_get)
        data_get['translated_word'] = 'Caramba'

        # validate patch request
        patch_response = self.client.patch(reverse('translation'),query_params=query_params_updated, headers=headers, format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(patch_response.data, patch_data)

        # validate database is updated succesfully
        response = self.client.get(reverse('translation'), query_params=query_params_get, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, data_get)


    def test_patch_new_translation(self):
        """
        Tests when user attempts to add a new translation using patch endpoint.
        """
        query_params = {
            'language': 'spanish',
            'hello': 'hola'
        }
        query_params_get = {
            'language': 'spanish',
            'original_word': 'hello'
        }
        headers = {
            'token': self.TEST_TOKEN
        }

        response = self.client.patch(reverse('translation'), query_params=query_params, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Use a POST request to make new translations.')

        response = self.client.get(reverse('translation'), query_params=query_params_get, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Translation not found for given language and word!')

    def test_delete(self):
        """
        Tests when user attempts to add a new translation using patch endpoint.
        """
        query_params = {
            'language': 'spanish',
            'hello': 'hola'
        }
        query_params_get = {
            'language': 'spanish',
            'original_word': 'hello'
        }
        data = {
            "message": "Translation deleted successfuly!",
            "language": 'spanish',
            "original_word": 'hello',
            "translated_word": 'hola'
        }
        headers = {
            'token': self.TEST_TOKEN
        }

        self.client.post(reverse('translation'), query_params=query_params, headers=headers, format='json')

        response = self.client.delete(reverse('translation'), query_params=query_params, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

        response = self.client.get(reverse('translation'), query_params=query_params_get, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Translation not found for given language and word!')

    def test_duplicate_delete(self):
        """
        Tests when user attempts to add a new translation using patch endpoint.
        """
        query_params = {
            'language': 'spanish',
            'hello': 'hola'
        }
        headers = {
            'token': self.TEST_TOKEN
        }

        self.client.post(reverse('translation'), query_params=query_params, headers=headers, format='json')

        response = self.client.delete(reverse('translation'), query_params=query_params, headers=headers, format='json')
        response = self.client.delete(reverse('translation'), query_params=query_params, headers=headers, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "translation doesn't exist!")

    def test_bulk_translations(self):
        query_params_post = [
            {
                'language': 'spanish',
                'hello': 'hola'
            },
            {
                'language': 'spanish',
                'bye': 'adios'
            },
            {
                'language': 'french',
                'hello': 'bonjour'
            },
            {
                'language': 'french',
                'you': 'tu'
            }
        ]

        data_post = [
            {
                "message": "Translation created successfuly!",
                "language": 'spanish',
                "original_word": 'hello',
                "translated_word": 'hola'
            },
            {
                "message": "Translation created successfuly!",
                "language": 'spanish',
                "original_word": 'bye',
                "translated_word": 'adios'
            },
            {
                "message": "Translation created successfuly!",
                "language": 'french',
                "original_word": 'hello',
                "translated_word": 'bonjour'
            },
            {
                "message": "Translation created successfuly!",
                "language": 'french',
                "original_word": 'you',
                "translated_word": 'tu'
            }
        ]

        query_params_get = [
            {
                'language': 'spanish',
                'original_word': 'hello'
            },
            {
                'language': 'spanish',
                'original_word': 'bye'
            },
            {
                'language': 'french',
                'original_word': 'hello'
            },
            {
                'language': 'french',
                'original_word': 'you'
            },
        ]

        data_get = [
            {
                "language": 'spanish',
                "original_word": 'hello',
                "translated_word": 'hola'
            },
            {
                "language": 'spanish',
                "original_word": 'bye',
                "translated_word": 'adios'
            },
            {
                "language": 'french',
                "original_word": 'hello',
                "translated_word": 'bonjour'
            },
            {
                "language": 'french',
                "original_word": 'you',
                "translated_word": 'tu'
            }
        ]

        data_get_patch = [
            {
                "language": 'spanish',
                "original_word": 'hello',
                "translated_word": 'caramba'
            },
            {
                "language": 'spanish',
                "original_word": 'bye',
                "translated_word": 'adios2'
            },
            {
                "language": 'french',
                "original_word": 'hello',
                "translated_word": 'salut'
            },
            {
                "language": 'french',
                "original_word": 'you',
                "translated_word": 'vous'
            }
        ]

        query_params_patch = [
            {
                'language': 'spanish',
                'hello': 'caramba'
            },
            {
                'language': 'spanish',
                'bye': 'adios2'
            },
            {
                'language': 'french',
                'hello': 'salut'
            },
            {
                'language': 'french',
                'you': 'vous'
            }
        ]

        data_patch = [
            {
                "message": "Translation updated successfuly!",
                "language": 'spanish',
                "original_word": 'hello',
                "original_translated_word": 'hola',
                "updated_translated_word": 'caramba'
            },
            {
                "message": "Translation updated successfuly!",
                "language": 'spanish',
                "original_word": 'bye',
                "original_translated_word": 'adios',
                "updated_translated_word": 'adios2'
            },
            {
                "message": "Translation updated successfuly!",
                "language": 'french',
                "original_word": 'hello',
                "original_translated_word": 'bonjour',
                "updated_translated_word": 'salut'
            },
            {
                "message": "Translation updated successfuly!",
                "language": 'french',
                "original_word": 'you',
                "original_translated_word": 'tu',
                "updated_translated_word": 'vous'
            }
        ]

        data_delete = [
            {
                "message": "Translation deleted successfuly!",
                "language": 'spanish',
                "original_word": 'hello',
                "translated_word": 'caramba'
            },
            {
                "message": "Translation deleted successfuly!",
                "language": 'spanish',
                "original_word": 'bye',
                "translated_word": 'adios2'
            },
            {
                "message": "Translation deleted successfuly!",
                "language": 'french',
                "original_word": 'hello',
                "translated_word": 'salut'
            },
            {
                "message": "Translation deleted successfuly!",
                "language": 'french',
                "original_word": 'you',
                "translated_word": 'vous'
            }
        ]

        headers = {
            'token': self.TEST_TOKEN
        }

        # validate bulk post
        for i in range(0, 4):
            # validate post requests
            response = self.client.post(reverse('translation'), query_params=query_params_post[i], headers=headers, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertDictEqual(response.data, data_post[i])

            # validate get requests
            response = self.client.get(reverse('translation'), query_params=query_params_get[i], headers=headers)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response.data, data_get[i])

        # validate bulk patch
        for i in range(0, 4):
            # validate patch requests
            response = self.client.patch(reverse('translation'), query_params=query_params_patch[i], headers=headers, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertDictEqual(response.data, data_patch[i])

            # validate get requests
            response = self.client.get(reverse('translation'), query_params=query_params_get[i], headers=headers)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response.data, data_get_patch[i])

        #validate bulk delete
        for i in range(0, 4):
            # validate delete requests
            response = self.client.delete(reverse('translation'), query_params=query_params_patch[i], headers=headers, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response.data, data_delete[i])

            # validate get requests
            response = self.client.get(reverse('translation'), query_params=query_params_get[i], headers=headers)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.data['error'], 'Translation not found for given language and word!')

class PullTranslations(APITestCase):

    def setUp(self):
        token = Token.objects.create()
        self.TEST_TOKEN = str(token.value)
   
    def test_pulling_multiple_assigned_translations(self):
        headers = {
            'Token': self.TEST_TOKEN
        }
        translations_data = {
            'translations': [
                {
                    'language': 'spanish',
                    'hello': 'hola',
                    'bye': 'chau',
                },
                {
                    'language': 'french',
                    'hello': 'bonjour',
                }
            ]
        }
        expected_response = {
            'spanish': {
                'hello': 'hola',
                'bye': 'chau',
            },
            'french': {
                'hello': 'bonjour',
            }
        }

        self.client.post(reverse('process-translations'), data=translations_data, headers=headers, format='json')

        response = self.client.get(reverse('pull-translations'), headers=headers, format='json')
        response_data = response.json()
        self.assertEqual(response_data, expected_response)
