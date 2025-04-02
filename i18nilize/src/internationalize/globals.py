import os
 
from .project_root_utils import get_project_root_directory
class GlobalToken:
    def __init__(self):
        self.value = "dummy-value"

class MSGlobalToken:
    def __init__(self):
        self.value = "dummy"

# Directory values are set dynamically on startup in command_line.py
ROOT_DIRECTORY = ""
LANGUAGES_DIR = ""

API_BASE_URL = "http://localhost:8000/api/"

TOKEN_ENDPOINT = f"{API_BASE_URL}token/"
MS_TOKEN_ENDPOINT = f"{API_BASE_URL}ms-token/"
TRANSLATIONS_ENDPOINT = f"{API_BASE_URL}translations/"
PULL_TRANSLATIONS_ENDPOINT = f"{TRANSLATIONS_ENDPOINT}pull/"
PUSH_TRANSLATIONS_ENDPOINT = f"{TRANSLATIONS_ENDPOINT}push/"
WRITER_PERMISSIONS_ENDPOINT = f"{API_BASE_URL}writer-permission/"

LANGUAGES_DIR = 'languages'
DIFF_STATE_DIR = 'diff_state'
ENV_FILE = ".env"

def initialize_root_directory():
    try:
        global ROOT_DIRECTORY, LANGUAGES_DIR, DIFF_STATE_DIR, ENV_FILE
 
        if ROOT_DIRECTORY and LANGUAGES_DIR and DIFF_STATE_DIR and ENV_FILE:
            return
 
        root_directory = get_project_root_directory()
        ROOT_DIRECTORY = root_directory
        LANGUAGES_DIR = os.path.join(root_directory, "languages")
        DIFF_STATE_DIR = os.path.join(root_directory, "diff_state")
        ENV_FILE = os.path.join(DIFF_STATE_DIR, ".env")
    except FileNotFoundError as err:
        print("Error:", err)
        exit(1)
 

token = GlobalToken()
ms_token = MSGlobalToken()
initialize_root_directory()
