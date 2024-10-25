import json

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

