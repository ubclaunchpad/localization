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
        Localize.translations_map["french"] = {"hello": "bonjour"}
        Localize.load_language("french")

        mock_path_exists.assert_not_called()

    def test_load_existing_language(self):
        Localize.load_language("spanish")

        self.assertIn("spanish", Localize.translations_map)
        self.assertEqual(Localize.translations_map["spanish"], {"hello": "hola", "thanks": "gracias"})

    def test_load_non_existing_language(self):
        with self.assertRaises(FileNotFoundError) as context:
            Localize.load_language("german")

        self.assertEqual(str(context.exception), "Translations for german not found.")

    def test_translate_valid(self):
        self.assertEqual(Localize.translate("hello", "spanish"), "hola", "Translation error: is the translation missing from the language file?")
        self.assertEqual(Localize.translate("thanks", "french"), "merci", "Translation error: is the translation missing from the language file?")

    def test_translate_invalid(self):
        self.assertEqual(Localize.translate("asdf", "spanish"), "Translation not found")

    def test_translate_invalid_language(self):
        self.assertRaises(FileNotFoundError, Localize.translate, "hello", "asdf")


if __name__ == '__main__':
    unittest.main()
