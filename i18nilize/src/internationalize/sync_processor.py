import requests, os, json
from . import globals
from src.internationalize.diffing_processor import DiffingProcessor

"""
Pulls all translations assigned to the microservices' token
and overwrites all language files to sync translations.
"""
def pull_translations(write_directory=globals.LANGUAGES_DIR):
    token = globals.token.value
    diff_processor = DiffingProcessor(write_directory)

    try:
        all_translations = requests.get(globals.PULL_TRANSLATIONS_ENDPOINT, headers={'Token': token})
    except Exception as e:
        print("Error: Could not fetch translations from database.", e)

    # Overwrite all translation files
    all_transactions_dict = all_translations.json()
    for language, translations in all_transactions_dict.items():
        file_name = f"{language}.json"
        curr_file_path = os.path.join(write_directory, file_name)
        with open(curr_file_path, "w+") as file:
            json.dump(translations, file, indent=4)

    diff_processor.update_to_current_state()
    print(f"Pulled all translations from the database.")

"""
Push all local translations to the API.
"""
def push_translations(translations_dir=globals.LANGUAGES_DIR):
    token = globals.token.value
    diff_processor = DiffingProcessor(translations_dir)
    changed_translations = diff_processor.get_changed_translations()

    for language in changed_translations:
        created = changed_translations[language]["created"]
        modified = changed_translations[language]["modified"]
        deleted = changed_translations[language]["deleted"]

        # Post a new entry for each new translation
        for original_word in created:
            try:
                response = requests.post(globals.PUSH_TRANSLATIONS_ENDPOINT, headers={'Token': token}, 
                                         params={'language': language, original_word: created[original_word]})
            except Exception as e:
                print("Error: Could not create translation.", e)
        
        # Patch the appropriate entry for each modified translation
        for original_word in modified:
            try:
                response = requests.patch(globals.PUSH_TRANSLATIONS_ENDPOINT, headers={'Token': token}, 
                                         params={'language': language, original_word: modified[original_word]})
            except Exception as e:
                print("Error: Could not patch translation.", e)

        # Delete the appropriate entry for each deleted translation
        for original_word in deleted:
            try:
                response = requests.delete(globals.PUSH_TRANSLATIONS_ENDPOINT, headers={'Token': token}, 
                                         params={'language': language, original_word: deleted[original_word]})
            except Exception as e:
                print("Error: Could not delete translation.", e)

    print(f"Pushed all translations from the database.")
