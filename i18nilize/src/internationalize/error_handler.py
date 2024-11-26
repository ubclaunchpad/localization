import os

"""
Error Handler Class
"""
class ErrorHandler():
    """
    Sets up the directory where the languages are located
    """
    def __init__(self, translations_dir):
        self.translations_dif = translations_dir

    """
    Verify each language file is valid
    """
    def verify_languages(self):
        """
        key: language containing an error
        value: error message
        """
        errors = {}

        all_languages = os.listdir(self.translations_dif)

        for language in all_languages:
            error = self.handle_error(language, False)
            if error != "":
                errors[language] = error
        
        return errors


    """
    Used to handle an error from a language
    Input: string: language_file (source of error), boolean: error_expected (is the error expected?)\
    Output: descriptive string about the error from the language file
    """
    def handle_error(self, language, error_expected):
        result = ""

        # Verify if file is invalid
        result = self.handle_invalid_file(language)
        if result != "":
            return result

        # Verify if any keys are invalid
        result = self.handle_invalid_keys(language)

        if result == "" and error_expected:
            raise Exception(f"expected error in {language} but no error was found")
        
        return result

    """
    Checks if given language is in an invalid file
    Output:
        - An empty string if there isn't any errors
        - A descriptive message about the error
    """
    def handle_invalid_file(self, language):
        return ""

    """
    Checks if given language contains any invalid keys
    Output:
        - An empty string if there aren't any errors
        - A descriptive message about the invalid key(s)
    """
    def handle_invalid_keys(self, language):
        return ""