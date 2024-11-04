import unittest, os, json, timeit
from unittest.mock import patch
from src.internationalize.helpers import get_json, make_translation_map, get_translation, add_language, add_update_translated_word

# Create your tests here.            
# To test:
# In i18nilize directory, run python -m tests.test_cli

class TestCLI(unittest.TestCase):                
    def setUp(self):
        self.TEST_JSON_PATH = 'src/internationalize/resources/languages.json'
        with open(self.TEST_JSON_PATH, 'r') as file:
            self.original_json = json.load(file)
    
    def tearDown(self):
        with open(self.TEST_JSON_PATH, 'w') as file:
            json.dump(self.original_json, file, indent=4)

    def test_add_language(self):
        data = get_json(self.TEST_JSON_PATH)

        print("Checking Number of Translations:")
        self.assertEqual(data['Token'], "85124f79-0829-4b80-8b5c-d52700d86e46")
        self.assertEqual(len(data['translations']), 2)

        print("Checking French Translations:")
        french_translation = data['translations'][0]
        self.assertEqual(french_translation['language'], "French")
        self.assertEqual(french_translation['hello'], "bonjour")
        self.assertEqual(french_translation['No'], "Non")
        self.assertEqual(french_translation['Why'], "pourquoi")

        print("Checking Spanish Translations:")
        spanish_translation = data['translations'][1]
        self.assertEqual(spanish_translation['language'], "Spanish")
        self.assertEqual(spanish_translation['hello'], "Hola")

        add_language("Korean")
        data = get_json(self.TEST_JSON_PATH)
        self.assertEqual(data['Token'], "85124f79-0829-4b80-8b5c-d52700d86e46")
        self.assertEqual(len(data['translations']), 3)

        french_translation = data['translations'][0]
        self.assertEqual(french_translation['language'], "French")
        self.assertEqual(french_translation['hello'], "bonjour")
        self.assertEqual(french_translation['No'], "Non")
        self.assertEqual(french_translation['Why'], "pourquoi")

        spanish_translation = data['translations'][1]
        self.assertEqual(spanish_translation['language'], "Spanish")
        self.assertEqual(spanish_translation['hello'], "Hola")

        korean_translation = data['translations'][2]
        self.assertEqual(korean_translation['language'], "Korean")
        print("Test passed!")

    def test_add_existing_language(self):
        data = get_json(self.TEST_JSON_PATH)

        self.assertEqual(data['Token'], "85124f79-0829-4b80-8b5c-d52700d86e46")
        self.assertEqual(len(data['translations']), 2)

        french_translation = data['translations'][0]
        self.assertEqual(french_translation['language'], "French")
        self.assertEqual(french_translation['hello'], "bonjour")
        self.assertEqual(french_translation['No'], "Non")
        self.assertEqual(french_translation['Why'], "pourquoi")

        spanish_translation = data['translations'][1]
        self.assertEqual(spanish_translation['language'], "Spanish")
        self.assertEqual(spanish_translation['hello'], "Hola")

        add_language("Spanish")
        data = get_json(self.TEST_JSON_PATH)
        self.assertEqual(data['Token'], "85124f79-0829-4b80-8b5c-d52700d86e46")
        self.assertEqual(len(data['translations']), 2)

        french_translation = data['translations'][0]
        self.assertEqual(french_translation['language'], "French")
        self.assertEqual(french_translation['hello'], "bonjour")
        self.assertEqual(french_translation['No'], "Non")
        self.assertEqual(french_translation['Why'], "pourquoi")

        spanish_translation = data['translations'][1]
        self.assertEqual(spanish_translation['language'], "Spanish")
        self.assertEqual(spanish_translation['hello'], "Hola")
    
    def test_add_word_language_exists(self):
        data = get_json(self.TEST_JSON_PATH)
        french_translation = data['translations'][0]
        self.assertEqual(len(french_translation), 4)

        add_update_translated_word("French", "good", "bien")

        data = get_json(self.TEST_JSON_PATH)
        french_translation = data['translations'][0]
        self.assertEqual(len(french_translation), 5)
        self.assertEqual(french_translation['good'], "bien")

    def test_update_word_language_exists(self):
        data = get_json(self.TEST_JSON_PATH)
        french_translation = data['translations'][0]
        self.assertEqual(len(french_translation), 4)

        add_update_translated_word("French", "good", "bie")
        data = get_json(self.TEST_JSON_PATH)
        french_translation = data['translations'][0]
        self.assertEqual(len(french_translation), 5)
        self.assertEqual(french_translation['good'], "bie")

        add_update_translated_word("French", "good", "bien")
        data = get_json(self.TEST_JSON_PATH)
        french_translation = data['translations'][0]
        self.assertEqual(len(french_translation), 5)
        self.assertEqual(french_translation['good'], "bien")

    @patch('sys.exit')
    @patch('builtins.print')
    def test_add_word_language_does_not_exist(self, mock_print, mock_exit):
        data = get_json(self.TEST_JSON_PATH)
        self.assertEqual(len(data['translations']), 2)

        add_update_translated_word("Italian", "hello", "ciao")

        mock_exit.assert_called_once_with(1)
        mock_print.assert_called_once_with("Error: Language 'Italian' does not exist. Add the language before adding a translation.")
        data = get_json(self.TEST_JSON_PATH)
        self.assertEqual(len(data['translations']), 2)

if __name__ == '__main__':
    unittest.main()
