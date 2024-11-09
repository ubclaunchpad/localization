import os
import hashlib
import json
from dirsync import sync

# Diffing Processor Class
class DiffingProcessor():
    def __init__(self, curr_translations_dir):
        self.old_translations_root_dir = "old_translations"
        self.old_translation_files_dir = os.path.join(self.old_translations_root_dir, "translations")
        self.metadata_file_dir = os.path.join(self.old_translations_root_dir, "metadata.json")
        self.curr_translation_files_dir = curr_translations_dir

    """
    Initializes the old state of translations when package is first installed.
    """
    def setup(self):
        try:
            os.mkdir(self.old_translations_root_dir)
            os.mkdir(self.old_translation_files_dir)
            with open(self.metadata_file_dir, "w") as outfile:
                json.dump({}, outfile)

            # sync folders
            self.sync_translations()

            # Compute all file hashes and store hashes in metadata
            all_files = os.listdir(self.old_translation_files_dir)
            all_file_hashes = compute_hashes(self.old_translation_files_dir)
            self.update_metadata(all_files, all_file_hashes)
        except FileExistsError:
            print(f"Old translations directory has already been created.")
        except PermissionError:
            print(f"Permission denied: unable to setup old translation state.")
        except Exception as e:
            print(f"An exception occured: {e}")

    """
    Updates translation files with new changes and updates hashes in metadata.
    """
    def update_to_current_state(self, changed_files_list, hash_dict):
        self.update_metadata(changed_files_list, hash_dict)
        self.sync_translations()

    """
    Gets differences between old and new translations and sets new state
    of translations.
    """
    def diff(self):
        # Get hashes of current translation files (current state)
        new_hashes_dict = self.compute_hashes(self.curr_translation_files_dir)

        # Get files that changed by comparing hashes
        changed_files_list = []

        # Perform diffing on files that changed and get added, modified, deleted

        # Update metadata and old state
        self.update_to_current_state(changed_files_list, new_hashes_dict)

        # return added, modified, deleted   
        pass

    def update_metadata(self, changed_files_list, hash_dict):
        metadata = {}
        with open(self.metadata_file_dir) as file:
            metadata = json.load(file)
        
        for file_name in changed_files_list:
            file_name_no_ext = file_name.split(".")[0]
            metadata[file_name_no_ext] = hash_dict[file_name_no_ext]

        with open(self.metadata_file_dir, "w") as outfile:
            json.dump(hash_dict, outfile)

    def sync_translations(self):
        sync(self.curr_translation_files_dir, self.old_translation_files_dir, "sync", purge=True)


"""
Helper functions    
"""

def compute_hash(file_content):
    hash = hashlib.sha256()
    hash.update(file_content)
    return hash.hexdigest()

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