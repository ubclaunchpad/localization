import unittest
from unittest.mock import patch, Mock
import json
import os
from src.internationalize.helpers import generate_file

# run tests using python -m tests.test_generate_file at i18nilize directory level

class TestGenerateFile(unittest.TestCase):                
    def setUp(self):
        self.TEST_TOKEN = '85124f79-0829-4b80-8b5c-d52700d86e46'

    @patch('src.internationalize.helpers.requests.get')
    def test_generate_file_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = { 
            'hello': 'hola',
            'thanks': 'gracias'
        }  
        mock_get.return_value = mock_response

        generate_file('spanish', self.TEST_TOKEN)
        
        expected_file_path = './src/internationalize/languages/spanish.json'
        self.assertTrue(os.path.exists(expected_file_path))

        with open (expected_file_path, 'r') as file:
            content = file.read()
            expected_content = json.dumps(mock_response.json.return_value, indent = 4)
            self.assertEqual(content, expected_content)
    
    @patch('src.internationalize.helpers.requests.get')
    def test_generate_file_error(self, mock_get):
        # Mock the response object
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'error': 'Language not found'}  # Proper dictionary
        mock_get.return_value = mock_response

        # Call the function
        generate_file('french', self.TEST_TOKEN)

        # Check that the file does not exist
        expected_file_path = './src/internationalize/languages/french.json'
        self.assertFalse(os.path.exists(expected_file_path))

if __name__ == '__main__':
    unittest.main()
