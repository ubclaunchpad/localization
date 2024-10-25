import json
import sys

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
    # filename = f"{language.lower()}.json"
    # file_path = os.path.join('i18nilize/src/internationalize/resources', filename)

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

# Adds/updates a translated word under the given language in the default JSON file
def add_update_translated_word(language, original_word, translated_word):
    data = get_json(DEFAULT_PATH)  
    translations = data.get('translations', [])

    language_exists = False
    for translation in translations:
        if translation.get('language') == language:
            language_exists = True
            translation[original_word] = translated_word

            with open(DEFAULT_PATH, 'w') as file:
                json.dump(data, file, indent=4)

            break

    if not language_exists:
        print(f"Error: Language '{language}' does not exist. Add the language before adding a translation.")
        sys.exit(1)  

# Input: 
#   - file_path: path of json file
# Output: Token in json file
def get_token(file_path):
    data = get_json(file_path)
    token = data["Token"]
    return token


# Input: a JSON object
# Output: None, but creates a local JSON file containing the object
def create_json(json_object):
    with open("src/internationalize/jsonFile/translations.json", "w") as outfile:
        outfile.write(json_object)

# Input: None (for now)
# Output: None, but creates a local JSON file containing translations
def generate_file():
    file_content = {
        "Token": "85124f79-0829-4b80-8b5c-d52700d86e46",
        "translations" : [{
				"language": "French",
				"hello": "bonjour",
				"No": "Non",
				"Why": "pourquoi",
			},
			{
				"language": "Spanish",
				"hello": "Hola",
			},
		]
    }

    # transforms the dictionary object above into a JSON object
    json_object = json.dumps(file_content, indent=4)
    create_json(json_object)

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

