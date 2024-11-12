from django.db import transaction
from ..models import Translation

"""
Utility functions for translation file processing.
"""


def validate_translations_data(translations_data):
    """
    Light validation of translation file structure and format
    """
    if "translations" not in translations_data:
        return False

    for translations in translations_data["translations"]:
        if "language" not in translations:
            return False

        for key, value in translations.items():
            if not isinstance(key, str) or not isinstance(value, str):
                return False

    return True


def get_new_translations(translations_data, token):
    """
    Returns a set of translations to add to the database. If any translation already
    exists and is being updated, returns False (use PATCH endpoint to make updates instead).
    """
    translations_set, languages_set = extract_translations(translations_data)
    existing_translations = fetch_existing_translations(token, translations_set, languages_set)
    return get_post_translations(translations_set, existing_translations)


def get_updated_translations(translations_data, token):
    """
    Returns a set of translations to update in the database. If there are any new translations
    in the translations list, returns False (use POST endpoint to make new translations instead).
    """
    translations_set, languages_set = extract_translations(translations_data)
    existing_translations = fetch_existing_translations(token, translations_set, languages_set)
    return get_patch_translations(translations_set, existing_translations)


def extract_translations(translations_data):
    """
    Extracts translations from the request and returns sets of translations and languages.
    """
    translations_set = set()
    languages_set = set()
    for translations in translations_data["translations"]:
        language = translations["language"]
        languages_set.add(language)

        for original_word, translated_word in translations.items():
            if original_word == "language":
                continue
            translations_set.add((original_word, translated_word, language))

    return translations_set, languages_set


def fetch_existing_translations(token, translations_set, languages_set):
    """
    Fetches existing translations from database in bulk to reduce number of queries.
    """
    existing_translations = {
        (t.original_word, t.language): t.translated_word

        for t in Translation.objects.filter(
            token=token,
            language__in=list(languages_set),
            original_word__in=[original_word for original_word, _, _ in translations_set],
        )
    }
    return existing_translations


def get_post_translations(translations_set, existing_translations):
    """
    Compares translations received in request with translations in database.
    If a translation already exists and is being updated, return False.
    Otherwise, returns a list of new translations to add to database.
    """
    new_translations = []
    for original_word, translated_word, language in translations_set:
        key = (original_word, language)
        if key in existing_translations:
            if existing_translations[key] == translated_word:
                continue
            # Translation already exists and is being updated
            return False
        else:
            new_translations.append((original_word, translated_word, language))
    return new_translations


def get_patch_translations(translations_set, existing_translations):
    """
    Compares translations received in request with translations in database.
    If a translation already exists and is being updated, return False.
    Otherwise, returns a list of new translations to add to database.
    """
    new_translations = []

    for original_word, translated_word, language in translations_set:
        key = (original_word, language)
        if key in existing_translations:
            if existing_translations[key] != translated_word:
                new_translations.append((original_word, translated_word, language))
        else:
            return False

    return new_translations


def bulk_create_translations(token, new_translations):
    """
    Adds new translations to the database with an atomic transaction.
    If any addition fails, it will rollback all previous additions i.e database
    will be unchanged.
    """
    bulk_translations = [
        Translation(
            token=token,
            original_word=original_word,
            translated_word=translated_word,
            language=language,
        )
        for original_word, translated_word, language in new_translations
    ]
    try:
        with transaction.atomic():
            Translation.objects.bulk_create(bulk_translations)
        return True, len(bulk_translations)
    except Exception as e:
        print(e)
        return False, 0


def bulk_update_translations(token, updated_translations):
    """
    Update translations in the database with an atomic transaction.
    Rollback previous updates if any fail.
    """
    try:
        with transaction.atomic():
            for original_word, translated_word, language in updated_translations:
                row = Translation.objects.get(token=token, original_word=original_word, language=language)
                row.translated_word = translated_word
                row.save()

        return True, len(updated_translations)
    except Exception as e:
        print(e)
        return False, 0

def get_translations_by_language(language, token):
    """
    Return all translations for the given language as a dictionary.
    """
    translations = Translation.objects.filter(language=language, token=token)

    translations_dict = {
        translation.original_word: translation.translated_word 
        for translation in translations
    }
    return translations_dict