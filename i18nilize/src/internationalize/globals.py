# globals.py

# Test Token: "c84234c3-b507-4ed0-a6eb-8b10116cdef1"

class GlobalToken:
    def __init__(self):
        self.value = "dummy"

API_BASE_URL = "http://localhost:8000/api/"

TOKEN_ENDPOINT = f"{API_BASE_URL}token/"
TRANSLATIONS_ENDPOINT = f"{API_BASE_URL}translations/"
PULL_TRANSLATIONS_ENDPOINT = f"{TRANSLATIONS_ENDPOINT}pull/"

LANGUAGES_DIR = 'src/internationalize/languages'

token = GlobalToken()
