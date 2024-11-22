import os
import hashlib
import json
from dirsync import sync
from src.internationalize.helpers import compute_hash, compute_hashes, read_json_file

JSON_EXTENSION = ".json"

TYPE = "type"
CREATED = "created"
MODIFIED = "modified"
DELETED = "deleted"

"""
Diffing Processor Class
"""
class DiffingProcessor():
    def __init__(self, curr_translations_dir):
        self.diff_state_root_dir = "diff_state"
        self.diff_state_files_dir = os.path.join(self.diff_state_root_dir, "translations")
        self.metadata_file_dir = os.path.join(self.diff_state_root_dir, "metadata.json")
        self.curr_translation_files_dir = curr_translations_dir

    """
    Initializes the old state of translations when package is first installed.
    """
    def setup(self):
        try:
            os.mkdir(self.diff_state_root_dir)
            os.mkdir(self.diff_state_files_dir)
            with open(self.metadata_file_dir, "w") as outfile:
                json.dump({}, outfile)

            # sync folders
            self.sync_translations()

            # Compute all file hashes and store hashes in metadata
            all_files = os.listdir(self.diff_state_files_dir)
            all_file_hashes = compute_hashes(self.diff_state_files_dir)
            self.update_metadata(all_file_hashes)
        except FileExistsError:
            print(f"Old translations directory has already been created.")
        except PermissionError:
            print(f"Permission denied: unable to setup old translation state.")
        except Exception as e:
            print(f"An exception occured: {e}")

    """
    Updates translation files with new changes and updates hashes in metadata.
    """
    def update_to_current_state(self, hash_dict):
        self.update_metadata(hash_dict)
        self.sync_translations()

    def update_metadata(self, hash_dict):
        with open(self.metadata_file_dir, "w") as outfile:
            json.dump(hash_dict, outfile)

    def sync_translations(self):
        sync(self.curr_translation_files_dir, self.diff_state_files_dir, "sync", purge=True)

    """
    Returns a list of all the files that have been modified
    """
    def get_changed_files(self):
        # Initialize hashes
        current_hashes = compute_hashes(self.curr_translation_files_dir)

        with open(self.metadata_file_dir, "r") as file:
            original_hashes = json.load(file)

        changed_files = {
            CREATED: [],
            MODIFIED: [],
            DELETED: []
        }

        # Find any languages that were either modified or added the current PIP package
        for language, current_hash in current_hashes.items():
            file_name = language + JSON_EXTENSION
            if language not in original_hashes:
                changed_files[CREATED].append(file_name)
            elif original_hashes[language] != current_hash:
                changed_files[MODIFIED].append(file_name)

        # Find files that were removed from PIP package
        for language in original_hashes:
            file_name = language + JSON_EXTENSION
            if language not in current_hashes:
                changed_files[DELETED].append(file_name)

        return changed_files

    """
    Gets differences between old and new translations
    """
    def get_changed_translations(self):
        changed_files = self.get_changed_files()
        changed_translations = {}

        for type, file_names in changed_files.items():
            for file_name in file_names:
                language = file_name.split(".")[0]
                changed_translations[language] = self.__initialize_changed_template(type)

                # fetch modified translations
                if type == MODIFIED:
                    changed_translations[language] = self.compare_language(file_name, changed_translations[language])

                if type == CREATED:
                    changed_translations[language] = self.add_language(file_name, changed_translations[language])
        
        return changed_translations

    """
    Gets differences between old and new translations for one language
    """
    def compare_language(self, file_name, changed_translations):        
        original_language_location = os.path.join(self.diff_state_files_dir, file_name)
        current_language_location = os.path.join(self.curr_translation_files_dir, file_name)

        original_language = read_json_file(original_language_location)
        current_language = read_json_file(current_language_location)

        # find modified and newly added translations
        for word, translation in current_language.items():
            if word not in original_language:
                changed_translations[CREATED][word] = translation
            elif translation != original_language[word]:
                changed_translations[MODIFIED][word] = translation

        # find removed translations
        for word, translation in original_language.items():
            if word not in current_language:
                changed_translations[DELETED][word] = translation

        return changed_translations
    
    def add_language(self, file_name, changed_translations):
        current_language_location = os.path.join(self.curr_translation_files_dir, file_name)
        current_language = read_json_file(current_language_location)

        for word, translation in current_language.items():
            changed_translations[CREATED][word] = translation

        return changed_translations
    
    """
    Create empty JSON template to show modifications from a language
    """
    def __initialize_changed_template(self, type):
        changed_translations = {}
        changed_translations[TYPE] = type
        changed_translations[CREATED] = {}
        changed_translations[MODIFIED] = {}
        changed_translations[DELETED] = {}
        return changed_translations
