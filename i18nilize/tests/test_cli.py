import json
import os
import shutil
import unittest
from unittest.mock import patch

from src.internationalize import globals
from src.internationalize.helpers import (
    add_language,
    add_update_translated_word,
    delete_translation,
    get_json,
)

# Create your tests here.
# To test:
# In i18nilize directory, run python -m tests.test_cli


class TestCLI(unittest.TestCase):
    def setUp(self):
        globals.ROOT_DIRECTORY = "test_directory__do_not_commit"
        globals.LANGUAGES_DIR = os.path.join(globals.ROOT_DIRECTORY, "languages")
        self.reset_token_endpoint = globals.API_BASE_URL + "test/"
        os.makedirs(globals.LANGUAGES_DIR, exist_ok=True)

    def tearDown(self):
        if os.path.exists(globals.ROOT_DIRECTORY):
            shutil.rmtree(globals.ROOT_DIRECTORY)

    def test_add_new_language(self):
        new_language = "Japanese"
        add_language(new_language)
        new_language_path = os.path.join(
            globals.LANGUAGES_DIR, f"{new_language.lower()}.json"
        )
        self.assertTrue(os.path.exists(new_language_path))

        with open(new_language_path, "r") as file:
            data = json.load(file)
        self.assertEqual(data, {})

        # clean up test
        os.remove(new_language_path)

    def test_add_word_language_exists(self):
        existing_language = "French"
        file_path = os.path.join(
            globals.LANGUAGES_DIR, f"{existing_language.lower()}.json"
        )

        # Create french translation file
        french_translations = {"tea": "thé", "hello": "bonjour"}
        with open(file_path, "w") as json_file:
            json.dump(french_translations, json_file, indent=4)

        data = get_json(file_path)
        self.assertEqual(len(data), 2)

        add_update_translated_word("French", "good", "bien")
        data = get_json(file_path)
        self.assertEqual(len(data), 3)
        self.assertEqual(data["good"], "bien")

    def test_update_word_language_exists(self):
        existing_language = "French"
        file_path = os.path.join(
            globals.LANGUAGES_DIR, f"{existing_language.lower()}.json"
        )

        french_translations = {"thanks": "should_change", "hello": "bonjour"}
        with open(file_path, "w") as json_file:
            json.dump(french_translations, json_file, indent=4)

        data = get_json(file_path)
        self.assertEqual(len(data), 2)

        add_update_translated_word("French", "thanks", "merc")
        data = get_json(file_path)
        self.assertEqual(len(data), 2)
        self.assertEqual(data["thanks"], "merc")

    @patch("builtins.print")
    def test_add_word_language_does_not_exist(self, mock_print):
        with self.assertRaises(SystemExit) as context:
            add_update_translated_word("NonExistentLanguage", "a", "b")
        self.assertTrue(context.exception.code, 1)

        mock_print.assert_called_once_with(
            "Error: Language 'NonExistentLanguage' does not exist. Add the language before adding a translation."
        )

    def test_delete_translation_success(self):
        language = "German"
        add_language(language)
        file_path = os.path.join(globals.LANGUAGES_DIR, f"{language.lower()}.json")

        initial_translations = {"goodbye": "auf Wiedersehen", "thank you": "danke"}
        with open(file_path, "w") as file:
            json.dump(initial_translations, file, indent=4)

        data = get_json(file_path)
        self.assertIn("goodbye", data)
        self.assertEqual(data["goodbye"], "auf Wiedersehen")

        delete_translation(language, "goodbye", "auf Wiedersehen")

        # verify deletion
        data = get_json(file_path)
        self.assertNotIn("goodbye", data)
        self.assertIn("thank you", data)

    @patch("builtins.print")
    def test_delete_translation_language_does_not_exist(self, mock_print):
        language = "Russian"
        original_word = "hello"
        translated_word = "привет"

        with self.assertRaises(SystemExit) as context:
            delete_translation(language, original_word, translated_word)
        self.assertEqual(context.exception.code, 1)

        mock_print.assert_called_once_with(
            f"Error: Language '{language}' does not exist."
        )

    def test_delete_translation_word_does_not_exist(self):
        language = "Chinese"
        add_language(language)
        file_path = os.path.join(globals.LANGUAGES_DIR, f"{language.lower()}.json")

        initial_translations = {"thank you": "谢谢"}
        with open(file_path, "w") as file:
            json.dump(initial_translations, file, indent=4)

        data = get_json(file_path)
        self.assertIn("thank you", data)
        self.assertNotIn("good morning", data)

        with patch("builtins.print") as mock_print, self.assertRaises(
            SystemExit
        ) as context:
            delete_translation(language, "good morning", "早上好")
        self.assertEqual(context.exception.code, 1)
        mock_print.assert_called_once_with(
            f"Error: Original word 'good morning' does not exist in language '{language}'."
        )

        # ensure existing translations remain unchanged
        data = get_json(file_path)
        self.assertIn("thank you", data)
        self.assertEqual(data["thank you"], "谢谢")

    def test_delete_translation_word_mismatch(self):
        language = "Korean"
        add_language(language)
        file_path = os.path.join(globals.LANGUAGES_DIR, f"{language.lower()}.json")

        initial_translations = {"welcome": "환영합니다"}
        with open(file_path, "w") as file:
            json.dump(initial_translations, file, indent=4)

        data = get_json(file_path)
        self.assertIn("welcome", data)
        self.assertEqual(data["welcome"], "환영합니다")

        with patch("builtins.print") as mock_print, self.assertRaises(
            SystemExit
        ) as context:
            delete_translation(language, "welcome", "환영해요")
        self.assertEqual(context.exception.code, 1)
        mock_print.assert_called_once_with(
            f"Error: Translated word for 'welcome' does not match '환영해요'."
        )

        # ensure existing translations remain unchanged
        data = get_json(file_path)
        self.assertIn("welcome", data)
        self.assertEqual(data["welcome"], "환영합니다")

    """
    Commenting out push and pull tests because they need the backend to be running.
    GitHub CI is not configured to start the backend before running tests.
    """

    # def test_pull_translations(self):
    #     # Set global token to test token (Note: test will fail if translations
    #     # tied token are modified)
    #     prev_token = globals.token.value
    #     test_token = "c84234c3-b507-4ed0-a6eb-8b10116cdef1"
    #     globals.token.value = test_token
    #
    #     # Initialize DiffingProcessor with test directory
    #     temp_dir_path = os.path.join(globals.LANGUAGES_DIR, "temp")
    #     diff_processor = DiffingProcessor(temp_dir_path)
    #     if os.path.exists(diff_processor.diff_state_root_dir):
    #         shutil.rmtree(diff_processor.diff_state_root_dir)
    #     diff_processor.setup()
    #
    #     # Create temporary directories to pull translations
    #     if os.path.exists(temp_dir_path):
    #         shutil.rmtree(temp_dir_path)
    #     os.mkdir(temp_dir_path)
    #
    #     # Copy test files into temp dir to test overwriting
    #     files_to_copy = ["spanish.json", "french.json"]
    #     for file_name in files_to_copy:
    #         curr_file_path = os.path.join(globals.LANGUAGES_DIR, file_name)
    #         new_file_path = os.path.join(temp_dir_path, file_name)
    #         shutil.copy(curr_file_path, new_file_path)
    #
    #     # Expected content after pulling from API
    #     expected_file_content = {
    #         "fr.json": {
    #             "hello": "bonjour"
    #         },
    #         "french.json": {
    #             "hello": "bonjour"
    #         },
    #         "spanish.json": {
    #             "hello": "hola",
    #             "bye": "chau",
    #             "what": "que",
    #             "como": "how",
    #             "codigo": "code"
    #         }
    #     }
    #
    #     pull_translations(write_directory=temp_dir_path)
    #     for file_name in os.listdir(temp_dir_path):
    #         file_path = os.path.join(temp_dir_path, file_name)
    #         file_content = get_json(file_path)
    #         self.assertEqual(file_content, expected_file_content[file_name])
    #
    #     # Cleanup
    #     shutil.rmtree(diff_processor.diff_state_root_dir)
    #     shutil.rmtree(temp_dir_path)
    #     globals.token.value = prev_token
    #
    # def test_push_translations(self):
    #     # Set global token to test token
    #     prev_token = globals.token.value
    #     test_token = "a373fc5e-5b65-463e-b89e-1a37706a69dd"
    #     globals.token.value = test_token
    #
    #     # Initialize DiffingProcessor with test directory
    #     temp_dir_path = os.path.join(globals.LANGUAGES_DIR, "temp")
    #     diff_processor = DiffingProcessor(temp_dir_path)
    #
    #     # Remove any persisting test data from previous tests (in case of a test failure)
    #     if os.path.exists(diff_processor.diff_state_root_dir):
    #         shutil.rmtree(diff_processor.diff_state_root_dir)
    #     if os.path.exists(temp_dir_path):
    #         shutil.rmtree(temp_dir_path)
    #     os.mkdir(temp_dir_path)
    #
    #     # Initialize with no translations in either state
    #     diff_processor.setup()
    #
    #     # Deletes all translations tied to test_token
    #     response = requests.delete(self.reset_token_endpoint, headers={'Token': test_token})
    #     self.assertTrue(response.ok)
    #
    #     # Copy files to push to API
    #     files_to_copy = ["spanish.json", "french.json"]
    #     for file_name in files_to_copy:
    #         curr_file_path = os.path.join(globals.LANGUAGES_DIR, file_name)
    #         new_file_path = os.path.join(temp_dir_path, file_name)
    #         shutil.copy(curr_file_path, new_file_path)
    #
    #     # Push changes, delete copied files, and pull
    #     push_translations(translations_dir=temp_dir_path)
    #     shutil.rmtree(temp_dir_path)
    #     os.mkdir(temp_dir_path)
    #     pull_translations(write_directory=temp_dir_path)
    #
    #     # Expected content after pulling from API (same content that was pushed)
    #     expected_file_content = {}
    #     for file_name in files_to_copy:
    #         copied_file_path = os.path.join(globals.LANGUAGES_DIR, file_name)
    #         expected_file_content[file_name] = get_json(copied_file_path)
    #
    #     pulled_files = os.listdir(temp_dir_path)
    #     self.assertEqual(len(pulled_files), 2)
    #     for file_name in os.listdir(temp_dir_path):
    #         file_path = os.path.join(temp_dir_path, file_name)
    #         file_content = get_json(file_path)
    #         self.assertEqual(file_content, expected_file_content[file_name])
    #
    #     # Cleanup
    #     shutil.rmtree(diff_processor.diff_state_root_dir)
    #     shutil.rmtree(temp_dir_path)
    #     globals.token.value = prev_token


if __name__ == "__main__":
    unittest.main()
