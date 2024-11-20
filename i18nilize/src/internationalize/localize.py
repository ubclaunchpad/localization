import json
import os
from src.internationalize.helpers import get_json


# NOTE: this is the old get_translation function - replace with the new one!!
def get_translation(file_path, language, word):
    # Input:
    #   - file_path: path of json file
    #   - language: chosen language to translate to
    #   - word: chosen word to translate
    # Output: translated word based on chosen language
    data = get_json(file_path)
    for translation in data["translations"]:
        if translation["language"] == language:
            new_word = translation.get(word)
            if (new_word is None):
                return f"'{word}' not found in {language}"
            return new_word
    return f"'{language}' not found"


class Localize:
    self.languages_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "languages")

    def __init__(self):
        self.translations_map = {}

    @classmethod
    def load_language(self, language):
        """
        Load the translation file for a specific language if not already loaded.
        """
        if language not in self.translations_map:
            file_path = os.path.join(self.languages_dir, f"{language}.json")
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    self.translations_map[language] = json.load(file)
            else:
                raise FileNotFoundError(f"Translations for {language} not found.")

    @classmethod
    def translate(self):
        """
        Get translation for a word in the specified language.
        """
        pass
