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

API_BASE_URL = "http://localhost:8000/api/"

TOKEN_ENDPOINT = f"{API_BASE_URL}token/"
MS_TOKEN_ENDPOINT = f"{API_BASE_URL}ms-token/"
TRANSLATIONS_ENDPOINT = f"{API_BASE_URL}translations/"
PULL_TRANSLATIONS_ENDPOINT = f"{TRANSLATIONS_ENDPOINT}pull/"
PUSH_TRANSLATIONS_ENDPOINT = f"{TRANSLATIONS_ENDPOINT}push/"
WRITER_PERMISSIONS_ENDPOINT = f"{TRANSLATIONS_ENDPOINT}writer-permission/"

LANGUAGES_DIR = 'languages'

token = GlobalToken()
ms_token = MSGlobalToken()
