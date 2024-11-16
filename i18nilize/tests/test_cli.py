import unittest, os, json, timeit
from unittest.mock import patch
from src.internationalize.helpers import get_json, make_translation_map, get_translation, add_language, add_update_translated_word

# Create your tests here.            
# To test:
# In i18nilize directory, run python -m tests.test_cli

class TestCLI(unittest.TestCase):                
    def setUp(self):
        self.languages_dir = "src/internationalize/languages"
        os.makedirs(self.languages_dir, exist_ok=True)

    def test_add_new_language(self):
        new_language = "Japanese"
        add_language(new_language)
        new_language_path = os.path.join(self.languages_dir, f"{new_language.lower()}.json")
        self.assertTrue(os.path.exists(new_language_path))

        with open(new_language_path, "r") as file:
            data = json.load(file)
        self.assertEqual(data, {})

        # clean up test
        os.remove(new_language_path)

    def test_add_word_language_exists(self):
        existing_language = "French"
        file_path = os.path.join(self.languages_dir, f"{existing_language.lower()}.json")
        self.assertTrue(os.path.exists(file_path))

        # save original state
        with open(file_path, "r") as file:
            original_translations = json.load(file)

        data = get_json(file_path)
        self.assertEqual(len(data), 2)

        add_update_translated_word("French", "good", "bien")
        data = get_json(file_path)
        self.assertEqual(len(data), 3)
        self.assertEqual(data["good"], "bien")

        # clean up test
        with open(file_path, 'w') as file:
            json.dump(original_translations, file, indent=4)

    def test_update_word_language_exists(self):
        existing_language = "French"
        file_path = os.path.join(self.languages_dir, f"{existing_language.lower()}.json")
        self.assertTrue(os.path.exists(file_path))

        # save original state
        with open(file_path, "r") as file:
            original_translations = json.load(file)

        data = get_json(file_path)
        self.assertEqual(len(data), 2)

        add_update_translated_word("French", "thanks", "merc")
        data = get_json(file_path)
        self.assertEqual(len(data), 2)
        self.assertEqual(data["thanks"], "merc")

        # clean up test
        with open(file_path, 'w') as file:
            json.dump(original_translations, file, indent=4)

    @patch('builtins.print')
    def test_add_word_language_does_not_exist(self, mock_print):
        with self.assertRaises(SystemExit) as context:
            add_update_translated_word("NonExistentLanguage", "hello", "ciao")
        self.assertTrue(context.exception.code, 1)

        mock_print.assert_called_once_with("Error: Language 'NonExistentLanguage' does not exist. Add the language before adding a translation.")

if __name__ == '__main__':
    unittest.main()
