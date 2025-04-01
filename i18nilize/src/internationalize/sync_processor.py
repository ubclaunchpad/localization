import json
import os

import requests

from .diffing_processor import DiffingProcessor

from . import globals
from .api_helpers import has_writer_permissions

"""
Pulls all translations assigned to the microservices' token
and overwrites all language files to sync translations.
"""


def pull_translations():
    token = globals.token.value
    diff_processor = DiffingProcessor(globals.LANGUAGES_DIR)

    try:
        all_translations = requests.get(
            globals.PULL_TRANSLATIONS_ENDPOINT, headers={"Token": token}
        )
    except Exception as e:
        print("Error: Could not fetch translations from database.", e)
        return

    # Overwrite all translation files
    all_transactions_dict = all_translations.json()
    for language, translations in all_transactions_dict.items():
        file_name = f"{language}.json"
        curr_file_path = os.path.join(globals.LANGUAGES_DIR, file_name)
        with open(curr_file_path, "w+") as file:
            json.dump(translations, file, indent=4)

    diff_processor.update_to_current_state()
    print("Pulled all translations from the database.")


"""
Push all local translations to the API.
"""


def push_translations():
    token = globals.token.value
    ms_token = globals.ms_token.value

    # make sure current microservice token has writer permissions
    if not has_writer_permissions(ms_token):
        error_msg = "Error: this microservice does not have writer permissions. Use the CLI to change writer permissions and try again."
        print(error_msg)
        return

    diff_processor = DiffingProcessor(translations_dir)
    changed_translations = diff_processor.get_changed_translations()

    for language in changed_translations:
        created = changed_translations[language]["created"]
        modified = changed_translations[language]["modified"]
        deleted = changed_translations[language]["deleted"]

        # Post a new entry for each new translation
        for original_word in created:
            try:
                requests.post(
                    globals.PUSH_TRANSLATIONS_ENDPOINT,
                    headers={"Token": token},
                    params={
                        "language": language,
                        original_word: created[original_word],
                    },
                )
            except Exception as e:
                print("Error: Could not create translation.", e)

        # Patch the appropriate entry for each modified translation
        for original_word in modified:
            try:
                requests.patch(
                    globals.PUSH_TRANSLATIONS_ENDPOINT,
                    headers={"Token": token},
                    params={
                        "language": language,
                        original_word: modified[original_word],
                    },
                )
            except Exception as e:
                print("Error: Could not patch translation.", e)

        # Delete the appropriate entry for each deleted translation
        for original_word in deleted:
            try:
                requests.delete(
                    globals.PUSH_TRANSLATIONS_ENDPOINT,
                    headers={"Token": token},
                    params={
                        "language": language,
                        original_word: deleted[original_word],
                    },
                )
            except Exception as e:
                print("Error: Could not delete translation.", e)

    diff_processor.update_to_current_state()
    print(f"Pushed all local translations to the database.")
