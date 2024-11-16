# api_helpers.py
from internationalize.helpers import generate_file
import globals
from core.i18nilize.views import TokenView
from rest_framework.request import Request
from django.http import HttpRequest


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
    
def generate_translation_file(language):
    token = globals.token
    if not token:
        print("Token not found. Creating a new token...")
        create_token()
        token = globals.token
        if not token:
            raise Exception("Failed to create token.")
        
    if not language:
        raise Exception("Language parameter is required.")
    
    generate_file(language, token)
    print(f"Generated translation file for language: {language}")

