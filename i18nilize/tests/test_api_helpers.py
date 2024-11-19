# test_api_helpers.py

import unittest
from unittest.mock import patch, MagicMock, call
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from internationalize.api_helpers import create_token, fetch_translation_data
from internationalize.globals import token 

class TestAPIHelpers(unittest.TestCase):

    def setUp(self):
        self.languages_dir = "src/internationalize/languages"
        os.makedirs(self.languages_dir, exist_ok=True)

        # backup the original token value
        self.original_token_value = token.value

    def tearDown(self):
        # restore the original token value
        token.value = self.original_token_value

        # clean up any created language files
        if os.path.exists(self.languages_dir):
            for filename in os.listdir(self.languages_dir):
                if filename.endswith('.json'):
                    os.remove(os.path.join(self.languages_dir, filename))


    @patch('internationalize.api_helpers.requests.post')
    def test_create_token_success(self, mock_post):
        """
        Test that create_token() successfully creates a token and sets it in globals.
        """
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'value': 'test-token'}
        mock_post.return_value = mock_response

        with patch('builtins.print') as mock_print:  
            create_token()

            mock_post.assert_called_once_with("http://localhost:8000/api/token/")
            self.assertEqual(token.value, 'test-token')
            mock_print.assert_called_once_with("Token set.")

    @patch('internationalize.api_helpers.requests.post')
    def test_create_token_failure(self, mock_post):
        """
        Test that create_token() raises an exception when API call fails.
        """
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'error': 'Bad Request'}
        mock_post.return_value = mock_response

        with patch('builtins.print') as mock_print:  
            with self.assertRaises(Exception) as context:
                create_token()

            mock_post.assert_called_once_with("http://localhost:8000/api/token/") 
            self.assertIn("Failed to retrieve token. Status code: 400", str(context.exception))
            mock_print.assert_not_called()


    @patch('internationalize.api_helpers.requests.get')
    @patch('internationalize.api_helpers.create_token')
    def test_fetch_translation_data_token_exists(self, mock_create_token, mock_get):
        """
        Test that fetch_translation_data() fetches translations when token exists.
        """
        token.value = 'existing-token'

        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {'hello': 'hola'}
        mock_get.return_value = mock_get_response

        with patch('builtins.print') as mock_print:  
            translations = fetch_translation_data('Spanish')

            mock_create_token.assert_not_called()
            mock_get.assert_called_once_with(
                "http://localhost:8000/api/translations/?language=Spanish",
                headers={'Authorization': 'Token existing-token'}
            )
            mock_print.assert_called_once_with("Generated translation data for language: Spanish")
            self.assertEqual(translations, {'hello': 'hola'})

    @patch('internationalize.api_helpers.requests.get')
    @patch('internationalize.api_helpers.requests.post')
    def test_fetch_translation_data_token_missing_and_created_successfully(self, mock_post, mock_get):
        """
        Test that fetch_translation_data() creates a token if missing and fetches translations successfully.
        """
        token.value = ''

        mock_post_response = MagicMock()
        mock_post_response.status_code = 201
        mock_post_response.json.return_value = {'value': 'new-token'}
        mock_post.return_value = mock_post_response

        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {'hello': 'hola'}
        mock_get.return_value = mock_get_response

        with patch('builtins.print') as mock_print:
            translations = fetch_translation_data('Spanish')

            mock_post.assert_called_once_with("http://localhost:8000/api/token/")
            mock_get.assert_called_once_with(
                "http://localhost:8000/api/translations/?language=Spanish",
                headers={'Authorization': 'Token new-token'}
            )
            expected_calls = [
                call("Token not found. Creating a new token..."),
                call("Token set."),
                call("Generated translation data for language: Spanish")
            ]
            mock_print.assert_has_calls(expected_calls, any_order=False)
            self.assertEqual(token.value, 'new-token')
            self.assertEqual(translations, {'hello': 'hola'})

    @patch('internationalize.api_helpers.requests.get')
    @patch('internationalize.api_helpers.requests.post')
    def test_fetch_translation_data_token_missing_and_creation_fails(self, mock_post, mock_get):
        """
        Test that fetch_translation_data() raises an exception if token creation fails.
        """
        token.value = ''

        mock_post_response = MagicMock()
        mock_post_response.status_code = 400
        mock_post_response.json.return_value = {'error': 'Bad Request'}
        mock_post.return_value = mock_post_response

        with patch('builtins.print') as mock_print:
            with self.assertRaises(Exception) as context:
                fetch_translation_data('Spanish')

            mock_post.assert_called_once_with("http://localhost:8000/api/token/") 
            mock_get.assert_not_called()
            expected_calls = [
                call("Token not found. Creating a new token...")
            ]
            mock_print.assert_has_calls(expected_calls, any_order=False)
            self.assertEqual(token.value, '')  # token remains empty
            self.assertIn("Failed to retrieve token. Status code: 400", str(context.exception))

    def test_fetch_translation_data_missing_language(self):
        """
        Test that fetch_translation_data() raises an exception when language parameter is missing.
        """
        token.value = 'existing-token'

        with patch('builtins.print') as mock_print:
            with self.assertRaises(Exception) as context:
                fetch_translation_data('')  # missing language

            self.assertIn("Language parameter is required.", str(context.exception))
            mock_print.assert_not_called()

    @patch('internationalize.api_helpers.requests.get')
    def test_fetch_translation_data_no_translations_found(self, mock_get):
        """
        Test that fetch_translation_data() raises an exception when no translations are found.
        """
        token.value = 'existing-token'

        mock_get_response = MagicMock()
        mock_get_response.status_code = 404  # assuming 404 for no translations
        mock_get_response.json.return_value = {'error': 'No translations found'}
        mock_get.return_value = mock_get_response

        with patch('builtins.print') as mock_print:
            with self.assertRaises(Exception) as context:
                fetch_translation_data('Spanish')

            mock_get.assert_called_once_with(
                "http://localhost:8000/api/translations/?language=Spanish",
                headers={'Authorization': 'Token existing-token'}
            )
            mock_print.assert_called_once_with("Generated translation data for language: Spanish")
            self.assertEqual(token.value, 'existing-token')  # token remains unchanged
            self.assertIn("No translations found for language: Spanish", str(context.exception))

if __name__ == '__main__':
    unittest.main()
