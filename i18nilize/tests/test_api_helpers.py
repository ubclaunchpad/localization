# test_api_helpers.py

import unittest
from unittest.mock import patch, MagicMock
import os
import json
import sys

from internationalize.api_helpers import create_token, fetch_translation_data
from src.internationalize import globals

class TestAPIHelpers(unittest.TestCase):

    def setUp(self):
        self.languages_dir = "src/internationalize/languages"
        os.makedirs(self.languages_dir, exist_ok=True)

        self.original_token = globals.token

    def tearDown(self):
        globals.token = self.original_token

        # clean up any created language files
        if os.path.exists(self.languages_dir):
            for filename in os.listdir(self.languages_dir):
                if filename.endswith('.json'):
                    os.remove(os.path.join(self.languages_dir, filename))


    @patch('src.internationalize.api_helpers.TokenView')
    def test_create_token_success(self, mock_token_view):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.data = {'value': 'test-token'}
        mock_token_view_instance = MagicMock()
        mock_token_view_instance.post.return_value = mock_response
        mock_token_view.return_value = mock_token_view_instance

        with patch('builtins.print') as mock_print:
            create_token()

            mock_token_view_instance.post.assert_called_once()
            self.assertEqual(globals.token, 'test-token')
            mock_print.assert_called_once_with("Token set.")

    @patch('src.internationalize.api_helpers.TokenView')
    def test_create_token_failure(self, mock_token_view):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.data = {'error': 'Bad Request'}
        mock_token_view_instance = MagicMock()
        mock_token_view_instance.post.return_value = mock_response
        mock_token_view.return_value = mock_token_view_instance

        with patch('builtins.print') as mock_print:
            with self.assertRaises(Exception) as context:
                create_token()

            mock_token_view_instance.post.assert_called_once()
            self.assertIn("Failed to retrieve token. Status code: 400", str(context.exception))
            mock_print.assert_not_called()  # no print on failure as per function definition

    @patch('src.internationalize.api_helpers.translation_processor.get_translations_by_language')
    @patch('src.internationalize.api_helpers.create_token')
    def test_fetch_translation_data_token_exists(self, mock_create_token, mock_get_translations):
        globals.token = 'existing-token'

        mock_get_translations.return_value = {'hello': 'hola'}

        with patch('builtins.print') as mock_print:
            fetch_translation_data('Spanish')

            mock_create_token.assert_not_called()
            mock_get_translations.assert_called_once_with('Spanish', 'existing-token')
            mock_print.assert_called_once_with("Generated translation data for language: Spanish")

    @patch('src.internationalize.api_helpers.translation_processor.get_translations_by_language')
    @patch('src.internationalize.api_helpers.create_token')
    def test_fetch_translation_data_token_missing_and_created_successfully(self, mock_create_token, mock_get_translations):
        globals.token = ''

        def side_effect_create_token():
            globals.token = 'new-token'
            print("Token set.")
        mock_create_token.side_effect = side_effect_create_token

        mock_get_translations.return_value = {'hello': 'hola'}

        with patch('builtins.print') as mock_print:
            fetch_translation_data('Spanish')

            mock_create_token.assert_called_once()
            mock_get_translations.assert_called_once_with('Spanish', 'new-token')
            expected_calls = [patch.call("Token not found. Creating a new token..."),
                              patch.call("Token set."),
                              patch.call("Generated translation data for language: Spanish")]
            mock_print.assert_has_calls(expected_calls, any_order=False)

    @patch('src.internationalize.api_helpers.translation_processor.get_translations_by_language')
    @patch('src.internationalize.api_helpers.create_token')
    def test_fetch_translation_data_token_missing_and_creation_fails(self, mock_create_token, mock_get_translations):
        globals.token = ''

        mock_create_token.side_effect = Exception("Failed to retrieve token.")

        with patch('builtins.print') as mock_print:
            with self.assertRaises(Exception) as context:
                fetch_translation_data('Spanish')

            mock_create_token.assert_called_once()
            mock_get_translations.assert_not_called()
            mock_print.assert_called_once_with("Token not found. Creating a new token...")

    def test_fetch_translation_data_missing_language(self):
        globals.token = 'existing-token'

        with patch('builtins.print') as mock_print:
            with self.assertRaises(Exception) as context:
                fetch_translation_data('')  # Missing language

            self.assertIn("Language parameter is required.", str(context.exception))
            mock_print.assert_not_called()  # No print as per function definition

    @patch('src.internationalize.api_helpers.translation_processor.get_translations_by_language')
    def test_fetch_translation_data_no_translations_found(self, mock_get_translations):
        globals.token = 'existing-token'

        mock_get_translations.return_value = {}

        with patch('builtins.print') as mock_print:
            with self.assertRaises(Exception) as context:
                fetch_translation_data('Spanish')

            mock_get_translations.assert_called_once_with('Spanish', 'existing-token')
            self.assertIn("No translations found for language: Spanish", str(context.exception))
            mock_print.assert_called_once_with("Generated translation data for language: Spanish")  # prints even if no translations, but raises exception

    if __name__ == '__main__':
        unittest.main()
