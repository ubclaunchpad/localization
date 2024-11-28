import unittest
from src.internationalize.error_handler import ErrorHandler

class TestErrorHandler(unittest.TestCase):
    def test_valid_keys(self):
        handler = ErrorHandler({})
        language = {
            "hello": "bonjour",
            "thanks": "merci"
        }
        self.assertEqual(handler.handle_invalid_keys(language), "")

    def test_non_string_keys(self):
        handler = ErrorHandler({})
        language = {
            123: "bonjour",
            None: "merci"
        }
        self.assertEqual(handler.handle_invalid_keys(language), "Key '123' is not a string.")

    def test_empty_or_whitespace_keys(self):
        handler = ErrorHandler({})
        language = {
            "": "bonjour",
            "   ": "merci"
        }
        self.assertEqual(handler.handle_invalid_keys(language), "Key is empty or only contains whitespace.")

    def test_combined_issues(self):
        handler = TranslationHandler({})
        language = {
            123: "bonjour",
            "   ": "merci",
            "hello-world": "salut"
        }
        self.assertEqual(handler.handle_invalid_keys(language), "Key '123' is not a string.")

if __name__ == "__main__":
    unittest.main()
