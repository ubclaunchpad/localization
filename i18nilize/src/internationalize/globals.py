# globals.py

class GlobalToken:
    def __init__(self):
        self.value = "dummy"  

API_BASE_URL = "http://localhost:8000/api/"

TOKEN_ENDPOINT = f"{API_BASE_URL}token/"
TRANSLATIONS_ENDPOINT = f"{API_BASE_URL}translations/"

token = GlobalToken()