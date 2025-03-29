import os

from .project_root_utils import get_project_root_directory


# Test Token: "c84234c3-b507-4ed0-a6eb-8b10116cdef1"
class GlobalToken:
    def __init__(self):
        self.value = "dummy-value"

class MSGlobalToken:
    def __init__(self):
        self.value = ""

# Directory values are set dynamically on startup in command_line.py
ROOT_DIRECTORY = ""
LANGUAGES_DIR = ""

API_BASE_URL = "http://localhost:8000/api"
TOKEN_ENDPOINT = f"{API_BASE_URL}/token"
TRANSLATIONS_ENDPOINT = f"{API_BASE_URL}/translations/"
PULL_TRANSLATIONS_ENDPOINT = f"{API_BASE_URL}/translations/pull/"
PUSH_TRANSLATIONS_ENDPOINT = f"{API_BASE_URL}/translations/push/"


def initialize_root_directory():
    try:
        global ROOT_DIRECTORY, LANGUAGES_DIR

        if ROOT_DIRECTORY and LANGUAGES_DIR:
            return

        root_directory = get_project_root_directory()
        ROOT_DIRECTORY = root_directory
        LANGUAGES_DIR = os.path.join(root_directory, "languages")
    except FileNotFoundError as err:
        print("Error:", err)
        exit(1)


token = GlobalToken()
initialize_root_directory()
