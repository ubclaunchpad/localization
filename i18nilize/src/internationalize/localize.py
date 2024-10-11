from src.internationalize.helpers import get_json
    
# Input:
#   - file_path: path of json file
#   - language: chosen language to translate to
#   - word: chosen word to translate
# Output: translated word based on chosen language
def get_translation(file_path, language, word):
    data = get_json(file_path)
    for translation in data["translations"]:
        if translation["language"] == language:
            new_word = translation.get(word)
            if (new_word == None):
                return f"'{word}' not found in {language}"
            return new_word
    return f"'{language}' not found"