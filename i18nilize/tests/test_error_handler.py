import json
import os
import unittest
from internationalize.error_handler import ErrorHandler

class TestErrorHandler(unittest.TestCase):
    def setUp(self):
        self.test_folder = os.path.join("tests", "resources", "error_handling")
        self.translations_folder = os.path.join(self.test_folder, "translations")
        self.handler = ErrorHandler(self.translations_folder)

    # ================== Test Keys ================================
    def test_valid_keys(self):
        language = "valid_keys.json"
        self.assertEqual(self.handler.handle_invalid_keys(language), "")

    def test_non_string_values(self):
        language = "non_string_values.json"
        self.assertEqual(self.handler.handle_invalid_keys(language), "Value is not a string.")

    def test_empty_or_whitespace_keys(self):
        language = "empty_keys.json"
        self.assertEqual(self.handler.handle_invalid_keys(language), "Key is empty or contains only whitespace.")

    def test_combined_issues(self):
        language = "combined_issues.json"
        self.assertEqual(self.handler.handle_invalid_keys(language), "Value is not a string.")

    # ================== Test Invalid Files ================================
    
    def test_invalid_file_individual(self):
        language = "invalid_file.json"
        self.assertEqual(self.handler.handle_invalid_file(language), "Invalid language file, try fixing the json format.")

    # ================== Test Error Handler ================================
    def test_invalid_file(self):
        print("invalid File Test: ")
        language = "invalid_file.json"
        self.assertEqual(self.handler.handle_error(language), "Invalid language file, try fixing the json format.")

    def test_non_string_values(self):
        language = "non_string_values.json"
        self.assertEqual(self.handler.handle_error(language), "Value is not a string.")

    def test_valid_expected(self):
        language = "valid_keys.json"
        self.assertEqual(self.handler.handle_error(language), "")

    # ================== Test Folder ================================
    def test_invalid_folder(self):
        with open(os.path.join(self.test_folder, "expected.json"), "r") as file:
            expected = json.load(file)

        self.assertEqual(self.handler.verify_languages(), expected)

if __name__ == "__main__":
    unittest.main()
