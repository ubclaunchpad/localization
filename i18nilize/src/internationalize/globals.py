# Test Token: "c84234c3-b507-4ed0-a6eb-8b10116cdef1"
import os


class GlobalToken:
    def __init__(self):
        self.value = "replace_with_valid_token"


CONFIG_FILE_PATH = os.path.expanduser("~/.i18nilize_config.json")
# Directory values are set dynamically on startup in command_line.py
ROOT_DIRECTORY = ""
LANGUAGES_DIR = ""

API_BASE_URL = "http://localhost:8000/api"
TOKEN_ENDPOINT = f"{API_BASE_URL}/token"
TRANSLATIONS_ENDPOINT = f"{API_BASE_URL}/translations/"
PULL_TRANSLATIONS_ENDPOINT = f"{API_BASE_URL}/translations/pull/"
PUSH_TRANSLATIONS_ENDPOINT = f"{API_BASE_URL}/translations/push/"


token = GlobalToken()
