import os

from .project_root_utils import get_project_root_directory


# Test Token: "c84234c3-b507-4ed0-a6eb-8b10116cdef1"
class GlobalToken:
    def __init__(self):
        self.value = "9af7f4cd-8c81-41a2-abac-0faf8d6a2902"


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
        root_directory = get_project_root_directory()

        global ROOT_DIRECTORY, LANGUAGES_DIR

        ROOT_DIRECTORY = root_directory
        LANGUAGES_DIR = os.path.join(root_directory, "languages")

    except FileNotFoundError as err:
        print("Error:", err)
        exit(1)


token = GlobalToken()
initialize_root_directory()
