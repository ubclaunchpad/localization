# globals.py

# Test Token: "c84234c3-b507-4ed0-a6eb-8b10116cdef1"
import os
import json
import sys

class GlobalToken:
    def __init__(self):
        self.value = "be75d9b5-7785-4594-957c-59431c897acd"

CONFIG_FILE = os.path.expanduser("~/.i18nilize_config.json")

def get_installation_directory():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config.get("installation_dir")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if "env" in current_dir:
        current_dir = os.path.dirname(current_dir)
    return current_dir

ROOT_DIRECTORY = get_installation_directory()

API_BASE_URL = "http://localhost:8000/api/"

TOKEN_ENDPOINT = f"{API_BASE_URL}token/"
TRANSLATIONS_ENDPOINT = f"{API_BASE_URL}translations/"
PULL_TRANSLATIONS_ENDPOINT = f"{TRANSLATIONS_ENDPOINT}pull/"
PUSH_TRANSLATIONS_ENDPOINT = f"{TRANSLATIONS_ENDPOINT}push/"

LANGUAGES_DIR = os.path.join(ROOT_DIRECTORY, 'languages')


token = GlobalToken()
