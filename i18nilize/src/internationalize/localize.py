import json

def getJson(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Input: 
#   - file_path: path of json file
# Output: Token in json file
def getToken(file_path):
    data = getJson(file_path)
    token = data["Token"]
    return token
    
# Input:
#   - file_path: path of json file
#   - language: chosen language to translate to
#   - word: chosen word to translate
# Output: translated word based on chosen language
def getTranslation(file_path, language, word):
    data = getJson(file_path)
    for translation in data["translations"]:
        if translation["language"] == language:
            new_word = translation.get(word)
            if (new_word == None):
                return f"'{word}' not found in {language}"
            return new_word
    return f"'{language}' not found"