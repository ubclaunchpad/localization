import json
import os

from . import globals

class Localize:
    languages_dir = globals.LANGUAGES_DIR
    translations_map = {}

    @classmethod
    def load_language(cls, language):
        """
        Load the translation file for a specific language if not already loaded.
        """
        if language not in cls.translations_map:
            file_path = os.path.join(cls.languages_dir, f"{language}.json")
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    cls.translations_map[language] = json.load(file)
            else:
                raise FileNotFoundError(f"Translations for {language} not found.")

    @classmethod
    def translate(cls, word, language):
        """
        Get translation for a word in the specified language.
        """
        cls.load_language(language)
        return cls.translations_map[language].get(word, f"Translation for {word} not found")
