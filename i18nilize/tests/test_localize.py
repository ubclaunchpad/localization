import unittest
from unittest.mock import patch
from src.internationalize.localize import Localize

# to test:
# in i18nilize directory, run python -m tests.test_localize

class TestLocalize(unittest.TestCase):
    def setUp(self):
        Localize.translations_map = {}
    
    @patch("os.path.exists")
    def test_load_language_already_in_map(self, mock_path_exists):
        Localize.translations_map["french"] = { "hello": "bonjour" }
        Localize.load_language("french")

        mock_path_exists.assert_not_called()

    def test_load_existing_language(self):
        Localize.load_language("spanish")

        self.assertIn("spanish", Localize.translations_map)
        self.assertEqual(Localize.translations_map["spanish"], { "hello": "hola", "thanks": "gracias" })

    def test_load_non_existing_language(self):
        with self.assertRaises(FileNotFoundError) as context:
            Localize.load_language("german")
        
        self.assertEqual(str(context.exception), "Translations for german not found.")

    # def basicTest(self):
    #     print(Localize.translate("en", "hello"))  # Outputs the translation if found, else "Translation not found"
    #     print(Localize.translate("es", "hello"))  # Similarly checks Spanish language file


if __name__ == '__main__':
    unittest.main()
