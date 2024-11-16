import json
import sys
import os
import requests

DEFAULT_PATH = 'src/internationalize/resources/languages.json' # to be removed after refactoring
LANGUAGES_DIR = 'src/internationalize/languages'

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

# Adds a json file corresponding to the added language
def add_language(language):
    os.makedirs(LANGUAGES_DIR, exist_ok=True)
    file_path = os.path.join(LANGUAGES_DIR, f"{language.lower()}.json")

    if os.path.exists(file_path):
        return
    
    initial_content = {}
    with open(file_path, 'w') as file:
        json.dump(initial_content, file, indent=4)
    print(f"Language added.")

# Adds/updates a translated word under the given language in the default JSON file
def add_update_translated_word(language, original_word, translated_word):
    file_path = os.path.join(LANGUAGES_DIR, f"{language.lower()}.json")

    if not os.path.exists(file_path):
        print(f"Error: Language '{language}' does not exist. Add the language before adding a translation.")
        sys.exit(1)
    
    data = get_json(file_path)

    data[original_word] = translated_word
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"{original_word}: {translated_word} added to translations.")

# Deletes a translated word for the given language
def delete_translation(language, original_word, translated_word):
    file_path = os.path.join(LANGUAGES_DIR, f"{language.lower()}.json")

    if not os.path.exists(file_path):
        print(f"Error: Language '{language}' does not exist.")
        sys.exit(1)

    data = get_json(file_path)

    if original_word not in data:
        print(f"Error: Original word '{original_word}' does not exist in language '{language}'.")
        sys.exit(1)

    if data[original_word] != translated_word:
        print(f"Error: Translated word for '{original_word}' does not match '{translated_word}'.")
        sys.exit(1)

    del data[original_word]
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Translation for '{original_word}' deleted successfully from language '{language}'.")

# Input: 
#   - file_path: path of json file
# Output: Token in json file
def get_token(file_path):
    data = get_json(file_path)
    token = data["Token"]
    return token


# Input: a JSON object
# Output: None, but creates a local JSON file containing the object
def create_json(json_object, language):
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'languages', f'{language}.json')
    with open(file_path, 'w') as outfile:
        outfile.write(json_object)

# Input: language
# Output: None, but creates a local JSON file containing translations
def generate_file(language, token):
    url = 'http://localhost:8000/api/translations'
    params = {'language': language}
    headers = {'token': token}
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        print(f'Error: {response.status_code}.', response.json()['error'])
        return
    
    file_content = response.json() 

    # transforms the dictionary object above into a JSON object
    json_object = json.dumps(file_content, indent=4)
    create_json(json_object, language)

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

