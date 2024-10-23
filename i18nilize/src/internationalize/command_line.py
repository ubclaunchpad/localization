#from src.internationalize.helpers import add_language
import json
import argparse

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

# Get rid of the hard coded path
def add_language(language):
    data = get_json('i18nilize/src/internationalize/resources/languages.json')
    translations = data.get('translations', [])

    # Check if the language already exists in the translations list
    if not any(t.get('language') == language for t in translations):
        # Add new language as a dictionary in the list
        new_language = {"language": language}
        translations.append(new_language)
        data['translations'] = translations

        with open('i18nilize/src/internationalize/resources/languages.json', 'w') as file:
            json.dump(data, file)
        print("Language added!")
    else:
        print("Language is already added.")

def cli():
    parser = argparse.ArgumentParser(description="internationalization for translation")
    subparsers = parser.add_subparsers(dest='command')

    # sub parser for add_language
    add_lang_parser = subparsers.add_parser('add-language')
    add_lang_parser.add_argument('language')

    args = parser.parse_args()

    if args.command == 'add-language':
        add_language(args.language)
    else:
        print("Invalid command")

cli()