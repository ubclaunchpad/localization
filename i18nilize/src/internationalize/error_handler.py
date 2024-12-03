import json
import os

"""
Error Handler Class
"""
class ErrorHandler():
    """
    Sets up the directory where the languages are located
    """
    def __init__(self, translations_dir):
        self.translations_dir = translations_dir

    """
    Verify each language file is valid
    """
    def verify_languages(self):
        """
        key: language containing an error
        value: error message
        """
        errors = {}

        all_language_files = os.listdir(self.translations_dir)

        for language_file in all_language_files:
            error = self.handle_error(language_file)
            if error != "":
                errors[language_file] = error
        
        return errors


    """
    Used to handle an error from a language
    Input: string: language_file (source of error), boolean: error_expected (is the error expected?)\
    Output: descriptive string about the error from the language file
    """
    def handle_error(self, language_file, error_expected=False):
        result = ""

        # Verify if file is invalid
        result = self.handle_invalid_file(language_file)
        if result != "":
            return result

        # Verify if any keys are invalid
        result = self.handle_invalid_keys(language_file)

        if result == "" and error_expected:
            raise Exception(f"expected error in {language_file} but no error was found")
        
        return result

    """
    Checks if given language is in an invalid file
    Output:
        - An empty string if there isn't any errors
        - A descriptive message about the error
    """
    def handle_invalid_file(self, language_file):
        language_location = os.path.join(self.translations_dir, language_file)
        try:
            with open(language_location, "r") as file:
                json.load(file)
        except json.JSONDecodeError as e:
            return "Invalid Language File, try fixing the json format."
        except Exception as e:
            print(f"Unexpected Error: {e}")
            raise e
        # return empty string if no error found
        return ""

    """
    Checks if given language contains any invalid keys
    Output:
        - An empty string if there aren't any errors
        - A descriptive message about the invalid key(s)
    """
    def handle_invalid_keys(self, language_file):
        language_location = os.path.join(self.translations_dir, language_file)
        language = {}
        try:
            with open(language_location, "r") as file:
                language = json.load(file)
            for key in language:
                if not isinstance(language[key], str):
                    return "Value is not a string."
                if not key.strip():
                    return "Key is empty."
        except Exception as e:
            print(f"Unexpected Error: {e}")
            raise e
        return ""