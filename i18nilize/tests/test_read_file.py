import unittest
from src.internationalize.localize import get_token, get_translation

# run tests using python -m tests.test_read_file at i18nilize directory level

class TestLocalize(unittest.TestCase):
    file_path = "tests/resources/basic.json"

    def test_read_token(self):
        expected_token = "85124f79-0829-4b80-8b5c-d52700d86e46"
        self.assertEqual(get_token(self.file_path), expected_token)

    def test_read_translations(self):
        self.assertEqual(get_translation(self.file_path, "French", "hello"), "bonjour")
        self.assertEqual(get_translation(self.file_path, "French", "No"), "Non")
        self.assertEqual(get_translation(self.file_path, "French", "Why"), "pourquoi")
        self.assertEqual(get_translation(self.file_path, "Spanish", "hello"), "Hola")

    def test_read_bad_translations(self):
        self.assertEqual(get_translation(self.file_path, "French", "bonjour"), "'bonjour' not found in French")
        self.assertEqual(get_translation(self.file_path, "Frrench", "hello"), "'Frrench' not found")
            


unittest.main()