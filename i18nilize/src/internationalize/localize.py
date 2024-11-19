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
    def __init__(self, languages_dir):
        self.languages_dir = languages_dir
        self.language_map = {}

    @classmethod
    def load_language(self):
        """Load the translation file for a specific language if not already loaded."""
        pass

    @classmethod
    def translate(self):
        """Get translation for a word in the specified language."""
        pass
