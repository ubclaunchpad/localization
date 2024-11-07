import os
import hashlib
import json
from dirsync import sync

OLD_TRANSLATIONS_ROOT_DIR = "old_translations"
OLD_TRANSLATION_FILES_DIR = OLD_TRANSLATIONS_ROOT_DIR + "/translations"
METADATA_FILE_DIR = OLD_TRANSLATIONS_ROOT_DIR + "/metadata.json"
CURR_TRANSLATION_FILES_DIR = "delete_after"

"""
Initializes the old state of translations when package is first installed.
"""
def setup():
    try:
        os.mkdir(OLD_TRANSLATIONS_ROOT_DIR)
        os.mkdir(OLD_TRANSLATION_FILES_DIR)
        with open(METADATA_FILE_DIR, "w") as outfile:
            json.dump({}, outfile)
        sync_translations()

        # Compute all file hashes and store hashes in metadata
        all_files = os.listdir(OLD_TRANSLATION_FILES_DIR)
        all_file_hashes = compute_hashes(OLD_TRANSLATION_FILES_DIR)
        update_metadata(all_files, all_file_hashes)
    except FileExistsError:
        print(f"Old translations directory has already been created.")
    except PermissionError:
        print(f"Permission denied: unable to setup old translation state.")
    except Exception as e:
        print(f"An exception occured: {e}")

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

def compute_hash(file_content):
    hash = hashlib.sha256()
    hash.update(file_content)
    return hash.hexdigest()

def update_metadata(changed_files_list, hash_dict):
    metadata = {}
    with open(METADATA_FILE_DIR) as file:
        metadata = json.load(file)
    
    for file_name in changed_files_list:
        file_name_no_ext = file_name.split(".")[0]
        metadata[file_name_no_ext] = hash_dict[file_name_no_ext]

    with open(METADATA_FILE_DIR, "w") as outfile:
        json.dump(hash_dict, outfile)

def sync_translations():
    sync(CURR_TRANSLATION_FILES_DIR, OLD_TRANSLATION_FILES_DIR, "sync", purge=True)

"""
Updates translation files with new changes and updates hashes in metadata.
"""
def update_to_current_state(changed_files_list, hash_dict):
    update_metadata(changed_files_list, hash_dict)
    sync_translations()

"""
Gets differences between old and new translations and sets new state
of translations.
"""
def diff():
    # Get hashes of current translation files (current state)
    new_hashes_dict = compute_hashes(CURR_TRANSLATION_FILES_DIR)

    # Get files that changed by comparing hashes
    changed_files_list = []

    # Perform diffing on files that changed and get added, modified, deleted

    # Update metadata and old state
    update_to_current_state(changed_files_list, new_hashes_dict)

    # return added, modified, deleted   
    pass
