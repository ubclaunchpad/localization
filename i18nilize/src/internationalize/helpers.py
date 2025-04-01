import json
import sys
import os
import hashlib
import requests
from . import globals
from src.internationalize.error_handler import ErrorHandler

# Function to parse json file, given its path
def get_json(file_path):
    try:
    # open file and parse
        with open(file_path, 'r', encoding='utf8') as file:
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
    os.makedirs(globals.LANGUAGES_DIR, exist_ok=True)
    file_path = os.path.join(globals.LANGUAGES_DIR, f"{language.lower()}.json")

    if os.path.exists(file_path):
        return
    
    initial_content = {}
    with open(file_path, 'w') as file:
        json.dump(initial_content, file, indent=4)
    print(f"Language added.")

# Adds/updates a translated word under the given language in the default JSON file
def add_update_translated_word(language, original_word, translated_word):
    file_path = os.path.join(globals.LANGUAGES_DIR, f"{language.lower()}.json")
    handler = ErrorHandler(globals.LANGUAGES_DIR)
    
    if not os.path.exists(file_path):
        print(f"Error: Language '{language}' does not exist. Add the language before adding a translation.")
        sys.exit(1)
    if not original_word.strip():
        print("Error: Original word cannot be empty or contain only whitespace.")
        sys.exit(1)
    if not translated_word.strip():
        print("Error: Translated word cannot be empty or contain only whitespace.")
        sys.exit(1)
    try:
        data = get_json(file_path)
    except json.JSONDecodeError as e:
        result = handler.handle_error(f"{language.lower()}.json", True)
        sys.exit(1)
    
    result = handler.handle_error(f"{language.lower()}.json", True)
    if (result == "Key is empty or contains only whitespace."):
        print(result)
        sys.exit(1)
    elif (result != ""):
        print(result)
        sys.exit(1)
    data[original_word] = translated_word
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"{original_word}: {translated_word} added to translations.")

# Deletes a translated word for the given language
def delete_translation(language, original_word, translated_word):
    file_path = os.path.join(globals.LANGUAGES_DIR, f"{language.lower()}.json")
    handler = ErrorHandler(globals.LANGUAGES_DIR)
    if not os.path.exists(file_path):
        print(f"Error: Language '{language}' does not exist.")
        sys.exit(1)
    try:
        data = get_json(file_path)
    except json.JSONDecodeError as e:
        result = handler.handle_error(f"{language.lower()}.json", True)
        sys.exit(1)
    
    result = handler.handle_error(f"{language.lower()}.json", True)
    if (result == "Key is empty or contains only whitespace."):
        print(result)
        sys.exit(1)
    elif (result != ""):
        print(result)
        sys.exit(1)

    if not original_word.strip():
        print("Error: Original word cannot be empty or contain only whitespace.")
        sys.exit(1)

    if not translated_word.strip():
        print("Error: Translated word cannot be empty or contain only whitespace.")
        sys.exit(1)

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

# Input: None
# Output: Default language based on user's IP address
def get_default_language():
    # get user's coordinates based on IP address
    g = ip('me')
    coord = str(g.latlng[0]) + ", " + str(g.latlng[1])

    # convert coordinates to country code
    geolocator = Nominatim(user_agent="localization_launchpad")
    location = geolocator.reverse(coord, exactly_one=True)
    address = location.raw['address']
    country_code = address["country_code"]

    # pick the first (most popular) language
    return get_official_languages(country_code)[0]

# Input: language
# Output: None, but creates a local JSON file containing translations
def generate_file(language, token):
    if not language:
        language = get_default_language()
    url = globals.TRANSLATIONS_ENDPOINT
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

# assign group token
def assign_token(token):
    globals.token = token
    print("Group token successfully set to : ", globals.token)
    
# fetch group token 
def fetch_token():
    print("Group token is : ", globals.token)
    return globals.token

"""
Computes 256-bit hash for given content
"""
def compute_hash(file_content):
    hash = hashlib.sha256()
    hash.update(file_content)
    return hash.hexdigest()

"""
Computes hashes for all files in a directory
"""
def compute_hashes(directory):
    hash_dict = {}
    files = os.listdir(directory)
    for file_name in files:
        path = directory + "/" + file_name
        
        # Read file as byte buffer for hashing
        with open(path, "rb") as file:
            file_name_no_ext = file_name.split(".")[0]
            file_content = file.read()
            file_hash = compute_hash(file_content)
            hash_dict[file_name_no_ext] = file_hash

    return hash_dict

"""
Reads a file given the directory and returns json object
Expects file to be in json format
"""
def read_json_file(directory):
    try:
        with open(directory, "r") as file:
            json_object = json.load(file)
            return json_object
    except FileNotFoundError:
        print(f"File not found: {directory}")
        raise
    except IOError:
        print(f"An error occurred while trying to read the file: {directory}")
        raise
    except Exception as e:
        print(f"An exception occured: {e}") 
