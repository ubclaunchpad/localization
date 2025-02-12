# globals.py

# Test Token: "c84234c3-b507-4ed0-a6eb-8b10116cdef1"
import os
import json
import sys

class GlobalToken:
    def __init__(self):
        self.value = "ae54501d-48c1-4a05-80d3-2b4d417de771"

CONFIG_FILE = os.path.expanduser("~/.i18nilize_config.json")

def find_project_root(start_path=None):
    """Finds the root directory of the project by locating a `.git` folder."""
    if start_path is None:
        start_path = os.getcwd()  

    current_path = os.path.abspath(start_path)

    while current_path != os.path.dirname(current_path):  
        if os.path.isdir(os.path.join(current_path, ".git")):
            return current_path  
        current_path = os.path.dirname(current_path) 

    return None  

def get_installation_directory():
    """Gets the root directory of the project."""
    git_root = find_project_root()
    if git_root:
        return git_root  

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config.get("installation_dir")

    return os.getcwd()  

ROOT_DIRECTORY = get_installation_directory()

print(f"[DEBUG] ROOT_DIRECTORY is set to: {ROOT_DIRECTORY}")

API_BASE_URL = "http://localhost:8000/api/"

TOKEN_ENDPOINT = f"{API_BASE_URL}token/"
TRANSLATIONS_ENDPOINT = f"{API_BASE_URL}translations/"
PULL_TRANSLATIONS_ENDPOINT = f"{TRANSLATIONS_ENDPOINT}pull/"
PUSH_TRANSLATIONS_ENDPOINT = f"{TRANSLATIONS_ENDPOINT}push/"

LANGUAGES_DIR = os.path.join(ROOT_DIRECTORY, 'languages')


token = GlobalToken()
