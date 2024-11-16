import json
import os
import shutil
from src.internationalize.diffing_processor import read_json_file

class DiffingTestUtil():
    def __init__(self, test_directory):
        self.test_directory = test_directory

    """
    Initialize test data for diffing algorithm
    """
    def initialize_test_data(self, directory):
        self.clear_test_data()
        os.mkdir(self.test_directory)

        # this will create all the language files
        self.bulk_modify_test_data(directory)


    """
    Modify test data with new language files
    Doesn't support removing a language
    """
    def bulk_modify_test_data(self, directory):
        file_names = os.listdir(directory)
        for file_name in file_names:
            language_data = read_json_file(os.path.join(directory, file_name))
            with open(os.path.join(self.test_directory, file_name), 'w') as json_file:
                json.dump(language_data, json_file, indent=4)

    def clear_test_data(self):
        if os.path.exists(self.test_directory):
            shutil.rmtree(self.test_directory)