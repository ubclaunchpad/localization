import json
import os
import requests
from geocoder import ip
from geopy.geocoders import Nominatim
from babel.languages import get_official_languages
from . import globals

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

