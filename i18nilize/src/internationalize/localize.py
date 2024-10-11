import json

def get_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Input: 
#   - file_path: path of json file
# Output: Token in json file
def get_token(file_path):
    data = get_json(file_path)
    token = data["Token"]
    return token
    
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