import os
import hashlib
import json
from dirsync import sync

OLD_TRANSLATIONS_ROOT_DIR = "old_translations"
OLD_TRANSLATIONS_FILES_DIR = OLD_TRANSLATIONS_ROOT_DIR + "/translations"
METADATA_FILE_DIR = OLD_TRANSLATIONS_ROOT_DIR + "/metadata.json"
NEW_TRANSLATIONS_FILES_DIR = "delete_after"

"""
On package setup, generates old state of translation files.
"""
def setup():
    try:
        os.mkdir(OLD_TRANSLATIONS_ROOT_DIR)
        os.mkdir(OLD_TRANSLATIONS_ROOT_DIR + "/translations")
        with open(METADATA_FILE_DIR, "w") as outfile:
            json.dump({}, outfile)
        sync(NEW_TRANSLATIONS_FILES_DIR, OLD_TRANSLATIONS_FILES_DIR, "sync", purge=True)

        # Compute all file hashes and store hashes in metadata
        files = os.listdir(OLD_TRANSLATIONS_FILES_DIR)
        update_hashes(files)
    except FileExistsError:
        print(f"Old translations directory has already been created.")
    except PermissionError:
        print(f"Permission denied: unable to setup old translation state.")
    except Exception as e:
        print(f"An exception occured: {e}")

def compute_hash(file_content):
    hash = hashlib.sha256()
    hash.update(file_content)
    return hash.hexdigest()

def update_hashes(changed_files_list):
    hash_dict = {}

    with open(METADATA_FILE_DIR) as file:
        hash_dict = json.load(file)

    for file_name in changed_files_list:
        path = OLD_TRANSLATIONS_FILES_DIR + "/" + file_name
        
        # Read file as byte buffer
        with open(path, "rb") as file:
            file_name_no_ext = file_name.split(".")
            file_content = file.read()
            file_hash = compute_hash(file_content)
            hash_dict[file_name_no_ext[0]] = file_hash

    with open(METADATA_FILE_DIR, "w") as outfile:
        json.dump(hash_dict, outfile)

"""
Initializes new old state files and metadata if a new translation
file is added.
"""
def update_old_state():
    pass

"""
Gets differences between old and new states of changed translation
files.
"""
def get_diff():
    pass

"""
Updates old file hashes and updates old state of changed files.
"""
def update_metadata():
    pass

"""
Returns an array of added, modified, and deleted translations
between two sets of translations.
"""
def compare_files(oldTranslations, newTranslations):
    pass

"""
Compares hashes of old and new translation files.
"""
def get_changed_files():
    pass
