import json

# Should this be removed?
DEFAULT_PATH = 'i18nilize/src/internationalize/resources/languages.json'

# Function to parse json file, given its path
def get_json(file_path):
    try:
    # open file and parse
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("File not found")
        raise FileNotFoundError
    except json.JSONDecodeError as e:
        print("JSON Decoding Error")
        raise e
    except Exception as e:
        print(f"Error: {e}")
        raise e
    return data

# Adds a language to the default JSON file
def add_language(language):
    data = get_json(DEFAULT_PATH)
    translations = data.get('translations', [])

    # Check if the language already exists in the translations list
    if not any(t.get('language') == language for t in translations):
        # Add new language as a dictionary in the list
        new_language = {"language": language}
        translations.append(new_language)
        data['translations'] = translations

        # open and write
        with open(DEFAULT_PATH, 'w') as file:
            json.dump(data, file, indent=4)

# Input: 
#   - file_path: path of json file
# Output: Token in json file
def get_token(file_path):
    data = get_json(file_path)
    token = data["Token"]
    return token

# make hashmap from translations
def make_translation_map(data):
    translations_map = {}
    for translation in data.get('translations', []):
        language = translation.get('language')
        if language:
            translations_map[language] = translation
    return translations_map

# get translations from hashmap given the language
def get_translation(translations_map, language):
    return translations_map.get(language, "Translation not found")