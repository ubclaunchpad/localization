# api_helpers.py
from . import globals
from core.i18nilize.views import TokenView
from rest_framework.request import Request
from django.http import HttpRequest
from i18nilize.services import translation_processor as tp


def create_token():
    http_request = HttpRequest()
    http_request.method = 'POST'
    
    request = Request(http_request)

    token_view = TokenView()
    response = token_view.post(request)

    if response.status_code == 201:
        globals.token = response.data.get("value")
        print("Token set.")
    else:
        raise Exception(f"Failed to retrieve token. Status code: {response.status_code}")
    
def fetch_translation_data(language):
    token = globals.token
    if not token:
        print("Token not found. Creating a new token...")
        create_token()
        token = globals.token
        if not token:
            raise Exception("Failed to create token.")
        
    if not language:
        raise Exception("Language parameter is required.")
    
    translations = tp.get_translations_by_language(language, token)
    if not translations:
        raise Exception(f"No translations found for language: {language}")
    
    print(f"Generated translation data for language: {language}")
